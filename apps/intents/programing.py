from intent_handler import IntentHandler
import random

class StartProgramingIntent(IntentHandler):
  def name(self):
    return 'programing.start'

  def run_script(self, kwargs):
    self.app.call_service('script/go_programing')

  def call(self, data):
    responses = [
      "Your word is my command",
      "As you wish captain!"
    ]

    self.app.run_in(self.run_script, 1)
    return random.choice(responses)
