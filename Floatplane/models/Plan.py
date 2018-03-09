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
