import appdaemon.plugins.hass.hassapi as hass
import requests
import time
import random
class ThingSpeak(hass.Hass):
  def sensor(self):
    return self.args['entity_id']

  def api_key(self):
    return self.args['api_key']

  def field(self):
    return self.args['field']

  def value(self):
    return self.get_state(self.sensor())

  def initialize(self):
    self.listen_state(self.on_adaptation_callback, entity = self.sensor())
    self.publish()

  def on_adaptation_callback(self, entity, attribute, old, new, kwargs):
    self.log("State callback triggered for {} from {} to {}.".format(entity, old, new))
    self.publish()

  def publish(self):
    self.log("Sending state for {} and field {} and value: {}".format(self.sensor(), self.field(), self.value()))
    endpoint = "https://api.thingspeak.com/update?api_key={}&{}={}".format(self.api_key(), self.field(), self.value())
    request = requests.get(endpoint)
    self.log(request.text)
