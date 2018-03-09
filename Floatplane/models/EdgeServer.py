class EdgeServer:
	def __init__(self):
		self.hostname = None # String
		self.queryPort = 0 # Int : Port
		self.bandwith = 0 # Long : in kbit?
		self.allowDownload = False # Boolean
		self.allowStreaming = False # Boolean (Live-Streaming?)
		self.datacenter = None # EdgeDatacenter
