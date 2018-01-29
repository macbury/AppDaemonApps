from intent_handler import IntentHandler
import spotipy.oauth2
import spotipy
from fuzzywuzzy import fuzz

SCOPE = 'user-read-playback-state user-modify-playback-state user-read-private'

class SpotifyIntent(IntentHandler):
  oauth = None
  player = None
  token_info = None

  def call(self, data):
    self._prepare_player()
    if self.token_info is None or self.oauth.is_token_expired(self.token_info):
      return "Spotify failed to update, token expired."

  def _load_token(self):
    callback_url = self.app.args['spotify_callback_url']
    cache = self.app.args['spotify_cache_path']
    client_id = self.app.args['spotify_client_id']
    client_secret = self.app.args['spotify_client_secret']

    self.oauth = spotipy.oauth2.SpotifyOAuth(
          client_id, client_secret,
          callback_url, scope=SCOPE,
          cache_path=cache)
    self.token_info = self.oauth.get_cached_token()

  def _prepare_player(self):
    if self.oauth is None or self.oauth.is_token_expired(self.token_info):
      self._load_token()
      self.player = None

    if self.oauth.is_token_expired(self.token_info):
      return None

    if self.player is None:
      self.player = spotipy.Spotify(auth=self.token_info.get('access_token'))

class CurrrentMusicIntent(SpotifyIntent):
  def name(self):
    return 'music.info'

  def call(self, data):
    self._prepare_player()
    current_playback = self.player.current_playback()
    if current_playback is None:
      return "Nothing is currently playing"

    item = current_playback['item']
    track = item['name']
    artist = item['artists'][0]['name']

    return "Currently playing {} by {}".format(track, artist)
      

class MusicControlIntent(IntentHandler):
  def name(self):
    return 'music.control'

  def call(self, data):
    action = self.app.get_apiai_slot_value(data, "MusicAction")
    entity_id = 'media_player.spotify'
    if action == 'shuffle':
      self.app.call_service("media_player/shuffle_set", entity_id=entity_id, shuffle=True)
    else:
      self.app.call_service("media_player/media_{}".format(action.replace(" ", '_')), entity_id=entity_id)
    return "Asking Spotify to {}".format(action)

class MusicPlayIntent(SpotifyIntent):
  def name(self):
    return 'music.play'

  def set_source_wifi(self):
    entity_id = 'media_player.soundbar'
    self.app.call_service("media_player/select_source", entity_id=entity_id, source='wifi')

  def async_play(self, kwargs):
    self.set_source_wifi()
    entity_id = 'media_player.spotify'
    source = '[AV] Samsung Soundbar K650'
    self.app.log("Selecting source for: {}".format(self.uri))
    self.app.call_service("media_player/select_source", entity_id=entity_id, source=source)
    self.app.log("Playing: {}".format(self.uri))
    self.app.call_service("media_player/play_media", entity_id=entity_id, media_content_id=self.uri, media_content_type=self.media_content_type)
    self.app.log("Finished play for: {}".format(self.uri))
  
  def play(self, uri, media_content_type):
    self.uri = uri
    self.media_content_type = media_content_type
    self.app.run_in(self.async_play, 0)

  def call(self, data):
    self._prepare_player()
    name = self.app.get_apiai_slot_value(data, "ArtistOrPlaylist")

    playlist_data = self.find_playlist(name)
    if playlist_data is not None:
      self.play(playlist_data['uri'], 'playlist')
      return "Playing playlist {}".format(playlist_data['name'])

    artist_data = self.find_artist(name)
    if artist_data is not None:
      self.play(artist_data['uri'], 'playlist')
      return "Playing songs by {}".format(artist_data['name'])

    track_data = self.find_track(name)
    if track_data is not None:
      self.play(track_data['uri'], 'music')
      return "Playing song {}".format(track_data['name'])

    return "Could not find {}".format(name)

  def find_playlist(self, playlist_name):
    current_user = self.player.current_user()['id']

    playlists = self.player.user_playlists(current_user)
    best_score = 0
    best_match = None
    for playlist in playlists['items']:
      score = fuzz.ratio(playlist_name, playlist['name'])
      if score > best_score:
        best_match = playlist
        best_score = score

    if best_score >= 70:
      return { 'uri': best_match['uri'], 'name': best_match['name'], 'score': best_score }
    else:
      return None

  def find_artist(self, artist_name):
    results = self.player.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']

    best_score = 0
    best_match = None
    for artist in items:
      score = fuzz.ratio(artist_name, artist['name'])
      if score > best_score:
        best_match = artist
        best_score = score

    if best_score >= 70:
      return { 'uri': best_match['uri'], 'name': best_match['name'], 'score': best_score }
    else:
      return None

  def find_track(self, track_name):
    results = self.player.search(q='track:' + track_name, type='track')
    items = results['tracks']['items']

    best_score = 0
    best_match = None
    for track in items:
      score = fuzz.ratio(track_name, track['name'])
      if score > best_score:
        best_match = track
        best_score = score

    if best_score >= 70:
      return { 'uri': best_match['uri'], 'name': best_match['name'], 'score': best_score }
    else:
      return None
