def showVideoComments(client, video, limit=None):
    for comment in client.getVideoComments(video.guid, limit):
        print("    > {} +{} -{}:\n    {}".format(
            comment.user.username,
            comment.interactionCounts.like,
            comment.interactionCounts.dislike,
            comment.text.strip()
        ))

def showVideo(client, video, commentLimit=None, displayDownloadLink=False):
    try:
        print('Video: [{}] {}'.format(video.guid, video.title))
        print('ReleaseDate: {}'.format(client.getVideoInfo(video.guid).releaseDate.strftime("%d.%m.%Y %H:%M:%S")))
        if displayDownloadLink:
            print('Link: {}'.format(client.getVideoURL(video.guid)))

        showVideoComments(client, video, commentLimit)
    except Exception as e:
        print('Ignoring video')
        print(e)

def showCreator(client, creator, videoLimit=None, commentsPerVideo=None, resolveVideos=True, showVideoFunc=None):
    # print('Owner: {}'.format(client.getUser(creator.owner)))

    if not resolveVideos:
        return

    videos = client.getVideosByCreator(creator.id, limit=videoLimit)

    if videos is None:
        print('No videos found for creator {}'.format(creator.title))
    else:
        for video in videos:
            print()
            if showVideoFunc:
                showVideoFunc(client, video, commentLimit=commentsPerVideo)
