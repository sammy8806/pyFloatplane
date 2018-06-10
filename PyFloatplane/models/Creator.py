from PyFloatplane.models.User import User
from PyFloatplane.models.Image import Image


class Creator:
    def __init__(self, id=None, owner=None, title=None, urlname=None,
                 description=None, about=None, cover=None, category=None):
        if type(cover) is dict:
            cover = Image.generate(cover)

        if type(owner) is dict:
            owner = User.generate(owner)

        self.id = id  # String : Id (Hash?)
        self.owner = owner  # String : Id (Hash?)
        self.title = title  # String
        self.urlname = urlname  # String : ShortTag
        self.description = description  # String
        self.about = about  # String : Description (Markdown?!)
        self.cover = cover  # Image

        self.category = category  # String : Id

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Creator()

        if type(source) is str:
            return Creator(source)

        if 'coverImage' in source:
            coverImage = source['coverImage']
        else:
            coverImage = None

        return Creator(
            source['id'], source['owner'], source['title'], source['urlname'],
            source['description'], source['about'], coverImage, source['category']
        )

    def __repr__(self):
        return '<Creator id=\'{}\' title=\'{}\'>'.format(
            self.id, self.title
        )
