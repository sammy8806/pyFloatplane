class UserConnection:
	def __init__(self, key=None, name=None, enabled=False, connected=False, connectedAccount=None):
		self.key = key # String [ltt]
		self.name = name # String
		self.enabled = enabled # Bool
		self.connected = connected # Bool
		self.connectedAccount = connectedAccount # ???
