#
# CMPUT 313 - Computer Networks
# Assignment 2 - Comparison of Medium Access Control Protocols
#
# Author: Jesse Tucker & James Finlay
#

import random
import sys

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


if(len(sys.argv) > 5):

  protocol = sys.argv[1]
  stations = int(sys.argv[2])
  probability = float(sys.argv[3])
  slotTime = int(sys.argv[4])
  trials = map(int, sys.argv[5:])
  
  psim(protocol, stations, probability, slotTime, trials)
else:
  print "Invalid Arguments passed in! Please pass in the format :"
  print "<Protocal Type> <Number of Stations> <probability of generating a frame> <slot time> <Number of Trials> <seed for trial 1> <seed for trial 2> ... <seed for trial N"
