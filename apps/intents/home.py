from intent_handler import IntentHandler
import random
import time

class BedtimeIntent(IntentHandler):
  def name(self):
    return 'home.bedtime'

  def async_call(self):
    self.app.log("Triggering bedtime in background")
    self.app.call_service('script/bedtime')

  def call(self, data):
    responses = [
      "Bedroom is ready"
    ]
    return random.choice(responses)

class GoodNightIntent(IntentHandler):
  def name(self):
    return 'home.good_night'

  def async_call(self):
    self.app.log("Triggering go sleep in background")
    self.app.call_service('script/go_sleep')
  
  def call(self, data):
    responses = [
      "See you tomorrow",
      "good night, sweet dreams",
      "Good night, bye",
      "Good night sleep well",
      "Bye, Bye"
    ]
    return random.choice(responses)

class GoodMorningIntent(IntentHandler):
  def name(self):
    return 'home.good_morning'

  def welcome(self):
    return 'Hi there!'

  def date(self):
    return "Today is {}".format(time.strftime("%A"))

  def time(self):
    return "The time is {}".format(time.strftime("%H %M"))

  def weather(self):
    temperature = self.app.get_state('sensor.dark_sky_temperature')
    humidity = self.app.get_state('sensor.dark_sky_humidity')
    pollution_level = self.app.get_state('sensor.us_air_pollution_level')
    return "Temperature outside is {} degrees and humidity is {} percent. Air quality index is {}".format(temperature, humidity, pollution_level)

  def rain(self):
    rain_probability = self.app.get_state('sensor.dark_sky_precip_probability')
    return "Probability of rain is {} percent".format(rain_probability)

  def goodbye(self):
    return 'Have a nice day!'

  def call(self, data):
    if self.app.sun_down():
      self.app.log("Switching on the lights!")
      self.app.turn_on('group.living_room_main_light')

    self.app.call_service('script/kitchen_normal_temp')
    self.app.call_service('script/living_room_normal_temp')

    return ".\n".join([
      self.welcome(),
      self.time(),
      self.date(),
      self.rain(),
      self.weather(),
      self.goodbye()
    ])
