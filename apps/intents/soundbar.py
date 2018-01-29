from intent_handler import IntentHandler

class SoundbarVolumeIntent(IntentHandler):
  def name(self):
    return 'soundbar.volume'

  def call(self, data):
    entity_id = 'media_player.soundbar'

    action = self.app.get_apiai_slot_value(data, "UpDown")
    amount = self.app.get_apiai_slot_value(data, "Amount")
    scaled_amount = float(amount) / 20.0
    volume_level = float(self.app.get_state(entity_id, 'volume_level'))

    if action == 'set':
      volume_level = scaled_amount
      speech = "Changing soundbar volume to {}".format(amount)
    else:
      if action == 'up':
        volume_level += scaled_amount
      else:
        volume_level -= scaled_amount

      speech = "Changed soundbar volume to {}".format(int(volume_level * 20.0))

    self.app.call_service("media_player/volume_set", entity_id=entity_id, volume_level=volume_level)
    return speech

class SoundbarSourceIntent(IntentHandler):
  def name(self):
    return 'soundbar.set_source'

  def perform_async_call(self):
    entity_id = 'media_player.soundbar'
    self.app.call_service("media_player/select_source", entity_id=entity_id, source=self.source)

  def call(self, data):
    self.source = self.app.get_apiai_slot_value(data, "SoundbarSource")
    return "Changed soundbar source to {}".format(self.source)
