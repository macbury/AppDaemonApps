from intent_handler import IntentHandler
class FamilyLocationIntent(IntentHandler):
  def name(self):
    return 'family.location'

  def call(self, data):
    ola_location = self.app.get_state('device_tracker.s6_ola')
    arek_location = self.app.get_state('device_tracker.s8_ab')

    speech = ""
    speech += "Arek is at {}.\n".format(arek_location.replace('_', ' '))
    speech += "Ola is at {}.".format(ola_location.replace('_', ' '))

    return speech
