class Plan:
    def __init__(self, id=None, title=None, description=None, price=0.0, priceYearly=0.0,
                 currency=None, interval=None, intervalCount=0, logo=None):
        # if type(logo) is dict:
        # logo = Logo.generate(logo)

        self.id = id  # String
        self.title = title  # String
        self.description = description  # String
        self.price = price  # Double
        self.priceYearly = priceYearly  # Double
        self.currency = currency  # String [cad, usd?, eur?]
        self.interval = interval  # String [month, year?]
        self.intervalCount = intervalCount  # Int // Every x months ? // Deprecated?
        self.logo = logo  # null?

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Plan()

        plan = Plan()

        for attr in source:
            setattr(plan, attr, source[attr])

        return plan
