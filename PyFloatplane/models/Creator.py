from PyFloatplane.models.User import User
from PyFloatplane.models.Image import Image
from PyFloatplane.models.LiveStream import LiveStream


class Creator:
    def __init__(self, id=None, owner=None, title=None, urlname=None,
                 description=None, about=None, cover=None, icon=None, live_stream=None,
                 category=None, discoverable=False, subscriber_count_display='hide',
                 income_display=False):
        if type(cover) is dict:
            cover = Image.generate(cover)

        if type(icon) is dict:
            icon = Image.generate(icon)

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
        self.icon = icon  # Image
        self.live_stream = live_stream

        self.category = category  # String : Id

        self.discoverable = discoverable  # Boolean
        self.subscriber_count_display = subscriber_count_display  # ['hide', ?'show'?]
        self.income_display = income_display

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Creator()

        if type(source) is str:
            return Creator(source)

        if 'coverImage' in source:
            coverImage = source['coverImage']
        elif 'cover' in source:
            coverImage = source['cover']
        else:
            coverImage = None

        if 'live_stream' in source:
            live_stream = source['live_stream']
        elif 'liveStream' in source:
            live_stream = source['liveStream']
        else:
            live_stream = None

        creator = Creator(
            id=source['id'],
            owner=source['owner'],
            title=source['title'],
            urlname=source['urlname'],
            description=source['description'],
            about=source['about'],
            cover=coverImage,
            icon=source['icon'],
            live_stream=live_stream,
            category=source['category'],
        )

        if 'incomeDisplay' in source:
            setattr(creator, 'income_display', source['incomeDisplay'])

        if 'subscriberCountDisplay' in source:
            setattr(creator, 'subscriber_count_display', source['subscriberCountDisplay'])

        if 'discoverable' in source:
            setattr(creator, 'discoverable', source['discoverable'])

        return creator

    def __repr__(self):
        return '<Creator id=\'{}\' title=\'{}\'>'.format(
            self.id, self.title
        )
