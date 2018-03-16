class EdgeDatacenter:
	def __init__(self, country_code=None, region_code=None, latitude=None, longitude=None):
		self.country_code = None # String : [CA, FR, AU]
		self.region_code = None # String : [QC, A, NSW]
		self.latitude = None # Float
		self.longitude = None # Float

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return EdgeDatacenter()
		
		return EdgeDatacenter(source['countryCode'], source['regionCode'], source['latitude'], source['longitude'])
