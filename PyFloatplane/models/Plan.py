class Plan:
    def __init__(self, id=None, title=None, description=None, price=0.0, priceYearly=0.0, currency=None,
                 interval=None, intervalCount=0, logo=None):

        self.id = id
        self.title = title  # String
        self.description = description  # String
        self.price = price  # Double
        self.priceYearly = float(priceYearly)  # Double
        self.currency = currency  # String [cad, usd?, eur?]
        self.interval = interval  # String [month, year?]
        self.intervalCount = intervalCount  # Int // Every x months ?
        self.logo = logo  # null?

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Plan()

        plan = Plan()

        for attr in source:
            setattr(plan, attr, source[attr])

        return plan
