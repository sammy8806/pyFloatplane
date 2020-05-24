class Plan:
	def __init__(self, id = None, title=None, description=None, price=0.0, price_yearly=0.0,
				 currency=None, interval=None, intervalCount=0, logo=None):
		#if type(logo) is dict:
			#logo = Logo.generate(logo)

		self.id = id # String
		self.title = title # String
		self.description = description # String
		self.price = price # Double
		self.priceYearly = price_yearly # Double
		self.currency = currency # String [cad, usd?, eur?]
		self.interval = interval # String [month, year?]
		self.intervalCount = intervalCount # Int // Every x months ? // Deprecated?
		self.logo = logo # null?

	@staticmethod
	def generate(source):
		if source is None or len(source) == 0:
			return Plan()

		id = source['id'] if 'id' in source else None
		price_yearly = source['priceYearly'] if 'priceYearly' in source else 0.0
		interval_count = source['intervalCount'] if 'intervalCount' in source else None

		return Plan(
			id=id,
			title=source['title'],
			description=source['description'],
			price=source['price'],
			price_yearly=price_yearly,
			currency=source['currency'],
			interval=source['interval'],
			intervalCount=interval_count,
			logo=source['logo']
		)
