class CommentInteraction:
	def __init__(self, like=None, dislike=None):
		self.like = like # Int
		self.dislike = dislike # Int

	@staticmethod
	def generate(source):
		if source is None or type(source) is str and len(source) is 0:
			return CommentInteraction()

		return CommentInteraction(source['like'], source['dislike'])
