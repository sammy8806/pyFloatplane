#!/usr/bin/env python3

from PyFloatplane import FloatplaneClient

client = FloatplaneClient()

username, password = client.loadCredentials()

loggedInUser = client.login(username, password)
if not loggedInUser:
    raise Exception('User login not valid')

subscriptions = client.getSubscriptions()

commentGUID = '5a6e4ffd55bff97725c7c6a0'
client.deleteVideoComment(commentGUID)
# client.postCommentReaction(commentGUID, 'dislike')
# client.clearCommentReaction(commentGUID, None)
