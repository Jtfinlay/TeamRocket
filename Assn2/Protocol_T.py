
import random
import Frame

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
        node.generate_frame(s)

      self.stations[s%len(self.stations)].transmit(s)

class Station:

  prob_generation = 0
  frames_waiting = [] # Unsent frames
  frames_sent = [] # Sent frames
  collisions = 0 # Number of collisions

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p

  # Generate frame from generation probability
  #
  # @param slot: current slot
  def generate_frame(self, slot):
    if random.random() <= self.prob_generation:
      self.frames_waiting.append(Frame.Frame(slot))

  # Transmit frame
  #
  # @param slot: current slot
  def transmit(self, slot):
    if len(self.frames_waiting) > 0:
      frame = self.frames_waiting.pop(0)
      frame.transmit(slot)
      self.frames_sent.append(frame)