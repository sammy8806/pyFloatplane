from PyFloatplane.models.EdgeDatacenter import EdgeDatacenter


class EdgeServer:
    def __init__(self, hostname=None, queryPort=0, bandwidth=0, allowDownload=False, allowStreaming=False,
                 datacenter=None):
        self.hostname = hostname  # String
        self.queryPort = queryPort  # Int : Port
        self.bandwidth = bandwidth  # Long : in kbit?
        self.allowDownload = allowDownload  # Boolean
        self.allowStreaming = allowStreaming  # Boolean (Live-Streaming?)
        self.datacenter = datacenter  # EdgeDatacenter

        if datacenter:
            self.datacenter = datacenter if type(datacenter) is EdgeDatacenter else EdgeDatacenter.generate(datacenter)

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return EdgeServer()

        return EdgeServer(
            source['hostname'], source['queryPort'], source['bandwidth'], source['allowDownload'],
            source['allowStreaming'], source['datacenter']
        )

    def __repr__(self):
        return '<EdgeServer hostname=\'{}\' queryPort=\'{}\' bandwith=\'{} GBit\' allowStream=\'{}\' allowDl=\'{}\'>'.format(
            self.hostname, self.queryPort, self.bandwidth / 1000 / 1000 / 1000, self.allowStreaming, self.allowDownload
        )
