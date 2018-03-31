import appdaemon.appapi as appapi
import datetime

class AirPurifierController(appapi.AppDaemon):
  def initialize(self):
    self.log("Started...")
    self.fan_id = self.args['fan_id']
    self.run_every(self.on_run_every, datetime.datetime.now(), 15 * 60)
    self.listen_state(self.on_adaptation_callback, entity = self.args['family_devices'])
    self.listen_state(self.on_adaptation_callback, entity = self.args['aqi_sensor'])
    self.adapt_air_purifier_mode()

  def on_run_every(self, kwargs=None):
    self.log("15 min callback")
    self.adapt_air_purifier_mode()

  def current_aqi(self):
    return float(self.get_state(self.args['aqi_sensor']) or '10')

  def anyone_in_home(self):
    state = self.get_state(self.args['family_devices'])
    self.log("State is {} for {}".format(state, self.args['family_devices']))
    return state == 'home'

  def get_mode(self):
    return self.get_state(self.fan_id, 'mode')

  def animal_cleaning_time(self):
    scheduled = self.args['animal_cleaning_time']
    for time_range in scheduled:
      if self.now_is_between(time_range["from"], time_range["to"]):
        self.log("In range: {} -> {}".format(time_range['from'], time_range['to']))
        return True
      else:
        self.log("Not in range: {} -> {}".format(time_range['from'], time_range['to']))
    return False

  def people_cleaning_time(self):
    scheduled = self.args['people_cleaning_time']
    for time_range in scheduled:
      if self.now_is_between(time_range["from"], time_range["to"]):
        self.log("In range: {} -> {}".format(time_range['from'], time_range['to']))
        return True
      else:
        self.log("Not in range: {} -> {}".format(time_range['from'], time_range['to']))
    return False

  def speed_by_aqi(self):
    speed = (self.current_aqi() / 350.0)
    if speed > 1.0:
      speed = 1.0
    return round(speed * 16)

  def update_speed(self, speed):
    self.log("Setting speed to: {}".format(speed))
    self.call_service('fan/xiaomi_miio_set_favorite_level', entity_id=self.fan_id, level=speed)
    self.call_service('fan/set_speed', entity_id=self.fan_id, speed='Auto')

  def turn_off(self):
    self.log("Turning off air purifier")
    self.call_service('fan/turn_off', entity_id=self.fan_id)

  def switch_to_auto(self):
    self.log("Switching to auto mode")
    self.call_service('fan/set_speed', entity_id=self.fan_id, speed='Auto')

  def switch_to_silent(self):
    self.log("Switching to silent mode")
    self.call_service('fan/set_speed', entity_id=self.fan_id, speed='Silent')

  def turn_on(self):
    self.log("Turning on air purifier")
    self.call_service('fan/turn_on', entity_id=self.fan_id)

  def on_adaptation_callback(self, entity, attribute, old, new, kwargs):
    self.log("State callback triggered for {} from {} to {}. Adapting air quality".format(entity, old, new))
    self.adapt_air_purifier_mode()

  def manual_mode(self):
    return self.get_mode() == "silent" or self.get_mode() == "auto"

  def adapt_air_purifier_mode(self):
    self.log("Current mode is: {}".format(self.get_mode()))
    self.log("Current aqi is: {}".format(self.current_aqi()))
    if self.anyone_in_home():
      self.log("People home")
      if not self.manual_mode():
        self.turn_on()
      elif self.people_cleaning_time():
        self.turn_on()
        self.log("Adapting speed")
        self.switch_to_auto()
      else:
        self.turn_on()
        self.log("Out of schedule, turning off")
        self.switch_to_silent()
    else:
      self.log("Nobody home")
      self.log("Turn off completle")
      self.turn_off()

    self.log("Current mode after adapt is: {}".format(self.get_mode()))
