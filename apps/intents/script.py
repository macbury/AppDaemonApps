from intent_handler import IntentHandler

class ScriptRunIntent(IntentHandler):
  def name(self):
    return 'script.run'

  def call(self, data):
    self.script = None
    scriptName = self.app.get_apiai_slot_value(data, "Script")
    if scriptName is None:
      return "Could not find script with name: {}".format(scriptName)

    self.script = scriptName.lower().replace(" ", "_")

    return "Starting script: {}".format(scriptName)

  def async_call(self):
    self.app.log("Triggering: {}".format(self.script))
    self.app.call_service("script/{}".format(self.script))
    self.script = None
