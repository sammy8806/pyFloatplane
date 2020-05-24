from PyFloatplane.models.User import User
from PyFloatplane.models.Image import Image
from PyFloatplane.models.LiveStream import LiveStream


class Creator:
    def __init__(self, id=None, owner=None, title=None, urlname=None,
                 description=None, about=None, cover=None, live_stream=None,
                 category=None, subscription_plan=None, discoverable=False,
                 subscriber_count_display='hide', income_display=False):
        if type(cover) is dict:
            cover = Image.generate(cover)

        if type(owner) is dict:
            owner = User.generate(owner)

        if type(live_stream) is dict:
            live_stream = LiveStream.generate(live_stream)

        self.id = id  # String : Id (Hash?)
        self.owner = owner  # String : Id (Hash?)
        self.title = title  # String
        self.urlname = urlname  # String : ShortTag
        self.description = description  # String
        self.about = about  # String : Description (Markdown?!)
        self.cover = cover  # Image
        self.live_stream = live_stream

        self.category = category  # String : Id

        self.subscription_plan = subscription_plan  # String[] ?
        self.discoverable = discoverable  # Boolean
        self.subscriber_count_display = subscriber_count_display  # String('hide')
        self.incomeDisplay = income_display  # Boolean

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Creator()

        if type(source) is str:
            return Creator(source)

        if 'coverImage' in source:
            coverImage = source['coverImage']
        else:
            coverImage = None

        if 'live_stream' in source:
            live_stream = source['live_stream']
        elif 'liveStream' in source:
            live_stream = source['liveStream']
        else:
            live_stream = None

        subscription_plan = source['subscriptionPlan'] if 'subscriptionPlan' in source else None
        discoverable = source['discoverable'] if 'discoverable' in source else None

        return Creator(
            id=source['id'],
            owner=source['owner'],
            title=source['title'],
            urlname=source['urlname'],
            description=source['description'],
            about=source['about'],
            cover=coverImage,
            live_stream=live_stream,
            category=source['category'],
            subscription_plan=subscription_plan,
            discoverable=discoverable,
            subscriber_count_display=source['subscriberCountDisplay'],
            income_display=source['incomeDisplay']
        )

    def __repr__(self):
        return '<Creator id=\'{}\' title=\'{}\'>'.format(
            self.id, self.title
        )
