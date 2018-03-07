#!/usr/bin/env python3

import logging
import requests
from datetime import timedelta, datetime
import configparser
import time

FP_PROTO = 'https'
FP_HOST = FP_PROTO + '://www.floatplane.com/api'

FP_VIDEO_GET = 'https://linustechtips.com/main/applications/floatplane/interface'
VALIDITY_PERIOD = 15

FORMAT = '%(process)d %(processName)s %(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=0)
log = logging.getLogger('Floatplane')

_cache = {}
_cache_time = {}

def normalize_key(key, *args, **kwargs):
	log.debug("Key: {}".format(key))
	log.debug("Args: {}".format(args))
	log.debug("KwArgs: {}".format(kwargs))

	arg_str = ['']
	for it in args:
		it_str = '_'.join(map(str,it))
		log.debug('>> {}'.format(it_str))
		arg_str.append(it_str)

	for key, value in kwargs:
		arg_str.append('{}={}'.format(key, value))

	cache_key = (key +
		'#' + '_'.join(arg_str)
	)

	log.debug("CacheKey: {}".format(cache_key))

	return cache_key

def memorize(key):
	def _decorating_wrapper(func):
		def _caching_wrapper(*args, **kwargs):
			cache_key = normalize_key(key, args, kwargs)
			now = time.time()

			log.debug('Cache: {}'.format(key))

			# if cached and still valid -> use it
			if _cache_time.get(cache_key, now) > now:
				log.debug('Cache still valid')
				return _cache[cache_key]

			log.debug('Cache invalid ... running function')
			ret = func(*args, **kwargs)

			_cache[cache_key] = ret
			_cache_time[cache_key] = now + VALIDITY_PERIOD

			log.debug('Cache: Saving value until {}'.format(_cache_time[cache_key]))
			return ret
		return _caching_wrapper
	return _decorating_wrapper

class Activity:
	def __init__(self, id=None, user=None):
		if type(user) is dict:
			user = User.generate(user)
		
		self.id = id # String : Id
		self.user = user # User

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Activity()
		if type(source) is str and len(source) > 0:
			return Activity(id=source)

		return Activity(source['id'], source['user'])

class User:
	def __init__(self, id=None, username=None, profileImage=None, email=None):
		if type(profileImage) is dict:
			if 'path' in profileImage:
				profileImage = Image.generate(profileImage)
			else:
				profileImage = FullImage.generate(profileImage)

		self.id = id # String : Id (Hash?)
		self.email = email # String
		self.username = username # String
		self.profileImage = profileImage # Image

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return User()
		if type(source) is str and len(source) > 0:
			return User(id=source)
		
		email = [source['email'] if 'email' in source else None]

		return User(source['id'], source['username'], source['profileImage'], email)

class UserConnection:
	def __init__(self, key=None, name=None, enabled=False, connected=False, connectedAccount=None):
		self.key = key # String [ltt]
		self.name = name # String
		self.enabled = enabled # Bool
		self.connected = connected # Bool
		self.connectedAccount = connectedAccount # ???

class Creator:
	def __init__(self, id=None, owner=None, title=None, urlname=None,
		description=None, about=None, cover=None, category=None):
		if type(cover) is dict:
			cover = Image.generate(cover)
		
		if type(owner) is dict:
			owner = User.generate(owner)
		
		self.id = id # String : Id (Hash?)
		self.owner = owner # String : Id (Hash?)
		self.title = title # String
		self.urlname = urlname # String : ShortTag
		self.description = description # String
		self.about = about # String : Description (Markdown?!)
		self.cover = cover # Image

		self.category = category # String : Id

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Creator()

		if type(source) is str:
			return Creator(source)

		if 'coverImage' in source:
			coverImage = source['coverImage']
		else:
			coverImage = None

		return Creator(
			source['id'], source['owner'], source['title'], source['urlname'],
			source['description'], source['about'], coverImage, source['category']
		)

class Plan:
	def __init__(self, title=None, description=None, price=0.0, currency=None,
		interval=None, intervalCount=0, logo=None):
		#if type(logo) is dict:
			#logo = Logo.generate(logo)

		self.title = title # String
		self.description = description # String
		self.price = price # Double
		self.currency = currency # String [cad, usd?, eur?]
		self.interval = interval # String [month, year?]
		self.intervalCount = intervalCount # Int // Every x months ?
		self.logo = logo # null?

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Plan()

		return Plan(source['title'], source['description'], source['price'], source['currency'],
			source['interval'], source['intervalCount'], source['logo'])

class Subscription:
	def __init__(self, startDate=None, endDate=None, plan={}, creator={}):
		if type(creator) is dict or type(creator) is str or creator is None:
			creator = Creator.generate(creator)

		if type(plan) is dict or plan is None:
			plan = Plan.generate(plan)

		self.startDate = startDate # IsoTimestamp
		self.endDate = endDate # IsoTimestamp
		self.plan = plan # Subscription Plan
		self.creator = creator # Creator

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Subscription()
		try:
			return Subscription(source['startDate'], source['endDate'], source['plan'], source['creator'])
		except Exception as e:
			log.error(e)

