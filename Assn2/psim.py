#
# CMPUT 313 - Computer Networks
# Assignment 2 - Comparison of Medium Access Control Protocols
#
# Author: Jesse Tucker & James Finlay
#

import random

import Protocol_T
import Protocol_P
import Protocol_I
import Protocol_B

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

  throughput = 0
  delay_per_frame = 0

  for trial in range(T[0]):
    if len(T) > trial + 1:
      random.seed(T[trial + 1])

    prot = None
    if Protocol == 'T': prot = Protocol_T.Protocol(N,p)
    elif Protocol == 'P': prot = Protocol_P.Protocol(N,p)
    elif Protocol == 'I': prot = Protocol_I.Protocol(N,p)
    elif Protocol == 'B': prot = Protocol_B.Protocol(N,p)
    else: raise ValueError("Invalid Protocol")

    prot.run(R)
    print "throughput: ",float(prot.getTransmittedFrameCount())/R
    throughput += float(prot.getTransmittedFrameCount()) / R
    delay_per_frame += prot.getTransmissionDelays()

  throughput /= float(T[0])
  delay_per_frame /= float(T[0])

  # ---- OUTPUTS ---- #
  print Protocol,N,p,R,T[0],"\n"
  # Average throughput followed by confidence interval
  print throughput,"\n"
  # Overall average per-frame delay followed by conf. int.
  print delay_per_frame,"\n"


psim('T', 20, .01, 50000, [5, 1,2,3,4,5])
psim('P', 20, .01, 50000, [5, 1,2,3,4,5])
psim('I', 20, .01, 50000, [5, 1,2,3,4,5])
psim('B', 20, .01, 50000, [5, 1,2,3,4,5])
