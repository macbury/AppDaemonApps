from intent_handler import IntentHandler
import time

class TimeIntent(IntentHandler):
  def name(self):
    return 'time.now'
  def async_call(self):
    self.app.log("This is triggered in background")
  def call(self, data):
    return "The time is {}".format(time.strftime("%H %M"))

