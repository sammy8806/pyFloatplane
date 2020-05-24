from PyFloatplane.models.Image import Image


class StreamOfflineInfo:
    def __init__(self, title=None, description=None, thumbnail=None):
        if type(thumbnail) is dict:
            thumbnail = Image.generate(thumbnail)

        self.title = title
        self.description = description
        self.thumbnail = thumbnail

    @staticmethod
    def generate(source):
        return StreamOfflineInfo(
            title=source['title'],
            description=source['description'],
            thumbnail=source['thumbnail']
        )

    def __repr__(self):
        return '<StreamOfflineInfo title=\'{}\'>'.format(
            self.title
        )
