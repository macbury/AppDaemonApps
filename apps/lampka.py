import appdaemon.plugins.hass.hassapi as hass
import datetime
from circleci.api import Api

class Lampka(hass.Hass):
  def initialize(self):
    self.circleci = Api(self.args['circleci_token'])
    self.last_state = None
    self.light_id = self.args['entity_id']
    self.effect_by_state()

    self.run_every(self.on_ci_state_update, datetime.datetime.now(), 10)

  def on_ci_state_update(self, kwargs=None):
    self.log("Tick, so we refresh!")
    self.effect_by_state()

  def effect_by_state(self):
    last_build = self.circleci.get_recent_builds()[0]

    if last_build['status'] != self.last_state:
      effect = ""
      self.last_state = last_build['status']
      self.log("State of build changed to: {}".format(self.last_state))
      if self.last_state == 'running' or self.last_state == 'queued':
        self.log("Effect is running...")
        effect = "Running"
      elif self.last_state == 'success' or self.last_state == 'fixed':
        self.log("Effect is success...")
        effect = "Success"
      else:
        self.log("Effect is failed...")
        effect = "Failed"

      current_state = self.get_state(self.light_id)

      if current_state == 'on':
        self.call_service('light/turn_on', entity_id = self.light_id, effect = effect)
