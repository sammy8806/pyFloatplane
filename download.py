#!/usr/bin/env python3

from __future__ import unicode_literals

import configparser
import logging
import os

import requests

from PyFloatplane import FloatplaneClient
from basicFunctions import showCreator, showVideo, showCreatorPlaylists, showEdgeSelection

import youtube_dl

log = logging.getLogger('Floatplane')


def read_dl_config(filename = 'floatplane-dl.ini', path = '.'):
    try:
        config = configparser.ConfigParser()
        config.read('{}/{}'.format(path, filename))

        if 'download' in config:
            return config['download']

    except Exception as e:
        log.warning('Could not read config: {}'.format(e))

    return dict()


# logging.basicConfig(format=LOG_FORMAT, level=0)

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_progress_hook(d):
    if d['status'] == 'downloading':
        print('[{}] {} / {:.2f} MB'.format(
            d['filename'], d['_percent_str'], d['total_bytes']/1024/1024)
        )

    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_thumbnail(client, video, file_name):
    if video.thumbnail is None:
        log.debug('No Thumbnail seems attached to {} ... skipping'.format(video.guid))
        return

    if os.path.isfile(file_name):
        log.warning('Thumbnail already exists ... archiving and redownloading it')

        dl_try = 1
        while os.path.isfile('{}.{}'.format(file_name, dl_try)):
            dl_try = dl_try + 1

        os.rename(file_name, '{}.{}'.format(file_name, dl_try))

    log.debug('Downloading Thumbnail for {}'.format(video.guid))

    thumb = requests.get(video.thumbnail.path)

    if thumb.status_code >= 300:
        log.warning('Thumbnail returned HTTP {} ... skipping'.format(thumb.status_code))

    with open(file_name, 'wb') as f:
        f.write(thumb.content)

    log.debug('Thumbnail successfully downloaded')


def download_video(client, video, commentLimit=None, displayDownloadLink=None):
    showVideo(client, video, 0, False)

    cfg_subfolder = 'creator_subfolder'
    cfg_path = 'target_path'
    cfg_perm = 'target_path_permissions'

    config = read_dl_config()
    dl_dir = config[cfg_path] if cfg_path in config else 'download'

    val_subfolder = config[cfg_subfolder].strip().lower()
    if val_subfolder == 'true' or val_subfolder == '1':
        creator = client.getCreatorInfo(video.creator.id)
        creator_short = creator[0].urlname
        dl_dir = '{}/{}'.format(dl_dir, creator_short)

    if not os.path.isdir(dl_dir):
        dl_perms = int(config[cfg_perm], base=8) if cfg_perm in config else 0o755
        os.mkdir(dl_dir, dl_perms)

    download_url = client.getDirectVideoURL(video.guid)
    creator = client.getCreatorInfo(video.creator.id)[0]

    basename = '{}-{}-{}'.format(video.guid, creator.title, video.title)
    output_template = '{}/{}.mp4'.format(dl_dir, basename)
    thumbnail_template = '{}/{}.png'.format(dl_dir, basename)

    if os.path.exists(output_template):
        print('This video is already downloaded ... skipping')
        return

    if os.path.exists('{}.part'.format(output_template)):
        print('Download seems to be interrupted ... continuing')

    print('Downloading Video from: {} to {}'.format(download_url, dl_dir))

    download_thumbnail(client, video, thumbnail_template)

    ydl_opts = {
        'format': 'bestaudio/best',
        'call_home': False,
        'outtmpl': output_template,
        'continue_dl': True,
        'writeinfojson': True,
        #'postprocessors': [{
            # 'key': 'FFmpegExtractAudio',
            # 'preferredcodec': 'mp3',
            # 'preferredquality': '192',
        #}],
        'logger': MyLogger(),
        'progress_hooks': [download_progress_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([download_url])


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
    showEdgeSelection(client)
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
                showCreator(client, creator, showVideoFunc=download_video, displayDownloadLink=True, videoLimit=1)
                print('\n-----------------------------\n')

except KeyboardInterrupt:
    print()
    print('Aborted by Keystroke!')
