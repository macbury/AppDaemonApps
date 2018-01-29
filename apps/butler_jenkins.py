import appdaemon.appapi as appapi
import random

from intents.spotify import MusicControlIntent, MusicPlayIntent, CurrrentMusicIntent
from intents.time import TimeIntent
from intents.family import FamilyLocationIntent
from intents.conditions import CurrentConditionsIntent, WillItRainIntent
from intents.home import GoodMorningIntent, GoodNightIntent, BedtimeIntent
from intents.devices import DevicesSwitchOnOffIntent
from intents.light import LightBrightness
from intents.programing import StartProgramingIntent
from intents.soundbar import SoundbarVolumeIntent, SoundbarSourceIntent
from intents.script import ScriptRunIntent
from intents.cat import FeedTheCat, InfoAboutFeeding, ReFill
from intents.air_purifier import AirPurifierMode

class ButlerJenkins(appapi.AppDaemon):
  def initialize(self):
    self.log("Registering endpoint...")
    self.intents = {}
    self.register_endpoint(self.api_call, "assistant")
    self.log("Initializing butler..")
    self.register(TimeIntent)
    self.register(FamilyLocationIntent)
    self.register(CurrentConditionsIntent)
    self.register(GoodMorningIntent)
    self.register(GoodNightIntent)
    self.register(BedtimeIntent)
    self.register(DevicesSwitchOnOffIntent)
    self.register(LightBrightness)
    self.register(StartProgramingIntent)
    self.register(MusicControlIntent)
    self.register(MusicPlayIntent)
    self.register(CurrrentMusicIntent)
    self.register(SoundbarVolumeIntent)
    self.register(SoundbarSourceIntent)
    self.register(WillItRainIntent)
    self.register(ScriptRunIntent)
    self.register(FeedTheCat)
    self.register(InfoAboutFeeding)
    self.register(ReFill)
    self.register(AirPurifierMode)

  def register(self, intent_klass):
    assistant = self
    intent = intent_klass(self)
    self.log("Registering: {} as {}".format(intent_klass, intent.name()))
    self.intents[intent.name()] = intent

  def api_call(self, data):
    intent = self.get_apiai_intent(data)
    if intent is None:
      self.log("Butler jenkins error encountered")
      return "", 201
    self.log("Intent: {}".format(intent))
    
    if intent in self.intents:
      intent_obj = self.intents[intent]
      speech = intent_obj.call(data)
      intent_obj.perform_async_call()
      response = self.format_apiai_response(speech = speech)
      self.log("Recieved Butler jenkins request: {}, answering: {}".format(intent, speech))

    else:
      response = self.format_apiai_response(speech = "I'm sorry, the {} does not exist within AppDaemon".format(intent))

    return response, 200
