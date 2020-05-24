from PyFloatplane.models.User import User
from PyFloatplane.models.Video import Video
from PyFloatplane.models.CommentInteraction import CommentInteraction


class Comment:
    def __init__(self, id=None, user=None, video=None, text=None, replying=None, postDate=None,
                 editDate=None, interactions=[], replies=[], interactionCounts={}, totalReplies=None):
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
        self.interactions = interactions  # TODO: Deprecated?
        self.replies = replies  # [Comment]
        self.interactionCounts = interactionCounts  # CommentInteraction
        self.totalReplies = totalReplies  # Int // TODO: Not working yet?

    @staticmethod
    def generate(source):
        if source is None or len(source) == 0:
            return Comment()

        interactions = source['interactions'] if 'interactions' in source else []
        replies = source['replies'] if 'replies' in source else []

        return Comment(
            id=source['id'],
            user=source['user'],
            video=source['video'],
            text=source['text'],
            replying=source['replying'],
            postDate=source['postDate'],
            editDate=source['editDate'],
            interactions=interactions,
            replies=replies,
            interactionCounts=source['interactionCounts'],
            totalReplies=source['totalReplies']
        )
