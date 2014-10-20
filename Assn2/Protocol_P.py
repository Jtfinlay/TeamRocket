
import random
import Frame

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
        node.generate_frame(s)

        if node.previous_collision:
          if node.transmit(1.0/len(self.stations),s):
            t_stations.append(i)
        else:
          if node.transmit(1.0,s):
            t_stations.append(i)

      if len(t_stations) > 1:
        for i in t_stations:
          self.stations[i].collision()

  # Get count of transmitted frames
  def getTransmittedFrameCount(self):
    result = 0
    for node in self.stations:
      result += node.getTransmittedFrameCount()
    return result

  # Get sum of delays / transmitted frame count
  def getTransmissionDelays(self):
    result = 0
    for node in self.stations:
      result += node.getTransmissionDelays()
    return result / self.getTransmittedFrameCount()

class Station:

  prob_generation = 0 # Probability of generating a frame
  frames_waiting = [] # Unsent frames
  frames_sent = [] # Sent frames

  previous_collision = False # if previous transmission was collision

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p

  # Generate frame from generation probability
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
  # @param prob: Probability of transmitting
  # @param slot: current slot
  def transmit(self, prob, slot):
    if len(self.frames_waiting) > 0 and random.random() <= prob:
      frame = self.frames_waiting.pop(0)
      frame.transmit(slot)
      self.frames_sent.append(frame)
      self.previous_collision = False
      return True
    else:
      return False

  # Collision detected. Put frame back into start of queue
  def collision(self):
    self.previous_collision = True
    frame = self.frames_sent.pop()
    frame.collision()
    self.frames_waiting.insert(0,frame)
