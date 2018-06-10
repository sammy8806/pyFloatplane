from PyFloatplane.models.User import User
from PyFloatplane.models.Video import Video
from PyFloatplane.models.CommentInteraction import CommentInteraction


class Comment:
    def __init__(self, id=None, user=None, video=None, text=None, replying=None, postDate=None,
                 editDate=None, interactions=[], replies=[], interactionCounts={}):
        if type(user) is dict or type(user) is str or user is None:
            user = User.generate(user)

        if type(video) is dict or type(video) is str or video is None:
            video = Video.generate(video)

        if type(interactionCounts) is dict or type(interactionCounts) is str or interactionCounts is None:
            interactionCounts = CommentInteraction.generate(interactionCounts)

        if type(replies) is list and len(replies) > 0:
            user_replies = []
            for reply in replies:
                user_replies.append(Comment.generate(reply))
            replies = user_replies

        self.id = id  # String : Id (Hash?)
        self.user = user  # User
        self.video = video  # Video
        self.text = text  # String
        self.replying = replying  # String
        self.postDate = postDate  # IsoTimestamp
        self.editDate = editDate  # IsoTimestamp
        self.interactions = interactions  # ?
        self.replies = replies  # [Comment]
        self.interactionCounts = interactionCounts  # CommentInteraction

    @staticmethod
    def generate(source):
        if source is None or len(source) is 0:
            return Comment()

        interactions = source['interactions'] if 'interactions' in source else []
        replies = source['replies'] if 'replies' in source else []

        return Comment(
            source['id'], source['user'], source['video'], source['text'], source['replying'],
            source['postDate'], source['editDate'], interactions, replies,
            source['interactionCounts']
        )
