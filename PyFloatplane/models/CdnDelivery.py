from PyFloatplane.models.Client import Client
from PyFloatplane.models.EdgeServer import EdgeServer


class CdnDeliveryQualityLevel:

    def __init__(self, name=None, width=None, height=None, order=None, label=None):
        self.name = name  # String
        self.width = width  # Int
        self.height = height  # Int
        self.order = order  # Int
        self.label = label  # String

    @staticmethod
    def generate(source):
        if source is None:
            return CdnDeliveryQualityLevel()

        return CdnDeliveryQualityLevel(source['name'], source['width'], source['height'], source['order'],
                                       source['label'])


class CdnDeliveryResourceData:
    def __init__(self, quality_levels=None, token=None):
        self.qualityLevels = []  # CdnDeliveryQualityLevel
        self.token = token  # String

        if quality_levels and len(quality_levels) > 0:
            for level in quality_levels:
                self.qualityLevels.append(CdnDeliveryQualityLevel.generate(level))

    @staticmethod
    def generate(source):
        if source is None:
            return CdnDeliveryResourceData()

        return CdnDeliveryResourceData(source['qualityLevels'], source['token'])


class CdnDeliveryResource:
    def __init__(self, uri=None, data=None):
        if type(data) is dict:
            data = CdnDeliveryResourceData.generate(data)

        self.uri = uri  # String
        self.data = data  # CdnDeliveryResourceData

    @staticmethod
    def generate(source):
        if source is None:
            return CdnDeliveryResource()

        return CdnDeliveryResource(source['uri'], source['data'])


class CdnDelivery:
    def __init__(self, client=None, edges=None, strategy=None, resource=None):
        if type(client) is dict:
            client = Client.generate(client)

        if type(resource) is dict:
            resource = CdnDeliveryResource.generate(resource)

        self.client = client  # Client TODO: Deprecated?
        self.edges = []  # EdgeServer
        self.strategy = strategy  # String : [client]
        self.resource = resource  # CdnDeliveryResource

        if edges and len(edges) > 0:
            for edge in edges:
                self.edges.append(EdgeServer.generate(edge))

        if resource:
            self.resource = resource

    @staticmethod
    def generate(source):
        if source is None:
            return CdnDelivery()

        client = source['client'] if 'client' in source else None

        return CdnDelivery(client, source['edges'], source['strategy'], source['resource'])
