#!/usr/bin/env python3

import logging
import requests
from datetime import timedelta, datetime
import configparser

FP_PROTO = 'https'
FP_HOST = FP_PROTO + '://www.floatplane.com/api'

FP_VIDEO_GET = 'https://linustechtips.com/main/applications/floatplane/interface'

FORMAT = '%(process)d %(processName)s %(asctime)-15s %(message)s'
#logging.basicConfig(format=FORMAT, level=0)
log = logging.getLogger('Floatplane')

# TODO: Use decorators for caching?

# TODO: Unused
class FPCache:
	def __init__(self, client):
		self.client = client
	pass

# TODO: Unused
class FPCacheEntry:
	def __init__(self, value, lifetime=60, method=None):
		self.lifetime = lifetime
		self.setValue(value)

	def setValue(self, value):
		self.value = value
		self.lastCache = datetime.utcnow()

	def getValue():
		now = datetime.utcnow()
		if self.lastCache + self.lifetime > now:
			return None
		else:
			return self.value

# TODO: Unused
class CreatorCache(FPCache):
	def __init__(self, client):
		super().__init__(client)
		self.creatorCache = {}

	def getByName(self, name):
		pass

	def getById(self, id):
		if id in self.creatorCache:
			return 

class User:
	def __init__(self, id=None, username=None, profileImage=None):
		if type(profileImage) is dict:
			profileImage = Image.generate(profileImage)

		self.id = id # String : Id (Hash?)
		self.username = username # String
		self.profileImage = profileImage # Image

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return User()
		return User(source['id'], source['username'], source['profileImage'])

class UserConnection:
	def __init__(self, key=None, name=None, enabled=False, connected=False, connectedAccount=None):
		self.key = key # String [ltt]
		self.name = name # String
		self.enabled = enabled # Bool
		self.connected = connected # Bool
		self.connectedAccount = connectedAccount # ???

class Creator:
	def __init__(self, id=None, owner=None, title=None, urlname=None,
		description=None, about=None, cover=None):
		if type(cover) is dict:
			cover = Image.generate(cover)
		
		self.id = id # String : Id (Hash?)
		self.owner = owner # String : Id (Hash?)
		self.title = title # String
		self.urlname = urlname # String : ShortTag
		self.description = description # String
		self.about = about # String : Description (Markdown?!)
		self.cover = cover # Image

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Creator()

		if type(source) is str:
			return Creator(source)

		return Creator(
			source['id'], source['owner'], source['title'], source['urlname'],
			source['description'], source['about'], source['cover']
		)

class Plan:
	def __init__(self, title=None, description=None, price=0.0, currency=None,
		interval=None, intervalCount=0, logo=None):
		if type(logo) is dict:
			logo = Logo.generate(logo)

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
	def __init__(self):
		self.like = 0 # Int
		self.dislike = 0 # Int

class Comments:
	def __init__(self):
		self.id = None # String : Id (Hash?)
		self.user = None # User
		self.video = None # Video
		self.text = None # String
		self.replying = None # null?
		self.postDate = None # IsoTimestamp
		self.editDate = None # IsoTimestamp
		self.interactions = [] # ?
		self.replies = [] # ?
		self.interactionCounts = {} # CommentInteraction

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
			self.videoGetUrl = videoSourceUrl

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

	def requestApi(self, path, params={}, method='GET', cookieJar=None, target=None):
		if cookieJar is None:
			cookies = self.fpCookies
		else:
			cookies = cookieJar

		if target is None:
			target = self.fpTarget

		req = requests.request(method, target + path, data=params, cookies=cookies)

		return req

	def requestApiJson(self, path, params=[], method='GET', cookieJar=None, target=None):
		return self.requestApi(path, params, method, cookieJar, target).json()

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

	# /creator/videos?creatorGUID=XXXX&limit=n
	def getVideosByCreator(self, creatorGuid, limit=5):
		path = '/creator/videos?creatorGUID={}&limit={}'.format(creatorGuid, limit)
		json = self.requestApiJson(path)

		if len(json) <= 0:
			log.info('No videos found for {}'.format(creatorGuid))
			return

		videoList = []
		for video in json:
			videoList.append(Video.generate(video))

		return videoList

	# /video/info?videoGUID=XXXX
	def getVideoInfo(self, videoId):
		pass

	# /video/related?videoGUID=XXXX
	def getReleatedVideos(self, videoId):
		pass

	# /video/comments?videoGUID=XXXX
	def getVideoComments(self, videoId):
		pass

	# /edges
	def getEdges(self):
		pass

	# /user/info?id=XXXX[&id=XXXX]
	def getUser(self, userId):
		pass

	# /user/connections/list
	def getUserConnections(self):
		pass

	# /push/web/info
	def getPushInfo(self):
		pass

	# /user/creator?id=XXXX
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

	# /creator/info?creatorGUID=XXXXX&creatorGUID=XXXXX
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
	def getVideoLink(self, videoId, quality=1080):
		"""
		Needs Cookie for https://linustechtips.com
		"""

		path = '/video_url.php?video_guid={}&video_quality={}'.format(videoId, quality)
		req = self.requestApi(path, cookieJar=self.lmgCookies, target=FP_VIDEO_GET)

		return req.text
