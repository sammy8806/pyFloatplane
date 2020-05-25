#!/usr/bin/env python3

from __future__ import unicode_literals

import configparser
import logging
import os

import requests

from PyFloatplane import FloatplaneClient
from basicFunctions import showCreator, showVideo, showCreatorPlaylists, showEdgeSelection

import youtube_dl
import sentry_sdk

log = logging.getLogger('Floatplane')

cfg_subfolder = 'creator_subfolder'
cfg_path = 'target_path'
cfg_dir_perm = 'target_path_permissions'
cfg_file_perm = 'dl_file_permissions'
cfg_video_limit = 'video_count'

NT_ILLEGAL_CHARS = '<>:"/\\|*?'


def read_dl_config(filename='floatplane.ini', path='.'):
    try:
        config = configparser.ConfigParser()
        config.read('{}/{}'.format(path, filename))

        if 'sentry' in config:
            dsn=config['sentry']['dsn']
            sentry_sdk.init(dsn=dsn)

        if 'download' in config:
            return config['download']

    except Exception as e:
        log.warning('Could not read config: {}'.format(e))

    return dict()


# logging.basicConfig(format=LOG_FORMAT, level=0)
# logging.basicConfig(level=0)

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
            d['filename'], d['_percent_str'], d['total_bytes'] / 1024 / 1024)
        )

    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_thumbnail(client, video, file_name, perm=0o775):
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

    os.chmod(file_name, perm)

    log.debug('Thumbnail successfully downloaded')


def download_video(client, video, commentLimit=None, displayDownloadLink=None, creator=None):
    showVideo(client, video, 0, False)

    dl_dir = dl_config[cfg_path] if cfg_path in dl_config else 'download'
    dl_dir_perms = int(dl_config[cfg_dir_perm], base=8) if cfg_dir_perm in dl_config else 0o755
    dl_file_perms = int(dl_config[cfg_file_perm], base=8) if cfg_file_perm in dl_config else 0o644

    if creator is None:
        creator = client.getCreatorInfo(video.creator.id)[0]

    val_subfolder = dl_config[cfg_subfolder].strip().lower()
    if val_subfolder == 'true' or val_subfolder == '1':
        creator_short = creator.urlname
        dl_dir = '{}/{}'.format(dl_dir, creator_short)

    if not os.path.isdir(dl_dir):
        os.makedirs(dl_dir, mode=dl_dir_perms, exist_ok=True)

    ending_video = 'mp4'
    ending_thumb = 'png'
    ending_info = 'info.json'
    basename = '{}-{}-{}'.format(video.guid, creator.title, video.title)

    if os.name == 'nt':

        # Avoiding NTFS alternative file streams
        for char in NT_ILLEGAL_CHARS:
            basename = basename.replace(char, '')

    output_template = '{}/{}.{}'.format(dl_dir, basename, ending_video)
    thumbnail_template = '{}/{}.{}'.format(dl_dir, basename, ending_thumb)

    if os.path.exists(output_template):
        print('This video is already downloaded ... skipping')

        for ending in [ending_video, ending_info, ending_thumb]:
            f_name = '{}/{}.{}'.format(dl_dir, basename, ending)
            if os.path.isfile(f_name):
                os.chmod(f_name, dl_file_perms)

        return

    if os.path.exists('{}.part'.format(output_template)):
        print('Download seems to be interrupted ... continuing')

    try:
        download_url = client.getDirectVideoURL(video.guid)
        print('Downloading Video from: {} to {}'.format(download_url, dl_dir))

        download_thumbnail(client, video, thumbnail_template, perm=dl_file_perms)

        ydl_opts = {
            'format': 'bestaudio/best',
            'call_home': False,
            'outtmpl': output_template,
            'continue_dl': True,
            # 'writeinfojson': True,
            # 'postprocessors': [{
            # 'key': 'FFmpegExtractAudio',
            # 'preferredcodec': 'mp3',
            # 'preferredquality': '192',
            # }],
            'logger': MyLogger(),
            'progress_hooks': [download_progress_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([download_url])

            for ending in [ending_video, ending_info]:
                f_name = '{}/{}.{}'.format(dl_dir, basename, ending)
                if os.path.isfile(f_name):
                    os.chmod(f_name, dl_file_perms)
    except Exception as err:
        print('Download Failed!: {}', err)
        sentry_sdk.capture_exception(err)

try:
    print('Reading Config ...')
    dl_config = read_dl_config()
    video_limit = int(dl_config[cfg_video_limit]) if cfg_video_limit in dl_config else 5

    client = FloatplaneClient()
    username, password = client.loadCredentials()

    print('Logging in as "{}"'.format(username))
    loggedInUser = client.login(username, password)
    if not loggedInUser:
        raise Exception('User login not valid')
    print('Successfully logged in')

    print('Searching for Edges ...')
    edgeInfo = client.getEdges()

    print('Searching for Creators ...')
    creators = client.getCreatorList()

    # client.getVideoURL('wBkla5faBo', is_download=True, is_stream=False)

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
        creators = client.getCreatorInfo([sub.creator.id for sub in subscriptions])
        for sub in subscriptions:
            print('Subscription: {} ({} {})'.format(sub.plan.title, sub.plan.price, sub.plan.currency))

        for creator in creators:
            creator_title = '----- {} -----'.format(creator.title)
            print('\n' + '-' * len(creator_title))
            print(creator_title)
            print('-' * len(creator_title))

            print('\n----- Playlists -----')
            showCreatorPlaylists(client, creator)
            print('\n----- Videos -----')
            showCreator(client, creator, showVideoFunc=download_video, displayDownloadLink=True, videoLimit=video_limit)
            print('\n-----------------------------\n')

except KeyboardInterrupt:
    print()
    print('Aborted by Keystroke!')

except Exception as e:
    log.critical(e)
    sentry_sdk.capture_exception(e)
