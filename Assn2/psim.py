#
# CMPUT 313 - Computer Networks
# Assignment 2 - Comparison of Medium Access Control Protocols
#
# Author: Jesse Tucker & James Finlay
#

import math
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

  throughput = []
  delay_per_frame = []

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
    throughput.append(float(prot.getTransmittedFrameCount()) / float(R))
    delay_per_frame.append(prot.getTransmissionDelays())

  throughput_avg = sum(throughput) / float(T[0])
  delay_per_frame_avg = sum(delay_per_frame) / float(T[0])
  throughput_std = calcStandardDeviation(throughput, throughput_avg)
  delay_per_frame_std = calcStandardDeviation(delay_per_frame, delay_per_frame_avg)

  # ---- OUTPUTS ---- #
  print Protocol,N,p,R,T[0],"\n"
  # Average throughput followed by confidence interval
  print throughput_avg, throughput_std
  # Overall average per-frame delay followed by conf. int.
  print delay_per_frame_avg, delay_per_frame_std

def calcStandardDeviation(arr, mean):
  result = 0
  for val in arr:
      result += (val - mean) * (val - mean)

  if len(arr) > 1:
      result = math.sqrt(result / (len(arr) - 1))
  else:
      result = math.sqrt(result)
  return result

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
