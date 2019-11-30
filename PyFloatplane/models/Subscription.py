import logging

from PyFloatplane.models.Creator import Creator
from PyFloatplane.models.Plan import Plan

log = logging.getLogger('Floatplane.models.Subscription')


class Subscription:
    def __init__(self, startDate=None, endDate=None, plan={}, creator={}, subscription_id=None):
        if type(creator) is dict or type(creator) is str or creator is None:
            creator = Creator.generate(creator)

        if type(plan) is dict or plan is None:
            plan = Plan.generate(plan)

        self.subscription_id = subscription_id  # String
        self.startDate = startDate  # IsoTimestamp
        self.endDate = endDate  # IsoTimestamp
        self.plan = plan  # Subscription Plan
        self.creator = creator  # Creator

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Subscription()

        if type(source) is str and len(source) > 0:
            return Subscription(subscription_id=source)

        try:
            sub = Subscription(source['startDate'], source['endDate'], source['plan'], source['creator'])

            for field in ['paymentID', 'interval', 'paymentCancelled']:
                if field in source:
                    setattr(sub, field, source[field])
            return sub

        except Exception as e:
            log.error(e)