class Firebase:
	def __init__(self):
		self.messagingSenderId = None # FirebaseSourceId

class FloatplaneInfo:
	def __init__(self):
		self.workerUrl = None # Sub-Url
		self.firebase = {} # FirebaseInfo

class FullImage:
	def __init__(self, id=None, createdAt=None, extension=None, height=None,
		originalName=None, owner=None, size=None, imageType=None, updatedAt=None, width=None):
		
		self.id = id # String : Guid
		
		self.extension = extension # String
		self.size = size # Integer
		self.type = imageType # String : Guid
		self.originalName = originalName # String

		self.owner = owner # String : Guid

		self.height = height # Integer
		self.width = width # Integer
		
		self.createdAt = createdAt # Timestamp
		self.updatedAt = updatedAt # Timestamp

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return FullImage()
		
		if type(source) is str and len(source) > 0:
			return FullImage(id=source)
		
		return FullImage(
			id=source['id'],
			createdAt=source['createdAt'],
			extension=source['extension'],
			height=source['height'],
			originalName=source['originalName'],
			owner=source['owner'],
			size=source['size'],
			imageType=source['type'],
			updatedAt=source['updatedAt'],
			width=source['width'])


class Image:
	def __init__(self, width=0, height=0, path=None, childImages=[]):
		tmpChildImages = []
		if type(childImages) is list:
			for child in childImages:
				tmpChildImages.append(Image.generate(child))
			childImages = tmpChildImages

		if type(childImages) is dict or childImages is None:
			childImages = [Image.generate(child)]

		if type(width) is dict:
			raise Exception('What?!')

		self.width = width # Int : px
		self.height = height # Int : px
		self.path = path # String : FullURL
		self.childImages = childImages # Image[] : Ignore if Empty

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Image()

		if 'childImages' in source:
			return Image(source['width'], source['height'], source['path'], source['childImages'])
		else:
			return Image(source['width'], source['height'], source['path'])

class Video:
	def __init__(self, title=None, guid=None, tags=[], description=None, private=False,
		releaseDate=None, duration=0, creator=None, thumbnail=None, relatedVideos=[]):

		if type(creator) is dict or type(creator) is str or creator is None:
			creator = Creator.generate(creator)

		if type(thumbnail) is dict or thumbnail is None:
			thumbnail = Image.generate(thumbnail)

		self.title = title # String
		self.guid = guid # String : NoGUID!
		self.tags = tags # String[]
		self.description = description # String?
		self.private = private # Bool
		self.releaseDate = releaseDate # IsoTimestamp
		self.duration = duration # Int? : Seconds?
		self.creator = creator # Creator
		self.thumbnail = thumbnail # Thumbnail
		self.relatedVideos = relatedVideos # Videos

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Video()
		
		if type(source) is str and len(source) > 0:
			return Video(title=source)

		return Video(
			source['title'], source['guid'], source['tags'], source['description'], source['private'],
			source['releaseDate'], source['duration'], source['creator'], source['thumbnail']
		)

class Playlist:
	def __init__(self):
		self.id = None # String : Id (Hash?)
		self.title = None # String
		self.updatedAt = None # IsoTimestamp
		self.videoCount = 0 # Int : Number of Videos
		self.image = {} # Image

class CommentInteraction:
	def __init__(self, like=None, dislike=None):
		self.like = like # Int
		self.dislike = dislike # Int

	@staticmethod
	def generate(source):
		if source is None or type(source) is str and len(source) is 0:
			return CommentInteraction()

		return CommentInteraction(source['like'], source['dislike'])

class Comment:
	def __init__(self, id=None, user=None, video=None, text=None, replying=None, postDate=None,
		editDate=None, interactions=[], replies=[], interactionCounts={}):
		if type(user) is dict or type(user) is str or user is None:
			user = User.generate(user)

		if type(video) is dict or type(video) is str or video is None:
			video = Video.generate(video)

		if type(interactionCounts) is dict or type(interactionCounts) is str or interactionCounts is None:
			interactionCounts = CommentInteraction.generate(interactionCounts)

		self.id = id # String : Id (Hash?)
		self.user = user # User
		self.video = video # Video
		self.text = text # String
		self.replying = replying # null?
		self.postDate = postDate # IsoTimestamp
		self.editDate = editDate # IsoTimestamp
		self.interactions = interactions # ?
		self.replies = replies # ?
		self.interactionCounts = interactionCounts # CommentInteraction
	
	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Comment()
		
		return Comment(
			source['id'], source['user'], source['video'], source['text'], source['replying'],
			source['postDate'], source['editDate'], source['interactions'], source['replies'],
			source['interactionCounts']
		)

class Edge:
	def __init__(self):
		self.client = None # Client
		self.edges = [] # EdgeServer

