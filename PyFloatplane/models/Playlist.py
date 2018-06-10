from PyFloatplane.models.Image import Image

class Playlist:
	def __init__(self, id=None, title=None, updatedAt=None, videoCount=None, image=None):
		self.id = id # String : Id (Hash?)
		self.title = title # String
		self.updatedAt = updatedAt # IsoTimestamp
		self.videoCount = videoCount # Int : Number of Videos

		if image and type(image) is not Image:
			image = Image.generate(image)
		
		self.image = image # Image
	
	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Playlist()

		return Playlist(source['id'], source['title'], source['updatedAt'], source['videoCount'], source['image'])
