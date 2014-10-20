
#
# Slotted ALOHA with probabilistic backoff
#
class Protocol_P:

  stations = []

  # Constructor
  #
  # @param N: Number of stations
  # @param p: Frame generation probability
  def __init__(self, N, p):
    for i in range(N):
      self.stations.append(Station.Station(p));

  # Run the protocol
  #
  # @param R: Total number of slots
  def run(self, R):

    for s in range(R):
      t_stations = []

      for i, node in enumerate(self.stations):
        node.generate_frame()

        if node.previous_collision:
          if node.transmit(1.0/N):
            t_stations.append(i)
        else:
          if node.transmit(1.0):
            t_stations.append(i)

      if len(t_stations) > 1:
        self.stations[i].collision()

class Station:

  prob_generation = 0 # Probability of generating a frame
  frames = 0 # Number of frames in queue
  transmissions = 0 # Number of transmissions sent
  collisions = 0 # Number of collisions

  previous_collision = False # if previous transmission was collision

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
    if len(self.frame) > 0 && random.random() <= prob:
      self.frames--
      self.transmissions++
      self.previous_collision = False
      return True
    else:
      return False

  # Collision detected. Put frame back into queue
  def collision(self):
    self.previous_collision = True
    self.collisions++
    self.frames++
