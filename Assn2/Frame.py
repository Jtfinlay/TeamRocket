

class Frame:
  
  # Constructor
  #
  # @param slot: current slot
  def __init__(self, slot):
    self.slot_generated = slot
    self.slot_transmitted = -1
    self.generated = 0

  # Track when successfully transmitted
  #
  # @param slot: current slot
  def transmit(self, slot):
    self.slot_transmitted = slot

  # Collision on transmission
  def collision(self):
    self.slot_transmitted = -1

  # Get time for generation to transmission
  def getDelay(self):
    if self.slot_transmitted == -1:
      return 0
    else:
      return self.slot_transmitted - self.slot_generated + 1
