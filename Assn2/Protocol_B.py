
import random
import math
import Frame

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
        node.generate_frame(s)

        if node.transmit(s):
          t_stations.append(i)

      for i in t_stations:
        if len(t_stations) > 1:
          self.stations[i].collision(s)
        else:
          self.stations[i].reset_collision_sequence()

class Station:

  prob_generation = 0
  frames_waiting = [] # Unsent frames
  frames_sent = [] # Sent frames

  prev_collisions = 0 # Number of collisions in sequence
  next_slot = 0 # Next slot to transmit on
  max_interval = 512

  # Constructor
  #
  # @param p: Frame generation probability
  def __init__(self, p):
    self.prob_generation = p

  # Genereate frame from generation probability
  def generate_frame(self, slot):
    if random.random() <= self.prob_generation:
      self.frames_waiting.append(Frame.Frame(slot))

  # Transmit frame
  #
  # @param slot: Current slot number
  def transmit(self, slot):
    if len(self.frames_waiting) > 0 and self.next_slot <= slot:
      frame = self.frames_waiting.pop(0)
      frame.transmit(slot)
      self.frames_sent.append(frame)
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

    frame = self.frames_sent.pop()
    frame.collision()
    self.frames_waiting.insert(0, frame)

  # Successful transmission! Reset failure sequence
  def reset_collision_sequence(self):
    self.prev_collisions = 0
