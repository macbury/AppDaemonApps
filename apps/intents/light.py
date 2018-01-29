from intent_handler import IntentHandler

class LightBrightness(IntentHandler):
  def name(self):
    return 'light.brightness'

  def get_by(self, data):
    try:
      return float(self.app.get_apiai_slot_value(data, "percentage"))/100.0
    except Exception as e:
      return 0.3

  def call(self, data):
    action = self.app.get_apiai_slot_value(data, "UpDown")
    if action is None:
      action = 'up'
    by = self.get_by(data)

    current = float(self.app.get_state('light.living_room_zyrandol_a', 'brightness'))

    if action == 'up':
      current += 255 * by
    else:
      current -= 255 * by

    if current > 255:
      current = 255

    if current < 0:
      current = 0

    self.app.turn_on('group.living_room_main_light', brightness=int(current))
    by_percent = round(by * 100)
    current_percent = round((current / 255.0) * 100)
    return "Brightness {} by {} to {} percent".format(action, by_percent, current_percent)
