#!/usr/bin/env python3

from PyFloatplane import FloatplaneClient
from basicFunctions import showCreator, showVideo, showCreatorPlaylists

# logging.basicConfig(format=LOG_FORMAT, level=0)

try:
    client = FloatplaneClient()
    username, password = client.loadCredentials()
    loggedInUser = client.login(username, password)
    if not loggedInUser:
        raise Exception('User login not valid')

    print('Searching for Edges ...')
    edgeInfo = client.getEdges()

    print('Searching for Creators ...')
    creators = client.getCreatorList()

    if creators is None:
        print('No creators creators found')
    else:
        for creator in creators:
            print('-> Found {}'.format(creator.title))

    print()

    print('Searching for Edge Endpoints ...')

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
    print()

    print('Searching for Subscriptions ...')
    subscriptions = client.getSubscriptions()
    if not subscriptions:
        print('No subscriptions found!')

        # Should fix timeouts for oauth logins
        print('Trying to reconnect account to forum')
        client.refreshUserConnection()
    else:
        for sub in subscriptions:
            print('Subscription: {} ({} {})'.format(sub.plan.title, sub.plan.price, sub.plan.currency))
            creators = client.getCreatorInfo(sub.creator.id)

            for creator in creators:
                print('\n----- Playlists -----')
                showCreatorPlaylists(client, creator)
                print('\n----- Videos -----')
                showCreator(client, creator, showVideoFunc=showVideo, displayDownloadLink=True, videoLimit=1)
                print('\n-----------------------------\n')

except KeyboardInterrupt:
    print()
    print('Aborted by Keystroke!')
