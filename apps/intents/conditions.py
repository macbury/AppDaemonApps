from intent_handler import IntentHandler
import dateparser
import forecastio
import datetime
# https://zeevgilovitz.com/python-forecast.io/
class WillItRainIntent(IntentHandler):
  def name(self):
    return 'conditions.rain'

  def fetch_forecast(self, date):
     api_key = self.app.args['darksky_api_key']
     lat = self.app.args['lat']
     lng = self.app.args['lng']
     forecast = forecastio.load_forecast(api_key, lat, lng, time=date)
     return forecast.currently()
  
  def call(self, data):
    raw_date = self.app.get_apiai_slot_value(data, "Date")
    self.app.log("Raw date is: {}".format(raw_date))
    date = dateparser.parse(raw_date)
    if date is not None:
      date += datetime.timedelta(hours=12)
    self.app.log("Date is {}".format(date))
    forecast = self.fetch_forecast(date)
        
    return "Conditions for {} will be {}".format(forecast.time.strftime("%A"), forecast.summary)

  
class CurrentConditionsIntent(IntentHandler):
  def name(self):
    return 'conditions.current'

  def inside(self):
    temperature = self.app.get_state('sensor.living_room_temperature')
    humidity = self.app.get_state('sensor.living_room_humidity')
    aqi = self.app.get_state('sensor.living_room_purifier_aqi')
    return "Temperature in the living room is {} degrees and humidity is {} percent. Inside air quality index is: {}. ".format(temperature, humidity, aqi)

  def outside(self):
    temperature = self.app.get_state('sensor.dark_sky_temperature')
    humidity = self.app.get_state('sensor.dark_sky_humidity')
    pollution_level = self.app.get_state('sensor.us_air_pollution_level')
    return "Temperature outside is {} degrees and humidity is {} percent. Air quality index is {}".format(temperature, humidity, pollution_level)

  def call(self, data):
    return self.inside() + self.outside()

