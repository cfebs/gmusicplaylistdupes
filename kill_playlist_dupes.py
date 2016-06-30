#!/usr/bin/env python
from __future__ import print_function
import gmusicapi
import pprint
import json
import getpass
import os
import sys

def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return choice.strip().lower() in values

def print_track_info(track_id, track):
    if track_info is None:
        print('- trackid: {}'.format(track_id))
        return

    print('- trackid: {}, title: "{}", album: "{}", artist: "{}"'.format(track_id, track_info.get('title'), track_info.get('album'), track_info.get('artist')))


def get_track_ids(tracks):
    track_ids = []
    for track in tracks:
        track_ids.append(track['id'])
    return track_ids


if __name__ == "__main__":
    SHOW_TRACK_INFO = str(os.environ.get('GMUSIC_DUPE_SHOW_TEST_INFO')).strip() == '1'

    from_test_file = os.environ.get('GMUSIC_DUPE_TEST_FILE', None)
    playlist_contents = []
    api = None

    if from_test_file is not None:
        print('Loading from test file {}'.format(from_test_file))
        file_path = os.path.abspath(from_test_file)
        if not os.path.exists(file_path):
            sys.exit('Error: Test file {} not found'.format(file_path))

        with open(file_path, 'r') as f:
            playlist_contents = json.loads(f.read())
    else:
        api = gmusicapi.Mobileclient()
        logged_in = api.login(raw_input('Username: '), getpass.getpass(), gmusicapi.Mobileclient.FROM_MAC_ADDRESS)

        if not logged_in:
            sys.exit('Error: Log in failed')

        print('Logged in, fetching playlists')
        playlist_contents = api.get_all_user_playlist_contents()
        #to create a test file
        test_file = os.environ.get('GMUSIC_WRITE_TEST_FILE', None)
        if test_file is not None:
            with open(os.path.abspath(test_file), 'w') as f:
                f.write(json.dumps(playlist_contents))

            print('json dumped to {}'.format(test_file))
            sys.exit(0)


    for playlist in playlist_contents:
        playlist_name = playlist.get('name')
        print('\nProcessing playlist "{}"'.format(playlist_name))
        uniq_track_ids = set()
        dupe_track_ids = []
        dupe_playlist_track_ids = set()
        track_count = 0
        track_map = {}
        for track in playlist.get('tracks', []):
            track_id = track.get('trackId')

            if track_id is None:
                raise Exception("Empty track id")

            track_map[track_id] = track
            track_count = track_count + 1

            if track_id not in uniq_track_ids:
                uniq_track_ids.add(track_id)
                continue

            # we have a dupe
            dupe_track_ids.append(track_id)
            # track.id not trackId
            # trackId seems to be a fingerprint of the track, where id seems to be the actual
            # playlist track resource (aka. the one we want to get rid of)
            dupe_playlist_track_ids.add(track.get('id'))

        if len(dupe_track_ids) <= 0:
            print('Found {} dupe tracks out of {} total in playlist "{}"'.format(len(dupe_track_ids), track_count, playlist_name))
            print("="*80)
            continue # next playlist

        if SHOW_TRACK_INFO:
            print('These tracks are unique:')
            for track_id in uniq_track_ids:
                track = track_map.get(track_id, None)
                track_info = track.get('track')
                print_track_info(track_id, track_info)

        if SHOW_TRACK_INFO:
            print('\nThese tracks are duplicates!!:')
            for track_id in dupe_track_ids:
                track = track_map.get(track_id, None)
                track_info = track.get('track')
                print_track_info(track_id, track_info)

        print('\nFound {} dupe tracks out of {} total in playlist "{}"'.format(len(dupe_track_ids), track_count, playlist_name))
        if yn_choice("Clean this up?", 'no'):
            print('Removed {} entries'.format(len(dupe_playlist_track_ids)))
            if api is None:
                print('Local test, no clean')

            else:
                api.remove_entries_from_playlist(list(dupe_playlist_track_ids))

        else:
            print('Moving on...')

        print("="*80)

    print('All done')
