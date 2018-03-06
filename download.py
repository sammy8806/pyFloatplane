#!/usr/bin/env python3

from Floatplane import FloatplaneClient

client = FloatplaneClient()
username, password = client.loadCredentials()
loggedInUser = client.login(username, password)
if not loggedInUser:
	raise Exception('User login not valid')

def showVideoComments(video, limit=None):
	for comment in client.getVideoComments(video.guid, limit):
		print("    > {} +{} -{}:\n    {}".format(
			comment.user.username,
			comment.interactionCounts.like,
			comment.interactionCounts.dislike,
			comment.text.strip()
		))

def showVideo(video, commentLimit=None, displayDownloadLink=False):
	try:
		print('Video: [{}] {}'.format(video.guid, video.title))
		print('ReleaseDate: {}'.format(client.getVideoInfo(video.guid).releaseDate))
		if displayDownloadLink:
			print('Link: {}'.format(client.getVideoURL(video.guid)))

		showVideoComments(video, commentLimit)
	except Exception as e:
		print('Ignoring video')
		print(e)

def showCreator(creator, videoLimit=None, commentsPerVideo=None, resolveVideos=True):
	# print('Owner: {}'.format(client.getUser(creator.owner)))

	if not resolveVideos:
		return

	videos = client.getVideosByCreator(creator.id, limit=videoLimit)

	if videos is None:
		print('No videos found for creator {}'.format(creator.title))
	else:
		for video in videos:
			print()
			showVideo(video, commentLimit=commentsPerVideo)

print('Searching for Creators ...')
creators = client.getCreatorList()

if creators is None:
	print('No creators creators found')
else:
	for creator in creators:
		print('-> Found {}'.format(creator.title))


print()

print('Searching for Subscriptions ...')
subscriptions = client.getSubscriptions()
if not subscriptions:
	print('No subscriptions found!')
else:
	for sub in subscriptions:
		print('Subscription: {} ({} {})'.format(sub.plan.title, sub.plan.price, sub.plan.currency))
		creators = client.getCreatorInfo(sub.creator.id)

		for creator in creators:
			showCreator(creator)
			print('\n-----------------------------\n')
