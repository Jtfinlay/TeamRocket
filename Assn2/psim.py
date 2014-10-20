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



# Time Division Multiplexing
#
# @param N: Number of stations
# @param p: Frame generation probability
# @param R: Total number of slots
def protocol_T(N, p, R):
  stations = [];
  for i in range(N):
    stations.append(Station.Station(p))

  for s in range(R):

    for node in stations:
      node.generate_frame()

    stations[s-(s/N)*N].transmit()






psim('T', 20, .01, 50000, [5, 1,2,3,4])
