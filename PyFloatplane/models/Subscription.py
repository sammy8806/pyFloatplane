import logging

from PyFloatplane.models.Creator import Creator
from PyFloatplane.models.Plan import Plan

log = logging.getLogger('Floatplane.models.Subscription')

class Subscription:
	def __init__(self, startDate=None, endDate=None, plan={}, creator={}):
		if type(creator) is dict or type(creator) is str or creator is None:
			creator = Creator.generate(creator)

		if type(plan) is dict or plan is None:
			plan = Plan.generate(plan)

		self.startDate = startDate # IsoTimestamp
		self.endDate = endDate # IsoTimestamp
		self.plan = plan # Subscription Plan
		self.creator = creator # Creator

	@staticmethod
	def generate(source):
		if source is None or len(source) is 0:
			return Subscription()
		try:
			return Subscription(source['startDate'], source['endDate'], source['plan'], source['creator'])
		except Exception as e:
			log.error(e)
