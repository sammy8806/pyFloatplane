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
