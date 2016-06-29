#!/usr/bin/env python
from __future__ import print_function
import gmusicapi
import pprint
import json
import getpass
import os

def map_track_duplication(tracks):
    album_track_duplicate_map = {}
    for track in tracks:
        albumNorm = track['album'].lower()
        titleNorm = track['title'].lower()
        if albumNorm not in album_track_duplicate_map:
            album_track_duplicate_map.update({albumNorm: {}})
        if titleNorm in album_track_duplicate_map[albumNorm]:
            album_track_duplicate_map[albumNorm][titleNorm] += 1
        else:
            album_track_duplicate_map[albumNorm][titleNorm] = 1
    return album_track_duplicate_map


def sort_tracks_by_album(tracks):
    tracks_by_album = {}
    for track in tracks:
        albumNorm = track['album'].lower()
        if albumNorm not in tracks_by_album:
            tracks_by_album[albumNorm] = []
        tracks_by_album[albumNorm].append(track)
    return tracks_by_album


def get_duplicate_tracks(all_tracks_by_album, album_track_duplicate_map):
    duplicate_tracks = []
    for album_title in album_track_duplicate_map:
        for track_title in album_track_duplicate_map[album_title]:
            duplicates = album_track_duplicate_map[album_title][track_title] - 1
            if duplicates > 0:
                for album in all_tracks_by_album:
                    if album_title == album:
                        for track in all_tracks_by_album[album]:
                            albumNorm = track['album'].lower()
                            titleNorm = track['title'].lower()
                            if titleNorm == track_title and duplicates > 0:
                                duplicate_tracks.append(track)
                                print("Queueing for removal: '" + track['title'] + "' from album '" + track['album'] + "' by '" + track['artist'])
                                all_tracks.remove(track)
                                duplicates += -1
    return duplicate_tracks

import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


def get_track_ids(tracks):
    track_ids = []
    for track in tracks:
        track_ids.append(track['id'])
    return track_ids


from_test_file = os.environ.get('GMUSIC_DUPE_TEST_FILE', None)
logged_in = False
playlist_contents = []

if from_test_file is not None:
    logged_in = True
    print('Loading from test file {}'.format(from_test_file))
    with open(os.path.abspath(from_test_file), 'r') as f:
        playlist_contents = json.loads(f.read())
else:
    api = gmusicapi.Mobileclient()
    logged_in = api.login(raw_input('Username: '), getpass.getpass(), gmusicapi.Mobileclient.FROM_MAC_ADDRESS)
    playlist_contents = api.get_all_user_playlist_contents()

#logged_in = True
#
#pp = pprint.PrettyPrinter(indent=2)

if logged_in:
    #print("Successfully logged in. Beginning duplicate detection process."
    #playlists = api.get_all_playlists()
    #pp.pprint(playlists)


    #pp.pprint(playlist_contents)

    for playlist in playlist_contents:
        if playlist.get('type') != 'USER_GENERATED':
            continue

        print('\n\nProcessing playlist "{}"'.format(playlist.get('name')))
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
            dupe_playlist_track_ids.add(track.get('id'))

        print('Found {} dupe tracks out of {} total'.format(len(dupe_track_ids), track_count))
        if len(dupe_track_ids) > 0:
            print('These tracks are unique:')
            #pp.pprint(track_map)
            for track_id in uniq_track_ids:
                track = track_map.get(track_id, None)
                track_info = track.get('track')
                if track_info is None:
                    print('No track info, id:{}'.format(track_id))
                    continue

                #pp.pprint(track)
                print('\tid: {}, title: "{}", album: "{}", artist: "{}"'.format(track_id, track_info.get('title'), track_info.get('album'), track_info.get('artist')))

            print('\nThese tracks are duplicates!!:')
            for track_id in dupe_track_ids:
                track = track_map.get(track_id, None)
                track_info = track.get('track')
                if track_info is None:
                    print('No track info, id:{}'.format(track_id))
                    continue

                #pp.pprint(track)
                print('\tid: {}, title: "{}", album: "{}", artist: "{}"'.format(track_id, track_info.get('title'), track_info.get('album'), track_info.get('artist')))

        print("=========================")
        # Find duplicates

    #all_tracks = api.get_all_songs()
    #album_track_duplicate_map = map_track_duplication(all_tracks)
    #all_tracks_by_album = sort_tracks_by_album(all_tracks)
    #duplicate_tracks = get_duplicate_tracks(all_tracks_by_album, album_track_duplicate_map)
    #duplicate_track_ids = get_track_ids(duplicate_tracks)
    #if len(duplicate_track_ids) > 0:
    #    if query_yes_no("Found " + str(len(duplicate_track_ids)) + " duplicate tracks. Delete duplicates?", "no"):
    #        deleted_track_ids = []
    #        for track in duplicate_track_ids:
    #            deleted_track_ids += api.delete_songs(track)
    #        print("Successfully deleted " + str(len(deleted_track_ids)) + " of " + str(len(duplicate_track_ids)) + " queued songs for removal."
    #else:
    #    print("I didn't find any duplicate tracks."
    #print("Thank you!"
