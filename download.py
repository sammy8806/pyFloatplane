#!/usr/bin/env python3

from Floatplane import FloatplaneClient

client = FloatplaneClient()
username, password = client.loadCredentials()
loggedInUser = client.login(username, password)
if not loggedInUser:
	raise Exception('User login not valid')

def showVideo(video):
	try:
		print('Video: [{}] {}'.format(video.guid, video.title))
		print('ReleaseDate: {}'.format(client.getVideoInfo(video.guid).releaseDate))
		#print('Link: {}'.format(client.getVideoLink(video.guid)))

		for comment in client.getVideoComments(video.guid):
			print("    > {} +{} -{}:\n    {}".format(
				comment.user.username,
				comment.interactionCounts.like,
				comment.interactionCounts.dislike,
				comment.text.strip()
			))
	except Exception:
		print('Ignoring video')

def showCreator(creator):
	print('Owner: {}'.format(client.getUser(creator.owner)))

	videos = client.getVideosByCreator(creator.id, limit=3)

	if videos is None:
		print('No videos found for creator {}'.format(creator.title))
	else:
		for video in videos:
			print()
			showVideo(video)

creators = client.getCreatorList()

if creators is None:
	print('No creators creators found')
else:
	for creator in creators:
		print('-> Found {}'.format(creator.title))

		showCreator(creator)
		print()

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
