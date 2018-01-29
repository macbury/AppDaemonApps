from intent_handler import IntentHandler

class HelloWorldIntent(IntentHandler):

  def name(self):
    return 'hello.world'

  def call(self, data):
    return "Hello world!"
