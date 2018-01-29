import appdaemon.appapi as appapi
import spotipy

class HelloWorld(appapi.AppDaemon):
  def initialize(self):
    self.log("Hello world!!!")
    #self.log(self.args['spotify_client_id'])
