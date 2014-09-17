#
# CMPUT 313 - Computer Networks
# Assignment 1 - A Study of Combined Error Detection and Error Correction Scheme
#
# Author: Jesse Tucker & James Finlay
#
import Frame

### Runs simple simulator to investigate the impact of error-correction encoding
### on the throughput of a communication channel.
###
### @param A: You can assume the feedback time is 500 bit time units.
### @param K: The number of blocks.
### @param F: Size of the frame in number of bits. Assume 4000 bits.
### @param e: Probability that bit is in error
### @param R: Length of simulation in bit time units.
def main(A, K, F, e, R, T):

    f = Frame.Frame(K, F);

    print f.getWastedData()
