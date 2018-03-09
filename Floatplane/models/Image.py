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
