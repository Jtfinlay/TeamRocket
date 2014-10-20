
import random

#
# Slotted ALOHA with interval-based backoff
#
class Protocol:

  stations = []

  # Constructor
  #
  # @param N: Number of stations
  # @param p: Frame generation probability
  def __init__(self, N, p):
    for i in range(N):
      self.stations.append(Station(p))

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

      if len(t_stations) > 1:
        for i in t_stations:
          self.stations[i].collision(s, len(self.stations))

class Station:

  prob_generation = 0
  frames = 0 # Number of frames in queue
  transmissions = 0 # Number of transmissions sent
  collisions = 0 # Number of collisions

  next_slot = 0 # Next interval to transmit on

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p

  # Generate frame from generation probability
  def generate_frame(self):
    if random.random() <= self.prob_generation:
      self.frames += 1

  # Transmit frame
  #
  # @param slot: Current slot number
  def transmit(self, slot):
    if self.frames > 0 and self.next_slot <= slot:
      self.frames -= 1
      self.transmissions += 1
      return True
    else:
      return False

  # Collision detected. Put frame back into queue
  #
  # @param slot: Current slot number
  # @param N: Number of stations
  def collision(self, slot, N):
    self.next_slot = slot + random.randint(1,N)
    self.collisions+=1
    self.frames+=1
