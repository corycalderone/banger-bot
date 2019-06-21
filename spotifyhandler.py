import spotipy
import spotipy.util as util
import config
import groupmehandler
import random

username = 'coryc'
scope = 'playlist-modify-public'

reponses = [
        "Already sent! Loser!"
        ]

def add_track(tracks, group_id):
    token = util.prompt_for_user_token(
        username, scope, config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost/')

    if token:
        print("Successfully acquired token.")
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
    else:
        print("Can't get token for", username)


    with open("log.txt", "r") as f:
        log = f.read()
        log = log.split("\n")
        log = list(filter(None, log))

        for track_id in tracks:
            if track_id not in log:
                log.append(track_id)
                sp.user_playlist_add_tracks(username, config.playlist_ids[group_id], tracks)
                print("Successfully added track!")
                with open("log.txt", "w") as f:
                    for post_id in log:
                        f.write(post_id + "\n")
            else:
                groupmehandler.send_message("Already been sent, feel shame", group_id)
                print("Duplicate detected in group "+group_id+", ignoring.")
