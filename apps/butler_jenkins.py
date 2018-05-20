import appdaemon.appapi as appapi
import random

from intents.family import FamilyLocationIntent
from intents.script import ScriptRunIntent
from intents.cat import FeedTheCat, InfoAboutFeeding, ReFill

class ButlerJenkins(appapi.AppDaemon):
  def initialize(self):
    self.log("Registering endpoint...")
    self.intents = {}
    self.register_endpoint(self.api_call, "alexa")
    self.log("Initializing butler..")
    self.register(FamilyLocationIntent)
    self.register(ScriptRunIntent)
    self.register(FeedTheCat)

  def register(self, intent_klass):
    assistant = self
    intent = intent_klass(self)
    self.log("Registering: {} as {}".format(intent_klass, intent.name()))
    self.intents[intent.name()] = intent

  def api_call(self, data):
    self.log("Got api call!")
    intent = self.get_alexa_intent(data)
    if intent is None:
      self.log("Butler jenkins error encountered")
      return "", 201
    self.log("Intent: {}".format(intent))

    if intent in self.intents:
      intent_obj = self.intents[intent]
      speech = intent_obj.call(data)
      intent_obj.perform_async_call()
      response = self.format_alexa_response(speech = speech)
      self.log("Recieved Butler jenkins request: {}, answering: {}".format(intent, speech))
    else:
      response = self.format_alexa_response(speech = "I'm sorry, the {} does not exist within AppDaemon jenkins".format(intent))

    return response, 200
