
import random

#
# Slotted ALOHA with probabilistic backoff
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

        if node.previous_collision:
          if node.transmit(1.0/len(self.stations)):
            t_stations.append(i)
        else:
          if node.transmit(1.0):
            t_stations.append(i)

      if len(t_stations) > 1:
        for i in t_stations:
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
      self.frames += 1

  # Transmit frame
  #
  # @param prob: Probability of transmitting
  def transmit(self, prob):
    if self.frames > 0 and random.random() <= prob:
      self.frames -= 1
      self.transmissions += 1
      self.previous_collision = False
      return True
    else:
      return False

  # Collision detected. Put frame back into queue
  def collision(self):
    self.previous_collision = True
    self.collisions+=1
    self.frames+=1
