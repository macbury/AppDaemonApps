import appdaemon.appapi as appapi
import datetime

class AdaptiveRoomHeating(appapi.AppDaemon):
  def initialize(self):
    self.run_hourly(self.on_hour_callback, datetime.time(0, 0, 0))
    self.listen_state(self.on_adaptation_callback, entity = self.args['family_devices'])
    self.listen_state(self.on_adaptation_callback, entity = self.args['max_temperature'])
    self.listen_state(self.on_adaptation_callback, entity = self.args['min_temperature'])
    self.listen_state(self.on_adaptation_callback, entity = self.args['temperature_sensor'])
    self.heating_time()

  def current_temperature(self):
    return float(self.get_state(self.args['temperature_sensor']))

  def anyone_in_home(self):
    return self.get_state(self.args['family_devices']) == 'home'

  def heating_time(self):
    scheduled = self.args['scheduled']
    for time_range in scheduled:
      if self.now_is_between(time_range["from"], time_range["to"]):
        self.log("In range: {} -> {}".format(time_range['from'], time_range['to']))
        return True
      else:
        self.log("Not in range: {} -> {}".format(time_range['from'], time_range['to']))
    return False

  def max_temperature(self):
    return float(self.get_state(self.args['max_temperature']))

  def min_temperature(self):
    return float(self.get_state(self.args['min_temperature']))

  def lower_temperature(self):
    self.log("Lowering temperature")
    self.call_service('climate/set_temperature', entity_id=self.args['climate'], temperature=7.0)
  def raise_temperature(self):
    self.log("Raising temperature")
    self.call_service('climate/set_temperature', entity_id=self.args['climate'], temperature=28.0)

  def on_hour_callback(self, kwargs):
    self.log("Hour callback")
    self.adapt_temperature()

  def on_adaptation_callback(self, entity, attribute, old, new, kwargs):
    self.log("State callback triggered for {} from {} to {}. Adapting temperature".format(entity, old, new))
    self.adapt_temperature()

  def adapt_temperature(self):
    self.log("Adapting temperature, Current temp is: {}".format(self.current_temperature()))
    if self.current_temperature() >= self.max_temperature():
      self.log("It is too hot")
      self.lower_temperature()
    elif self.current_temperature() <= self.min_temperature():
      self.log("Its cold here")
      self.raise_temperature()
    elif self.anyone_in_home() and self.heating_time():
      self.log("Somebody is home, and still day is")
      self.raise_temperature()
    else:
      self.log("Nobody home or night")
      self.lower_temperature()
