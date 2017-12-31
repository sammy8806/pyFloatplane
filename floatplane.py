#!/usr/bin env

import logging
import requests

FP_PROTO = 'https'
FP_HOST = FP_HOST + '://www.floatplane.com/api'

FP_VIDEO_GET = 'https://linustechtips.com/main/applications/floatplane/interface'

FORMAT = '%(process)d %(processName)s %(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

class User:
	def __init__(self):
		self.id = None # String : Id (Hash?)
		self.username = None # String
		self.profileImage = None # Image

class UserConnection:
	def __init__(self):
		self.key = None # String [ltt]
		self.name = None # String
		self.enabled = false # Bool
		self.connected = false # Bool
		self.connectedAccount = 

class Creator:
	def __init__(self):
		self.id = None # String : Id (Hash?)
		self.owner = None # String : Id (Hash?)
		self.title = None # String
		self.urlname = None # String : ShortTag
		self.description = None # String
		self.about = None # String : Description (Markdown?!)
		self.cover = {} # Image

class Plan:
	def __init__(self):
		self.title = None # String
		self.description = None # String
		self.price = 0.0 # Double
		self.currency = None # String [cad, usd?, eur?]
		self.interval = None # String [month, year?]
		self.intervalCount = 0 # Int // Every x months ?
		self.logo = None # null?

class Subscription:
	def __init__(self):
		self.startDate = None # IsoTimestamp
		self.endDate = None # IsoTimestamp
		self.plan = [] # List of plans
		self.creator = None # Creator

class Firebase:
	def __init__(self):
		self.messagingSenderId = None # FirebaseSourceId

class FloatplaneInfo:
	def __init__(self):
		self.workerUrl = None # Sub-Url
		self.firebase = {} # FirebaseInfo

class Image:
	def __init__(self):
		self.width = 0 # Int : px
		self.height = 0 # Int : px
		self.path = None # String : FullURL
		self.childImages = [] # Image[] : Ignore if Empty

class Video:
	def __init__(self):
		self.title = None # String
		self.guid = None # String : NoGUID!
		self.tags = [] # String[]
		self.description = None # String?
		self.private = False # Bool
		self.releaseDate = None # IsoTimestamp
		self.duration = 0 # Int? : Seconds?
		self.creator = None # Creator
		self.thumbnail = None # Thumbnail
		self.relatedVideos = [] # Videos

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

	# /user/subscriptions
	def getSubscriptions(self):
		pass

	# /creator/videos?creatorGUID=XXXX&limit=n
	def getVideosByCreator(self, creator, limit=5):
		pass

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

	# /user/info?id=XXXX
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

	# VIDEO_HOST/video_url.php?video_guid=XXXX&video_quality=XXXX
	def getVideoLink(self, videoId, quality=1080):
		"""
		Needs Cookie for https://linustechtips.com
		"""
		
		pass
