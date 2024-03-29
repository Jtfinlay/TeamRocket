
import random
import Frame

#
# Time Division Multiplexing
#
class Protocol():

  # Constructor
  #
  # @param N: Number of stations
  # @param p: Frame generation probability
  def __init__(self, N, p):
    self.stations = []
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

  # Get count of transmitted frames
  def getTransmittedFrameCount(self):
    result = 0
    for node in self.stations:
      result += node.getTransmittedFrameCount()
    return result

  # Get sum of delays / transmitted frame count
  def getTransmissionDelays(self):
    result = 0
    transmissions = self.getTransmittedFrameCount()
    for node in self.stations:
      result += node.getTransmissionDelays()
    return float(result) / transmissions if transmissions > 0 else 0

class Station:

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p
    self.frames_waiting = [] # Unsent frames
    self.frames_sent = [] # Sent frames

  # Generate frame from generation pr obability
  #
  # @param slot: current slot
  def generate_frame(self, slot):
    if random.random() <= self.prob_generation:
      self.frames_waiting.append(Frame.Frame(slot))

  # Get count of transmitted frames
  def getTransmittedFrameCount(self):
    return len(self.frames_sent)

  # Get sum of delays
  def getTransmissionDelays(self):
    result = 0
    for frame in self.frames_sent:
      result += frame.getDelay()
    return result

  # Transmit frame
  #
  # @param slot: current slot
  def transmit(self, slot):
    if len(self.frames_waiting) > 0:
      frame = self.frames_waiting.pop(0)
      frame.transmit(slot)
      self.frames_sent.append(frame)
