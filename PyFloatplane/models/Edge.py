from PyFloatplane.models.Client import Client
from PyFloatplane.models.EdgeServer import EdgeServer


class Edge:
    def __init__(self, client=None, edges=None):
        if type(client) is dict:
            client = Client.generate(client)

        self.client = client  # Client
        self.edges = []  # EdgeServer

        if edges and len(edges) > 0:
            for edge in edges:
                self.edges.append(EdgeServer.generate(edge))

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Edge()

        client = source['client'] if 'client' in source else None

        return Edge(client, source['edges'])
