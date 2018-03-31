import appdaemon.appapi as appapi
from adaptive_room_heating import AdaptiveRoomHeating

class KitchenRoomHeating(AdaptiveRoomHeating):
  def lower_temperature(self):
    self.log("Lowering temperature")
    self.call_service('climate/set_temperature', entity_id=self.args['climate'], temperature=0.0)
    self.call_service('climate/set_operation_mode', entity_id=self.args['climate'], operation_mode='Frost Protection')

  def raise_temperature(self):
    self.log("Raising temperature")
    self.call_service('climate/set_operation_mode', entity_id=self.args['climate'], operation_mode='Direct Valve Control')
    self.call_service('climate/set_temperature', entity_id=self.args['climate'], temperature=100.0)

