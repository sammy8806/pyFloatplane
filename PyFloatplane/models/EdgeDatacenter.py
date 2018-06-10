class EdgeDatacenter:
    def __init__(self, country_code=None, region_code=None, latitude=None, longitude=None):
        self.country_code = country_code  # String : [CA, FR, AU]
        self.region_code = region_code  # String : [QC, A, NSW]
        self.latitude = latitude  # Float
        self.longitude = longitude  # Float

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return EdgeDatacenter()

        return EdgeDatacenter(source['countryCode'], source['regionCode'], source['latitude'], source['longitude'])

    def __repr__(self):
        return '<EdgeDatacenter countryCode=\'{}\' region_code=\'{}\' latitude=\'{}\' longitude=\'{}\'>'.format(
            self.country_code, self.region_code, self.latitude, self.longitude
        )
