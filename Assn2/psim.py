#
# CMPUT 313 - Computer Networks
# Assignment 2 - Comparison of Medium Access Control Protocols
#
# Author: Jesse Tucker & James Finlay
#

import Protocol_P
import Protocol_T

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




psim('T', 20, .01, 50000, [5, 1,2,3,4])
