import dateutil.parser

from PyFloatplane.models.Creator import Creator
from PyFloatplane.models.Image import Image
from PyFloatplane.models.Subscription import Subscription


class Video:
    def __init__(self, title=None, guid=None, tags=[], description=None, private=False,
                 releaseDate=None, duration=0, creator=None, thumbnail=None, relatedVideos=[],
                 subscription_permissions=[]):

        if type(creator) is dict or type(creator) is str or creator is None:
            creator = Creator.generate(creator)

        if type(thumbnail) is dict or thumbnail is None:
            thumbnail = Image.generate(thumbnail)

        #if type(subscription_permissions) is list and len(subscription_permissions) > 0:
            #subscription_permissions = [Subscription.generate(sub_id) for sub_id in subscription_permissions]

        self.title = title  # String
        self.guid = guid  # String : NoGUID!
        self.tags = tags  # String[]
        self.description = description  # String?
        self.private = private  # Bool
        self.duration = duration  # Int? : Seconds?
        self.creator = creator  # Creator
        self.thumbnail = thumbnail  # Thumbnail
        self.relatedVideos = relatedVideos  # Videos
        self.subscriptionPermissions = subscription_permissions  # Creator[]

        if releaseDate:
            self.releaseDate = dateutil.parser.parse(releaseDate)  # IsoTimestamp

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Video()

        if type(source) is str and len(source) > 0:
            return Video(title=source)

        tags = source['tags'] if 'tags' in source else []
        subscription_permissions = source['subscriptionPermissions'] if 'subscriptionPermissions' in source else []

        return Video(
            title=source['title'],
            guid=source['guid'],
            tags=tags,
            description=source['description'],
            private=source['private'],
            releaseDate=source['releaseDate'],
            duration=source['duration'],
            creator=source['creator'],
            thumbnail=source['thumbnail'],
            subscription_permissions=subscription_permissions
        )
