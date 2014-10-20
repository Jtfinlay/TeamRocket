
# Station objects holds station/node info
class Station:

  prob_generation = 0
  frames = 0
  transmissions = 0

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p

  # Generate frame from generation probability
  def generate_frame(self):
    if random.random() <= self.prob_generation:
      frames++

  # Transmit frame
  def transmit(self):
    if len(frame) > 0:
      frames--
      transmissions++
      return true
    else:
      return false
