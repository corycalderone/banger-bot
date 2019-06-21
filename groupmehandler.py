import spotifyhandler
import config
import json
import sys
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from urlextract import URLExtract

extractor = URLExtract()

def add_tracks_from_json(file, group_id):
  with open(file) as json_file:
      data = json.load(json_file)

  tracks = []
  for item in data:
      print(item['text'])
      if item['text'] is not None and "open.spotify.com/track/" in item['text']:
        urls = extractor.find_urls(item['text'])
        o = urlparse(urls[0])
        track_id = o.path.split("/track/", 1)[1]
        
        with open("log.txt", "r") as f:
          log = f.read()
          log = log.split("\n")
          log = list(filter(None, log))

        if track_id not in log:
          tracks.append(track_id)
          with open("log.txt", "w") as f:
              for post_id in log:
                  f.write(post_id + "\n")

  n = 99
  tracklists = [tracks[i * n:(i + 1) * n] for i in range((len(tracks) + n - 1) // n )]

  for group in tracklists:
    spotifyhandler.add_track(group, group_id)

def send_message(msg, group_id):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : config.bot_ids[group_id],
          'text'   : msg
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()
