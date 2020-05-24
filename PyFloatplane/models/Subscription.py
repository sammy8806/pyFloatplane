import logging

from PyFloatplane.models.Creator import Creator
from PyFloatplane.models.Plan import Plan

log = logging.getLogger('Floatplane.models.Subscription')


class Subscription:
    def __init__(self, start_date=None, end_date=None, payment_id=None,
                 interval=None, payment_cancelled=None, plan={}, creator={}):
        if type(creator) is dict or type(creator) is str or creator is None:
            creator = Creator.generate(creator)

        if type(plan) is dict or plan is None:
            plan = Plan.generate(plan)

        self.startDate = start_date  # IsoTimestamp
        self.endDate = end_date  # IsoTimestamp
        self.payment_id = payment_id  # Int
        self.interval = interval  # String (month, year)
        self.payment_cancelled = payment_cancelled # bool
        self.plan = plan  # Subscription Plan
        self.creator = creator  # Creator

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Subscription()
        try:
            return Subscription(
                start_date=source['startDate'],
                end_date=source['endDate'],
                payment_id=source['paymentID'],
                interval=source['interval'],
                payment_cancelled=source['paymentCancelled'],
                plan=source['plan'],
                creator=source['creator']
            )
        except Exception as e:
            log.error(e)
