import config
import spotifyhandler
import urllib3
import spotipy
import spotipy.util as util
from flask import Flask, render_template, request
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from urlextract import URLExtract

extractor = URLExtract()
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world! banger-bot is up and running!"

@app.route('/msg', methods=['POST'])
def webhook():
  data = request.get_json()
  if data['name'] != 'banger-bot': # main logic for checking GM messages
    if "open.spotify.com/track/" in data['text']:
      urls = extractor.find_urls(data['text'])
      o = urlparse(urls[0])
      track_id = o.path.split("/track/", 1)[1]
      spotifyhandler.add_track([track_id], group_id=data['group_id'])
  return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, threaded=True)
