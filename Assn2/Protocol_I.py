
#
# Slotted ALOHA with interval-based backoff
#
class Protocol_I:

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
      t_stations = []

      for i, node in enumerate(self.stations):
        node.generate_Frame()

        if node.transmit(i):
          t_stations.append(i)

      if len(t_stations) > 1:
        for i in t_stations:
          self.stations[i].collision()

class Station:

  prob_generation = 0
  frames = 0 # Number of frames in queue
  transmissions = 0 # Number of transmissions sent
  collisions = 0 # Number of collisions

  next_interval = 0 # Next interval to transmit on

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
  # @param slot: Current slot number
  def transmit(self, slot):
    if len(self.frame) > 0 && self.next_interval <= slot:
      self.frames--
      self.transmissions++
      return True
    else:
      return False

  # Collision detected. Put frame back into queue
  #
  # @param slot: Current slot number
  # @param N: Number of stations
  def collision(self, slot, N):
    self.next_interval = slot + random.randint(1,N)
    self.collisions++
    self.frames++
