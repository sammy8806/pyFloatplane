from PyFloatplane.models.Image import Image
from PyFloatplane.models.FullImage import FullImage

class User:
	def __init__(self, id=None, username=None, profileImage=None, email=None):
		if type(profileImage) is dict:
			if 'path' in profileImage:
				profileImage = Image.generate(profileImage)
			else:
				profileImage = FullImage.generate(profileImage)

		if username:
			self.username = username # String

		self.id = id # String : Id (Hash?)
		self.email = email # String
		self.profileImage = profileImage # Image

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return User()
		if type(source) is str and len(source) > 0:
			return User(id=source)
		
		email = source['email'] if 'email' in source else None
		username = source['username'] if 'username' in source else None

		return User(source['id'], username, source['profileImage'], email)

