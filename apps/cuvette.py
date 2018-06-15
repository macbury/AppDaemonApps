import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

class Cuvette(hass.Hass):
  def initialize(self):
    self.log("Current state is {}".format(self.get_status()))
    self.listen_event(self.on_timer_finish, 'timer.finished', entity_id=self.args['timer_id'], old="off", new="on")

  def on_timer_finish(self, event_name, data, *args, **kwargs):
    self.clean_kitchen()

  def wait_for_state(self, required_state):
    while self.get_status() != required_state:
      self.log("Waiting for state {} while current is {}".format(required_state, self.get_status()))
      time.sleep(1)

  def get_status(self):
    vacuum_id = self.args['vacuum_id']
    return self.get_state(self.args['vacuum_id'], attribute = "status")

  def clean_kitchen(self):
    target_point = self.args['target_point']
    vacuum_id = self.args['vacuum_id']
    self.log("Switching to quiet mode")
    self.call_service('vacuum/set_fan_speed', entity_id=vacuum_id, fan_speed='Quiet')
    self.log("Going near cuvvete")
    self.call_service('vacuum/send_command', entity_id=vacuum_id, command='app_goto_target', params=target_point)
    self.wait_for_state("Going to target")
    self.log("Starting move to target...")
    self.wait_for_state("Idle")
    self.log("Target reached, starting spot cleaning")
    self.call_service('vacuum/clean_spot', entity_id=vacuum_id)
    self.log("Waiting for cleaning to start")
    self.wait_for_state("Spot cleaning")
    self.log("Waiting for cleaning to end")
    self.wait_for_state("Idle")
    self.call_service('vacuum/return_to_base', entity_id=vacuum_id)
