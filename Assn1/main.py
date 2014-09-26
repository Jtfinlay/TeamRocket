#
# CMPUT 313 - Computer Networks
# Assignment 1 - A Study of Combined Error Detection and Error Correction Scheme
#
# Author: Jesse Tucker & James Finlay
#

import Frame
import random

# Runs simple simulator to investigate the impact of error-correction encoding
# on the throughput of a communication channel.
#
# @param A: You can assume the feedback time is 500 bit time units.
# @param K: The number of blocks.
# @param F: Size of the frame in number of bits. Assume 4000 bits.
# @param e: Probability that bit is in error
# @param R: Length of simulation in bit time units.
# @param T: Number of trials, followed by seeds for the trials
def main(A, K, F, e, R, T):

    _transmissionsTotal = 0
    _transmissionsCorrect = 0
    _totalTime = 0
    
    _trialNumber = 1
    
    for trial in range(T[0]):
        
        rnd = random.Random()
        if _trialNumber < len(T):
            rnd.seed(T[_trialNumber])
        else:
            rnd.seed()
        
        [elapsed_time, frames_total, frames_correct] = performTransmissions(A,K,F,e,R, rnd)
    
        _transmissionsTotal += frames_total
        _transmissionsCorrect += frames_correct
        _totalTime += elapsed_time
    
        # Output
        print "---------------------"
        print "Trial", trial
        print "Elapsed time:", elapsed_time
        print "Total frames:", frames_total
        print "Correct frames:", frames_correct
    
        _trialNumber = _trialNumber + 1
    print "---------------------"    
    # Output - what's actually expected
    print A,K,F,e,R,T
    if _transmissionsCorrect / T[0] != 0:
        print (_transmissionsTotal / T[0])/(_transmissionsCorrect / T[0]), "conf"
    else:
        print "No successful transmissions!"
    print (_transmissionsCorrect / T[0]) / (elapsed_time / T[0]), "conf"
    
    # TODO - Confidence intervals

# Executes transmissions over given period of time.
#
# @param A: You can assume the feedback time is 500 bit time units.
# @param K: The number of blocks.
# @param F: Size of the frame in number of bits. Assume 4000 bits.
# @param e: Probability that bit is in error
# @param R: Length of simulation in bit time units.
# @param rnd: The random number generator to use
#
# @returns Elapsed Time, Total Frames sent, Total Correct Frames sent
def performTransmissions(A, K, F, e, R, rnd):
    
    f = Frame.Frame(K, F);
    
    elapsed_time = 0
    frames_total = 0
    frames_correct = 0
    
    while elapsed_time < R:
        elapsed_time += A
        frames_total += 1

        if f.performErrorChance(e, rnd):
            # Successful transmission
            frames_correct += 1
    
    return [elapsed_time, frames_total, frames_correct]

main(50, 4, 4000, .00005, 5000, [500, 100, 3, 5, 2, 8]);
