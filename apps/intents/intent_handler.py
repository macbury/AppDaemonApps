class IntentHandler:
  def __init__(self, app):
    self.app = app

  def perform_async_call(self):
    self.app.run_in(self._run_async_call, 0)
  def _run_async_call(self, kwargs):
    self.async_call()
  def async_call(self):
    pass
  def call(self, data):
    pass