class Client:
	def __init__(self):
		self.ip = None # String : IPv4/IPv6
		self.country_code = None # String : [US]
		self.country_name = None # String : [United State]
		self.region_code = None # String ?
		self.region_name = None # String ?
		self.city = None # String ?
		self.zip_code = None # String ?
		self.time_zone = None # String ?
		self.latitude = 0.0 # Double
		self.longitude = 0.0 # Double
		self.metro_code = 0 # Int ?

class EdgeDatacenter:
	def __init__(self):
		self.country_code = None # String : [CA, FR, AU]
		self.region_code = None # String : [QC, A, NSW]

class EdgeServer:
	def __init__(self):
		self.hostname = None # String
		self.queryPort = 0 # Int : Port
		self.bandwith = 0 # Long : in kbit?
		self.allowDownload = False # Boolean
		self.allowStreaming = False # Boolean (Live-Streaming?)
		self.datacenter = None # EdgeDatacenter

class Error:
	def __init__(self):
		self.errors = None # {0: reason : String}
		self.message = None # String

class FloatplaneClient:

	def __init__(self, options={}, fpCookies=None, lmgCookies=None):
		if 'target' not in options:
			self.fpTarget = FP_HOST
		else:
			self.fpTarget = options['target']

		if 'videoSourceUrl' not in options:
			self.videoGetUrl = FP_VIDEO_GET
		else:
			self.videoGetUrl = options['videoSourceUrl']

		self.fpCookies = fpCookies
		self.lmgCookies = lmgCookies

		self.loggedIn = False

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
					'ips4_hasJS' : 'false',
					'ips4_pass_hash' : lmgConfig['pass_hash'],
					'ips4_member_id' : lmgConfig['member_id'],
					'ips4_ipsTimezone' : lmgConfig['timezone'],
					'ips4_login_key' : lmgConfig['login_key'],
					'ips4_device_key' : lmgConfig['device_key']
				}

		except Exception as e:
			log.warn('Could not read config: {}'.format(e))

		return [username, password]

	def requestApi(self, path, params={}, method='GET', cookieJar=None, target=None, headers=None):
		if cookieJar is None:
			cookies = self.fpCookies
		else:
			cookies = cookieJar

		if target is None:
			target = self.fpTarget

		req = requests.request(method, target + path, data=params, cookies=cookies, headers=headers)

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
						errors.append(err['reason'])

					msg = "{} -> {}".format('; '.join(errors), json['message'])
					log.error(msg)
					raise Exception(msg)

			return json
		except Exception as e:
			log.error('{}: {} seems wrong (not yet implemented?) {}'.format(method, path, e))

	# /user/login
	def login(self, username, password):
		path = '/user/login'
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
		
		if 'Logged In Successfully' not in json['message']:
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
	def getVideosByCreator(self, creatorGuid, limit=5):
		path = '/creator/videos?creatorGUID={}'.format(creatorGuid)
		videoList = []

		if limit is not None and limit > 0:
			path += '&limit={}'.format(limit)
		
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

		log.debug(json)

		video = Video.generate(json)
		return video

	# /video/related?videoGUID=XXXX
	@memorize('relatedVideos')
	def getReleatedVideos(self, videoGuid):
		pass

	# /video/comments?videoGUID=XXXX
	@memorize('videoComments')
	def getVideoComments(self, videoGuid, limit=None):
		comments = []
		
		path = '/video/comments?videoGUID={}'.format(videoGuid)
		if limit is not None and limit > 0:
			path += '&limit={}'.format(limit)
		
		if limit is 0:
			return comments

		json = self.requestApiJson(path)

		if json is None:
			log.info('Video ({}) not found'.format(videoGuid))
			return comments

		for comment in json['comments']:
			comment_obj = Comment.generate(comment)
			comment_obj.user = self.getUser(comment_obj.user.id)[comment_obj.user.id]
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
		pass

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

		#raise Exception('Please use getVideoURL insted')

		path = '/video_url.php?video_guid={}&video_quality={}'.format(videoId, quality)
		req = self.requestApi(path, cookieJar=self.lmgCookies, target=FP_VIDEO_GET)

		return req.text
	
	# GET /video/url?guid=00nU1J5UfP&quality=1080
	@memorize('videoURL')
	def getVideoURL(self, videoId, quality=1080):
		path = '/video/url?guid={}&quality={}'.format(videoId, quality)
		req = self.requestApi(path, headers={
			'Referer': 'https://www.floatplane.com/video/{}'.format(videoId)
		})
		
		response = req.text
		if req is None or len(response) <= 0 or req.status_code != 200:
			log.info('VideoURL could not be acquired: {}'.format(response))
			return
		
		return response

	# /playlist/videos?playlistGUID=XXXX&limit=XXX
	# ==> [Video] ?
	@memorize('playlistVideos')
	def getPlaylistVideos(self, playlist, limit=3):
		pass

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