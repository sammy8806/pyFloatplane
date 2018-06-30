class Client:
    def __init__(self, ip=None, country_code=None, country_name=None, region_code=None, region_name=None,
                 city=None, zip_code=None, time_zone=None, latitude = 0.0, longitude=0.0, metro_code=0):
        self.ip = ip  # String : IPv4/IPv6
        self.country_code = country_code  # String : [US]
        self.country_name = country_name  # String : [United State]
        self.region_code = region_code  # String ?
        self.region_name = region_name  # String ?
        self.city = city  # String ?
        self.zip_code = zip_code  # String ?
        self.time_zone = time_zone  # String ?
        self.latitude = latitude  # Double
        self.longitude = longitude  # Double
        self.metro_code = metro_code  # Int ?

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Client()

        return Client(ip=source['ip'], country_code=source['country_code'], country_name=source['country_name'],
                      region_code=source['region_code'], region_name=source['region_name'], city=source['city'],
                      zip_code=source['zip_code'], time_zone=source['time_zone'], latitude=source['latitude'],
                      longitude=source['longitude'], metro_code=source['metro_code'])
