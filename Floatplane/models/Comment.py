from Floatplane.models.User import User
from Floatplane.models.Video import Video
from Floatplane.models.CommentInteraction import CommentInteraction

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
