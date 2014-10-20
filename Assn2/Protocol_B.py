
import random
import math

#
# Slotted ALOHA with a binary exponential backoff
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

      for i in t_stations:
        if len(t_stations) > 1:
          self.stations[i].collision(s)
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
  def collision(self, slot):
    self.prev_collisions+=1
    upper = random.randint(1, min(self.max_interval, math.pow(2,self.prev_collisions)))
    self.next_slot = slot + random.randint(1,upper)
    self.collisions += 1
    self.frames += 1

  # Successful transmission! Reset failure sequence
  def reset_collision_sequence(self):
    self.prev_collisions = 0
