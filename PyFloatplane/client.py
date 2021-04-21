import configparser
import logging
import requests
import re

from datetime import timedelta, datetime

# from . import annotations
from . import config

from PyFloatplane.annotations import memorize
from PyFloatplane.models import *

log = logging.getLogger('Floatplane')
#logging.basicConfig(level=logging.DEBUG, format="%(message)s")


class FloatplaneClient:

    def __init__(self, options={}, fpCookies=None, lmgCookies=None):
        if 'target' not in options:
            self.fpTarget = config.FP_HOST
        else:
            self.fpTarget = options['target']

        if 'videoSourceUrl' not in options:
            self.videoGetUrl = config.FP_VIDEO_GET
        else:
            self.videoGetUrl = options['videoSourceUrl']

        self.fpCookies = fpCookies
        self.lmgCookies = lmgCookies
        self.__req_session = None

        self.loggedIn = False

        self.fixedHeaders = {
            'User-Agent': 'PyFloatplane (Sammy8806, +https://github.com/sammy8806/pyFloatplane)'
        }

    def loadCredentials(self, filename='floatplane.ini', path='.'):
        try:
            config = configparser.ConfigParser()
            config.read('{}/{}'.format(path, filename))

            if 'floatplane' in config:
                log.debug('Found Floatplane Config')
                username = config['floatplane']['username']
                password = config['floatplane']['password']

            if 'lmg-forums' in config:
                log.debug('Found LMG Config')
                lmgConfig = config['lmg-forums']
                self.lmgCookies = {
                    'ips4_hasJS': 'false',
                    'ips4_pass_hash': lmgConfig['pass_hash'],
                    'ips4_member_id': lmgConfig['member_id'],
                    'ips4_ipsTimezone': lmgConfig['timezone'],
                    'ips4_login_key': lmgConfig['login_key'],
                    'ips4_device_key': lmgConfig['device_key']
                }

        except Exception as e:
            log.warn('Could not read config: {}'.format(e))

        return [username, password]

    def requestApi(self, path, params={}, method='GET', cookieJar=None, target=None, headers={}):
        if cookieJar is None:
            cookies = self.fpCookies
        else:
            cookies = cookieJar

        if target is None:
            target = self.fpTarget

        if self.__req_session is None:
            self.__req_session = requests.Session()

        request_headers = {**headers, **self.fixedHeaders}

        req = self.__req_session.request(method, target + path, data=params, cookies=cookies, headers=request_headers)

        if req.status_code == 404:
            raise Exception('{}: {} # {} not found!'.format(method, path, params))

        return req

    def requestApiJson(self, path, params=[], method='GET', cookieJar=None, target=None, headers=None):
        try:
            json = self.requestApi(path, params, method, cookieJar, target).json()

            if 'errors' in json and type(json['errors']) is list:
                if len(json['errors']) > 0:
                    errors = []
                    for err in json['errors']:
                        if 'reason' in json['errors']:
                            errors.append(err['reason'])

                    errorMsg = json['message'] if 'message' in json else json['name'] if 'name' in json else None
                    msg = "{} -> {}".format('; '.join(errors), errorMsg)
                    log.error(msg)
                    raise Exception(msg)

            return json
        except Exception as e:
            log.error('{}: {} seems wrong (not yet implemented?) {}'.format(method, path, e))

    # /user/login
    def login(self, username, password):
        path = '/auth/login'
        request = self.requestApi(path, method='POST', params={
            'username': username,
            'password': password
        })

        if len(request.cookies) > 0:
            self.fpCookies = request.cookies
            self.loggedIn = True

        json = request.json()

        if len(json) <= 0:
            return None

        if 'user' not in json:
            raise Exception('Error while login-request: {}'.format(json['message']))

        return User.generate(json['user'])

    # /user/subscriptions
    @memorize('subscriptions')
    def getSubscriptions(self):
        path = '/user/subscriptions'

        json = self.requestApiJson(path)

        if len(json) <= 0:
            return

        subObjects = []
        for sub in json:
            subObj = Subscription.generate(sub)
            subObjects.append(subObj)

        return subObjects

    # /user/administrator?id=<userGuid>
    # ==> Boolean
    @memorize('administrator')
    def isAdministrator(self, user):
        userObj = user if type(user) is not User else self.getUser(user).values()[0]

        path = '/user/administrator?id={}'.format(userObj.id)
        adminStatus = self.requestApiJson(path)

        # @TODO: Consider using exceptions
        if type(adminStatus) is not bool:
            log.info('Could not check administrative status for {}'.format(userObj.name))
            return

        return adminStatus

    # /creator/named?creatorURL=linustechtips
    # ==> [Creator]
    @memorize('creatorByName')
    def getCreateByName(self, creatorName):
        pass

    # /creator/videos?creatorGUID=XXXX&limit=n
    @memorize('videosByCreator')
    def getVideosByCreator(self, creatorGuid, limit=5, fetch_after=0):
        path = '/creator/videos?creatorGUID={}'.format(creatorGuid)
        videoList = []

        if limit is not None and limit > 0:
            path += '&limit={}'.format(limit)

        if fetch_after is not None and fetch_after > 0:
            path += '&fetchAfter={}'.format(fetch_after)

        json = self.requestApiJson(path)

        if json is None:
            log.info('No videos found for {}'.format(creatorGuid))
            return videoList

        for video in json:
            videoList.append(Video.generate(video))

        return videoList

    # /video/info?videoGUID=XXXX
    @memorize('videoInfo')
    def getVideoInfo(self, videoGuid):
        path = '/video/info?videoGUID={}'.format(videoGuid)
        json = self.requestApiJson(path)

        if len(json) <= 0:
            log.info('No video found for {}'.format(videoGuid))
            return

        video = Video.generate(json)
        return video

    # /video/related?videoGUID=XXXX
    @memorize('relatedVideos')
    def getReleatedVideos(self, videoGuid):
        path = '/video/related?videoGUID={}'.format(videoGuid)
        json = self.requestApiJson(path)

        if len(json) <= 0:
            log.info('No related videos found for {}'.format(videoGuid))
            return

        return [Video.generate(vid) for vid in json]

    # /video/comments?videoGUID=XXXX
    @memorize('videoComments')
    def getVideoComments(self, videoGuid, limit=None):
        comments = []

        path = '/video/comments?videoGUID={}'.format(videoGuid)
        if limit is not None and limit > 0:
            path += '&limit={}'.format(limit)

        if limit == 0:
            return comments

        json = self.requestApiJson(path)

        if json is None:
            log.info('Video ({}) not found'.format(videoGuid))
            return comments

        for comment in json['comments']:
            comment_obj = Comment.generate(comment)
            comment_obj.user = self.getUser(comment_obj.user.id)[comment_obj.user.id]

            for comment in comment_obj.replies:
                comment.user = self.getUser(comment.user.id)[comment.user.id]

            comments.append(comment_obj)

        return comments

    # /video/comment/interaction/set
    # ==> GUID id, GUID user, GUID comment, GUID?? type
    def postCommentReaction(self, commentGUID, type):
        path = '/video/comment/interaction/set'
        req = self.requestApiJson(path, method='POST', params={
            'commentGUID': commentGUID,
            'type': type
        })

        log.debug(req)

    # @TODO
    # /video/comment/interaction/clear(commentGUID=XXX, type=null)
    def clearCommentReaction(self, commentGUID, type):
        path = '/video/comment/interaction/clear'
        req = self.requestApiJson(path, method='POST', params={
            'commentGUID': commentGUID,
            'type': type
        }, headers={
            'Referer': 'https://www.floatplane.com/video/em996tSOVL'
        })

        log.debug(req)

    # /edges
    @memorize('edges')
    def getEdges(self):
        path = '/edges'
        json = self.requestApiJson(path)

        if json is None or len(json) <= 0:
            log.info('No edges found')
            return

        return Edge.generate(json)

    # /user/info?id=XXXX[&id=XXXX]
    @memorize('user')
    def getUser(self, userId):
        path = '/user/info?' + self.getRequestParamList('id', userId)
        json = self.requestApiJson(path)

        if len(json) <= 0:
            log.info('No such users found')
            return

        userList = {}
        for user in json['users']:
            userList[user['id']] = User.generate(user['user'])

        return userList

    # /user/named?username=<userName>
    # ==> {users: [ User, ... ]}
    @memorize('userByName')
    def getUserByName(self, userName):
        pass

    # /user/activity?id=<userGuid>
    # ==> [ Activity ]
    @memorize('userActivity')
    def getUserActivity(self, user):
        userObj = user if type(user) is not User else self.getUser(user).values()[0]
        path = '/user/activity?' + self.getRequestParamList('id', userObj.id)
        json = self.requestApiJson(path)

        if len(json) <= 0:
            log.info('No activity for user {} found'.format(userObj.username))
            return

        actitvityList = []
        for activity in json['activity']:
            actitvityList.append(Activity.generate(activity))

        return actitvityList

    # /image/optimizations?imageType=profile_images
    @memorize('imageOptimizations')
    def getImageOptimizations(self):
        # {"profile_images":[{"quality":"80","width":250,"height":250},{"quality":"80","width":100,"height":100},{"quality":"80","width":720,"height":720}]}
        pass

    # POST /user/avatar
    # multipart/form-data
    # Content-Disposition: form-data; name="avatar"; filename="<filename_with_ending>"
    # Content-Type: image/jpeg
    def pushUserAvatar(self, avatar):
        pass

    # /user/connections/list
    @memorize('userConnections')
    def getUserConnections(self):
        pass

    # /push/web/info
    @memorize('pushInfo')
    def getPushInfo(self):
        pass

    # /user/creator?id=XXXX
    @memorize('creator')
    def getCreator(self, creatorId):
        pass

    def getRequestParamList(self, paramName, values):
        requestString = ''

        if type(values) is list:
            first = True
            for guid in values:
                if not first:
                    requestString += '&'

                requestString += '{}={}'.format(paramName, guid)
                first = False
        else:
            requestString += '{}={}'.format(paramName, values)

        return requestString

    @memorize('creatorList')
    def getCreatorList(self):
        path = '/creator/list'
        json = self.requestApiJson(path)

        if len(json) <= 0:
            log.info('No such creators found')
            return

        creators = []
        for creator in json:
            creators.append(Creator.generate(creator))

        return creators

    # /creator/info?creatorGUID=XXXXX&creatorGUID=XXXXX
    @memorize('creatorInfo')
    def getCreatorInfo(self, creatorGUID):
        path = '/creator/info?' + self.getRequestParamList('creatorGUID', creatorGUID)
        json = self.requestApiJson(path)

        if len(json) <= 0:
            log.info('No such creators found')
            return

        creatorInfos = []
        for creator in json:
            creatorInfos.append(Creator.generate(creator))

        return creatorInfos

    # VIDEO_HOST/video_url.php?video_guid=XXXX&video_quality=XXXX
    @memorize('videoLink')
    def getVideoLink(self, videoId, quality=1080):
        """
        Needs Cookie for https://linustechtips.com
        """

        raise Exception('Please use getVideoURL insted')

        path = '/video_url.php?video_guid={}&video_quality={}'.format(videoId, quality)
        req = self.requestApi(path, cookieJar=self.lmgCookies, target=config.FP_VIDEO_GET)

        return req.text

    # GET /video/url?guid=00nU1J5UfP&quality=1080
    @memorize('videoURL')
    def getVideoURL(self, videoId, quality=1080, is_download=None, is_stream=True):
        path = '/video/url?guid={}&quality={}'.format(videoId, quality)
        req = self.requestApi(path, headers={
            'Referer': 'https://www.floatplane.com/video/{}'.format(videoId)
        })

        response = req.text
        if req is None or len(response) <= 0 or req.status_code != 200:
            log.info('VideoURL could not be acquired: {}'.format(response))
            return

        if is_download is True:
            is_stream = None

        edge_server = self.getTargetEdgeServer(guid=videoId, allowDownload=is_download, allowStreaming=is_stream)
        target_type = 'vod' if is_stream else 'download' if is_download else None
        cdn_info = self.getCdnDelivery(guid=videoId, type=target_type)

        template_uri = 'https://' + edge_server.hostname + cdn_info.resource.uri
        quality_level = sorted(cdn_info.resource.data.qualityLevels, key=lambda obj: obj.order, reverse=True)
        selected_quality_level = quality_level[0] if len(quality_level) > 0 else '1080p'

        response = template_uri.replace('{qualityLevels}', selected_quality_level.name)
        response = response.replace('{token}', cdn_info.resource.data.token)

        return response

    @memorize('DirectVideoURL')
    def getDirectVideoURL(self, videoId, quality=1080):
        url = self.getVideoURL(videoId, quality, is_download=True)
        return url.replace('/chunk.m3u8', '')

    # /playlist/videos?playlistGUID=XXXX&limit=XXX
    # ==> [Video] ?
    @memorize('playlistVideos')
    def getPlaylistVideos(self, playlist, limit=3):
        playlistId = playlist if type(playlist) is not Playlist else playlist.id

        path = '/playlist/videos?playlistGUID={}&limit={}'.format(playlistId, limit)
        req = self.requestApiJson(path)

        if req is None or len(req) <= 0:
            log.info('Playlist could not be acquired: {}'.format(req))
            return

        videos = []
        for video in req:
            videos.append(Video.generate(video))

        return videos

    # /playlists?creatorGUID={}
    def getCreatorPlaylists(self, creator, limit=5):
        creator = creator if type(creator) is Creator else self.getCreator(creator).values()[0]
        path = '/creator/playlists?creatorGUID={}'.format(creator.id)

        if limit is not None and limit > 0:
            path += '&limit={}'.format(limit)

        req = self.requestApiJson(path)

        if req is None or len(req) <= 0:
            log.info('Creator playlists could not be acquired: {}'.format(req))
            return

        playlists = []
        for playlist in req:
            playlists.append(Playlist.generate(playlist))

        return playlists

    # /video/comment
    # ==> Comment
    def postVideoComment(self, videoGUID, text):
        path = '/video/comment'
        json = self.requestApiJson(path, method='POST', params={'text': text})

        if len(json) <= 0:
            log.error('Comment could not be created: {}'.format(text))
            return

        comment = Comment.generate(json)
        return comment

    # TODO: Validate!
    # /video/comment
    # ==> ?
    def deleteVideoComment(self, commentGUID):
        path = '/video/comment'
        req = self.requestApiJson(path, method='DELETE', params={
            'commentGUID': commentGUID
        })

        log.debug(req)

    # POST: /user/password/reset/request
    # {email: 'test@test.de'}
    # Referer: https://www.floatplane.com/reset-password
    # => {"message":"We sent a recovery link to your email. Please follow the instructions inside the message."}
    def requestPasswordReset(self, email):
        pass

    # Email: https://www.floatplane.com/reset-password?code=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # POST: /user/password/reset
    # {key: '...', password: 'plainpass'}

    # POST: /user/connections/ltt/refresh
    # => {"site":{"key":"ltt","name":"LinusTechTips","enabled":true,"isAccountProvider":true,"connected":true,"connectedAccount":{"remoteUserId":XXXX,"remoteUserName":"XXX"}}}
    def refreshUserConnection(self, partner='ltt'):
        path = '/user/connections/ltt/refresh'
        json = self.requestApiJson(path, method='POST')

        return json

    # GET: https://www.floatplane.com/api/cdn/delivery?type=<download|vod>&guid=XXXX
    def getCdnDelivery(self, guid, type='download'):
        path = '/cdn/delivery?type={}&guid={}'.format(type, guid)
        json = self.requestApiJson(path, method='GET')

        cdn_delivery = CdnDelivery.generate(json)

        return cdn_delivery

    def getTargetEdgeServer(self, guid=None, allowDownload=True, allowStreaming=None):

        target_type = 'vod' if allowStreaming else 'download' if allowDownload else None
        edge_info = self.getEdges() if guid is None or target_type is None else self.getCdnDelivery(guid=guid,
                                                                                                    type=target_type)

        def approx_distance(source_long, source_lat, target_long, target_lat):
            """
            Code taken from https://stackoverflow.com/a/19412565/1679744
            """

            from math import sin, cos, sqrt, atan2, radians
            # approximate radius of earth in km
            R = 6373.0

            lat1 = radians(source_lat)
            lon1 = radians(source_long)
            lat2 = radians(target_lat)
            lon2 = radians(target_long)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            return distance

        if edge_info.client is not None:
            sorted_edges = sorted(edge_info.edges, key=lambda edge: approx_distance(
                edge.datacenter.longitude, edge.datacenter.latitude,
                edge_info.client.longitude, edge_info.client.latitude))
        else:
            sorted_edges = edge_info.edges

        for edge in sorted_edges:
            # allowStreaming = None
            # allowDownload = True

            if allowStreaming is not None and edge.allowStreaming is not allowStreaming:
                continue

            if allowDownload is not None and edge.allowDownload is not allowDownload:
                continue

            return edge

        return sorted_edges[0] if len(sorted_edges) > 0 else EdgeServer()
