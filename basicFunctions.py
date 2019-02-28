import logging

MAX_VIDEO_FETCH_COUNT = 20
log = logging.getLogger('Floatplane')

def showVideoComments(client, video, limit=None):
    for comment in client.getVideoComments(video.guid, limit):
        print("    > {} +{} -{}:\n    {}".format(
            comment.user.username,
            comment.interactionCounts.like,
            comment.interactionCounts.dislike,
            comment.text.strip()
        ))

        for comment in comment.replies:
            print("    |    > {} +{} -{}:\n    {}".format(
                comment.user.username,
                comment.interactionCounts.like,
                comment.interactionCounts.dislike,
                comment.text.strip()
            ))


def showVideo(client, video, commentLimit=None, displayDownloadLink=False, showRelatedVideos=False, showComments=False):
    try:
        print('Video: [{}] {}'.format(video.guid, video.title))
        print('ReleaseDate: {}'.format(client.getVideoInfo(video.guid).releaseDate.strftime("%d.%m.%Y %H:%M:%S")))
        if displayDownloadLink:
            print('Link: {}'.format(client.getDirectVideoURL(video.guid)))

        print('Related videos:')

        if showRelatedVideos:
            related = client.getReleatedVideos(video.guid)
            for vid in related:
                creator = client.getCreatorInfo(vid.creator.id)
                print('-> [{}][{}] {}'.format(creator[0].title, vid.guid, vid.title))

        print()

        if showComments:
            showVideoComments(client, video, commentLimit)
    except Exception as e:
        print('Ignoring video')
        print(e)


def showCreatorPlaylists(client, creator, playlistLimit=None, videosPerPlaylist=None):
    playlists = client.getCreatorPlaylists(creator, playlistLimit)

    if playlists is None:
        return

    for playlist in playlists:
        print('-> {}'.format(playlist.title))

        videos = client.getPlaylistVideos(playlist)

        if videos is None:
            continue

        for video in videos:
            print('--> [{}] {}'.format(video.guid, video.title))


def showCreator(client, creator, videoLimit=None, commentsPerVideo=None, resolveVideos=True, showVideoFunc=None,
                displayDownloadLink=False):
    # print('Owner: {}'.format(client.getUser(creator.owner)))

    if not resolveVideos:
        return

    videos = []
    skip_count = 0

    while skip_count < videoLimit:
        tmp_limit = videoLimit if videoLimit <= MAX_VIDEO_FETCH_COUNT else videoLimit - skip_count if videoLimit - skip_count <= MAX_VIDEO_FETCH_COUNT else MAX_VIDEO_FETCH_COUNT

        limit = None if skip_count > 0 and tmp_limit == MAX_VIDEO_FETCH_COUNT else tmp_limit
        log.info('Getting videos for {} {} -> {}'.format(creator.title, skip_count, skip_count + (limit if limit is not None else 0)))
        tmp_vids = client.getVideosByCreator(creator.id, limit=limit, fetch_after=skip_count)

        if len(tmp_vids) == 0:
            break

        for vid in tmp_vids:
            videos.append(vid)

        skip_count = skip_count + len(tmp_vids)

    if videos is None:
        print('No videos found for creator {}'.format(creator.title))
    else:
        for video in videos:
            print()
            if showVideoFunc:
                showVideoFunc(client, video, creator=creator, commentLimit=commentsPerVideo, displayDownloadLink=displayDownloadLink)


def showEdgeSelection(client):
    edgeInfo = client.getEdges()
    print('Found {} Edges'.format(len(edgeInfo.edges)))

    for edge in edgeInfo.edges:
        print(
            '-> [{}-{}] {} BW:{}GBit/s Download:{} Stream:{}'.format(edge.datacenter.country_code,
                                                                     edge.datacenter.region_code,
                                                                     edge.hostname, edge.bandwidth / 1000 / 1000 / 1000,
                                                                     edge.allowDownload, edge.allowStreaming))

    selected_edge = client.getTargetEdgeServer()

    print()
    print('=> Selected Edge: {}'.format(selected_edge.hostname))
