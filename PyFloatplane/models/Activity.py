from PyFloatplane.models.User import User

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
