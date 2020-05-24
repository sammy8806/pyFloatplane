class Client:
    def __init__(self, ip=None, country_code=None, country_name=None, region_code=None, region_name=None,
                 city=None, zip_code=None, time_zone=None, latitude=0.0, longitude=0.0, metro_code=0):
        self.ip = ip  # String : IPv4/IPv6
        self.country_code = country_code  # String : [DE]
        self.country_name = country_name  # String : [Germany]
        self.region_code = region_code  # String : [HH]
        self.region_name = region_name  # String : [Hamburg]
        self.city = city  # String : [Hamburg]
        self.zip_code = zip_code  # String : [22303]
        self.time_zone = time_zone  # String : [Europe/Berlin]
        self.latitude = latitude  # Double : [53.5844]
        self.longitude = longitude  # Double : [10.0288]
        self.metro_code = metro_code  # Int ?

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Client()

        return Client(ip=source['ip'], country_code=source['country_code'], country_name=source['country_name'],
                      region_code=source['region_code'], region_name=source['region_name'], city=source['city'],
                      zip_code=source['zip_code'], time_zone=source['time_zone'], latitude=source['latitude'],
                      longitude=source['longitude'], metro_code=source['metro_code'])
