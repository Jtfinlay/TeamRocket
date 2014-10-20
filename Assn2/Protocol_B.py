
#
# Slotted ALOHA with a binary exponential backoff
#
class Protocol_B:

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
        node.generate_frame()

        if node.transmit(i):
          t_stations.append(i)

      for i in t_stations:
        if len(t_stations) > 1:
          self.stations[i].collision()
        else:
          self.stations[i].reset_collision_sequence()

class Station:

  prob_generation = 0
  frames = 0 # Number of frames in queue
  transmissions = 0 # Number of transmissions sent
  collisions = 0 # Number of collisions

  prev_collisions = 0 # Number of collisions in sequence
  next_slot = 0 # Next slot to transmit on
  max_interval = 512

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p


  # Genereate frame from generation probability
  def generate_frame(self):
    if random.random() <= self.prob_generation:
      frames++

  # Transmit frame
  #
  # @param slot: Current slot number
  def transmit(self, slot):
    if len(self.frame) > 0 && self.next_slot <= slot:
      self.frames--
      self.transmissions++
      return True
    else:
      return False

  # Collision detected. Put frame back into queue
  #
  # @param slot: Current slot number
  def collision(self, slot):
    self.prev_collisions++
    upper = random.randint(1, min(self.max_interval, math.pow(2,self.prev_collisions)))
    self.next_slot = slot + random.randint(1,upper)
    self.collsions++
    self.frames++

  # Successful transmission! Reset failure sequence
  def reset_collision_sequence(self):
    self.prev_collisions = 0
