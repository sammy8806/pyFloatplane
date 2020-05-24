import dateutil.parser

from PyFloatplane.models.Subscription import Subscription
from PyFloatplane.models.Creator import Creator
from PyFloatplane.models.Image import Image


class Video:
    def __init__(self, title=None, guid=None, tags=[], description=None, private=False,
                 releaseDate=None, duration=0, creator=None, thumbnail=None, relatedVideos=[],
                 subscription_permissions=[], has_access=None):

        if type(creator) is dict or type(creator) is str or creator is None:
            creator = Creator.generate(creator)

        if type(thumbnail) is dict or thumbnail is None:
            thumbnail = Image.generate(thumbnail)

        self.title = title  # String
        self.guid = guid  # String : NoGUID!
        self.tags = tags  # String[] @Deprecated
        self.description = description  # String?
        self.private = private  # Bool
        self.duration = duration  # Int? : Seconds?
        self.creator = creator  # Creator
        self.thumbnail = thumbnail  # Thumbnail
        self.relatedVideos = relatedVideos  # Videos
        self.has_access = has_access

        if releaseDate:
            self.releaseDate = dateutil.parser.parse(releaseDate)  # IsoTimestamp

        if subscription_permissions:
            self.subscription_permissions = []  # Subscription[]
            for sub in subscription_permissions:
                self.subscription_permissions.append(Subscription.generate(sub))

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Video()

        if type(source) is str and len(source) > 0:
            return Video(title=source)

        tags = source['tags'] if 'tags' in source else []

        video = Video(
            title=source['title'],
            guid=source['guid'],
            tags=tags,
            description=source['description'],
            releaseDate=source['releaseDate'] if 'releaseDate' in source else None,
            private=source['private'],
            duration=source['duration'],
            creator=source['creator'],
            thumbnail=source['thumbnail'],
            subscription_permissions=source['subscriptionPermissions'] if 'subscriptionPermissions' in source else [],
        )

        if 'hasAccess' in source:
            setattr(video, 'hasAccess', source['hasAccess'])

        return video
