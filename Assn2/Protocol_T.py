
#
# Time Division Multiplexing
#
class Protocol_T:

  stations = []

  # Constructor
  #
  # @param N: Number of stations
  # @param p: Frame generation probability
  def __init__(self, N, p):
    for i in range(N):
      self.stations.append(Station.Station(p))

  # Run the protocol
  #
  # @param R: Total number of slots
  def run(self, R):

    for s in range(R):

      for node in stations:
        node.generate_frame()

      self.stations[s-(s/N)*N].transmit(1.0)

class Station:

  prob_generation = 0
  frames = 0 # Number of frames in queue
  transmissions = 0 # Number of transmissions sent
  collisions = 0 # Number of collisions

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
  def transmit(self):
    if len(self.frame) > 0:
      self.frames--
      self.transmissions++
      return True
    else:
      return False
