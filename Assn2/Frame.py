

class Frame:
  slot_generated = 0
  slot_transmitted = -1

  # Constructor
  #
  # @param slot: current slot
  def __init__(self, slot):
    slot_generated = slot

  # Track when successfully transmitted
  #
  # @param slot: current slot
  def transmit(self, slot):
    slot_transmitted = slot

  # Collision on transmission
  def collision(self):
    slot_transmitted = -1

  # Get time for generation to transmission
  def get_delay(self):
    if slot_transmitted == -1:
      return 0
    else:
      return slot_transmitted - slot_generated + 1
