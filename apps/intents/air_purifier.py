from intent_handler import IntentHandler

def fan_id(room):
  return "fan.{}_air_purifier".format(room.lower().replace(" ", "_"))

class AirPurifierMode(IntentHandler):
  def name(self):
    return 'air_purifier.set'

  def call(self, data):
    room = self.app.get_apiai_slot_value(data, "Room")
    speed = self.app.get_apiai_slot_value(data, "AirPurifierMode")

    self.app.call_service('fan/set_speed', entity_id=fan_id(room), speed=speed)
    return "I have changed {} air purifier mode to {}, master".format(room, speed)