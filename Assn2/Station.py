
# Station objects holds station/node info
class Station:

  prob_generation = 0  # Probability of generating a frame
  frames = 0  # Number of frames in queue
  transmissions = 0  # Number of transmissions sent
  collisions = 0 # Number of collisions
  previous_collision = False  # If previous transmission was collision

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
  #
  # @param prob: Probability of transmitting
  def transmit(self, prob):
    if len(frame) > 0 && random.random() <= prob:
      self.frames--
      self.transmissions++
      self.previous_collision = False
      return true
    else:
      return false

  # Collision detected. Put frame back into queue.
  def collision(self):
    self.previous_collision = True
    self.frames++
    self.collisions++
