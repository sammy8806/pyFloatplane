class Client:
	def __init__(self):
		self.ip = None # String : IPv4/IPv6
		self.country_code = None # String : [US]
		self.country_name = None # String : [United State]
		self.region_code = None # String ?
		self.region_name = None # String ?
		self.city = None # String ?
		self.zip_code = None # String ?
		self.time_zone = None # String ?
		self.latitude = 0.0 # Double
		self.longitude = 0.0 # Double
		self.metro_code = 0 # Int ?
