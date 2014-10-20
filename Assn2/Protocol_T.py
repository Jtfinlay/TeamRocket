
import random

#
# Time Division Multiplexing
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

      for node in self.stations:
        node.generate_frame()

      self.stations[s-(s/len(self.stations))*len(self.stations)].transmit()

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
      self.frames+=1

  # Transmit frame
  #
  # @param prob: Probability of transmitting
  def transmit(self):
    if self.frames > 0:
      self.frames-=1
      self.transmissions+=1
      return True
    else:
      return False
