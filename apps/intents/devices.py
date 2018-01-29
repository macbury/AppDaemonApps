from intent_handler import IntentHandler

def switch_name(room, name):
  return "switch.{}_{}".format(room.lower().replace(" ", "_"), name.lower().replace(" ", "_"))

def group_name(room, name):
  return "group.{}_{}".format(room.lower().replace(" ", "_"), name.lower().replace(" ", "_"))

def light_name(room, name):
  return "light.{}_{}".format(room.lower().replace(" ", "_"), name.lower().replace(" ", "_"))

def fan_name(room, name):
  return "fan.{}_{}".format(room.lower().replace(" ", "_"), name.lower().replace(" ", "_"))

class DevicesSwitchOnOffIntent(IntentHandler):
  def name(self):
    return 'devices.switch_on_off'

  def handle_fans(self, device, action, room):
    if device == 'air purifier':
      self.app.log("Found match for {}".format(device))
      if action == 'on':
        self.app.turn_on(fan_name(room, device))
      else:
        self.app.turn_off(fan_name(room, device))
      return True
    else:
      return False

  def handle_switch(self, device, action, room):
    if device == 'humidifier' or device == 'christmas tree':
      self.app.log("Found match for {}".format(device))
      if action == 'on':
        self.app.turn_on(switch_name(room, device))
      else:
        self.app.turn_off(switch_name(room, device))
      return True
    else:
      return False

  def handle_tv(self, device, action):
    if device == 'tv':
      entity_id = 'media_player.samsung_tv_remote'
      self.app.call_service('media_player/turn_{}'.format(action), entity_id=entity_id)
      return True
    else:
      return False

  def handle_lights(self, device, action, room):
    if device == 'desk lamp':
      self.app.log("Found light match for {}".format(device))
      if action == 'on':
        self.app.turn_on(light_name(room, device))
      else:
        self.app.turn_off(light_name(room, device))
      return True
    elif device == 'light' or device == 'ambient light':
      self.app.log("Found match for {}".format(device))
      if action == 'on':
        self.app.turn_on(group_name(room, device))
      else:
        self.app.turn_off(group_name(room, device))
      return True
    else:
      return False

  def call(self, data):
    room = self.app.get_apiai_slot_value(data, "Room")
    device = self.app.get_apiai_slot_value(data, "Device")
    action = self.app.get_apiai_slot_value(data, "OnOff") or 'off'

    if self.handle_fans(device, action, room) or self.handle_switch(device, action, room) or self.handle_tv(device, action) or self.handle_lights(device, action, room):
      return "Turning the {} {} in {}".format(device, action, room)
    else:
      return "I could not locate {} in {}".format(device, room)
