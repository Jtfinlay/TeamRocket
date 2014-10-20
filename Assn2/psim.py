#
# CMPUT 313 - Computer Networks
# Assignment 2 - Comparison of Medium Access Control Protocols
#
# Author: Jesse Tucker & James Finlay
#

import Station

#
# @param Protocol:
# 'T' - Time Division Multiplexing
# 'P' - Slotted ALOHA with probabilistic backoff
# 'I' - Slotted ALOHA with interval-based back-off
# 'B' - Slotted ALOHA with a binary exponential back-off
# @param N: Number of stations
# @param p: Frame generation probability for each node
# @param R: Total number of slots to simulate
# @param T: Number of trials, followed by seeds of file
def psim(Protocol, N, p, R, T):


  for trial in range(T[0]):




# Slotted ALOHA with probabilistic backoff
#
# @param N: Number of stations
# @param p: Frame generation probability
# @param R: Total number of slots
def protocol_P(N, p, R):

  stations = [];
  for i in range(N):
    stations.append(Station.Station(p))

  for s in range(R):
    transmissions = [] # Keep track of transmitting nodes

    for i, node in enumerate(stations):

      # each node tries to generate a frame
      node.generate_frame()

      # every node might try to transmit
      if (node.previous_collision):
        if node.transmit(1.0/N):
          transmissions.append(i)
      else:
        if node.transmit(1.0):
          transmissions.append(i)

    # if collision, let the nodes know
    if len(transmissions) > 1:
      for index in transmissions:
        stations[i].collision()

# Slotted ALOHA with interval-based backoff
#
# @param N: Number of stations
# @param p: Frame generation probability
# @param R: Total number of slots
def protocol_I(N, p, R):

  stations = [];
  for i in range(N):
    stations.append(Station.Station(p))

  for s in range(R):




psim('T', 20, .01, 50000, [5, 1,2,3,4])
