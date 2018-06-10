import dateutil.parser

from PyFloatplane.models.Creator import Creator
from PyFloatplane.models.Image import Image


class Video:
    def __init__(self, title=None, guid=None, tags=[], description=None, private=False,
                 releaseDate=None, duration=0, creator=None, thumbnail=None, relatedVideos=[]):

        if type(creator) is dict or type(creator) is str or creator is None:
            creator = Creator.generate(creator)

        if type(thumbnail) is dict or thumbnail is None:
            thumbnail = Image.generate(thumbnail)

        self.title = title  # String
        self.guid = guid  # String : NoGUID!
        self.tags = tags  # String[]
        self.description = description  # String?
        self.private = private  # Bool
        self.duration = duration  # Int? : Seconds?
        self.creator = creator  # Creator
        self.thumbnail = thumbnail  # Thumbnail
        self.relatedVideos = relatedVideos  # Videos

        if releaseDate:
            self.releaseDate = dateutil.parser.parse(releaseDate)  # IsoTimestamp

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Video()

        if type(source) is str and len(source) > 0:
            return Video(title=source)

        tags = source['tags'] if 'tags' in source else []

        return Video(
            source['title'], source['guid'], tags, source['description'], source['private'],
            source['releaseDate'], source['duration'], source['creator'], source['thumbnail']
        )
