#
# CMPUT 313 - Computer Networks
# Assignment 1 - A Study of Combined Error Detection and Error Correction Scheme
#
# Author: Jesse Tucker & James Finlay
#

import Frame
import math
import random
import sys

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

    _throughputResults = []
    _averageTransmissions = []

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
        #print "---------------------"
        #print "Trial", trial
        #print "Elapsed time:", elapsed_time
        #print "Total frames:", frames_total
        #print "Correct frames:", frames_correct

        _throughputResults.append(frames_correct * F / float(R))
        if frames_correct > 0:
            _averageTransmissions.append(frames_total / float(frames_correct))

        _trialNumber = _trialNumber + 1

    t_value = 2.776 # this corresponds to a 95% confidence interval

    throughput_mean = sum(_throughputResults) / float(T[0])
    throughput_stdDev = calcStandardDeviation(_throughputResults, throughput_mean)
    throughput_leftInverval = throughput_mean - t_value * throughput_stdDev / math.sqrt(T[0])
    throughput_rightInverval = throughput_mean + t_value * throughput_stdDev / math.sqrt(T[0])

    averageTransmissions_mean = sum(_averageTransmissions) / float(T[0])
    averageTransmissions_stdDev = calcStandardDeviation(_averageTransmissions, averageTransmissions_mean)
    averageTransmissions_leftInverval = averageTransmissions_mean - t_value * averageTransmissions_stdDev / math.sqrt(T[0])
    averageTransmissions_rightInverval = averageTransmissions_mean + t_value * averageTransmissions_stdDev / math.sqrt(T[0])

    print "\n---------------------\n"
    # Output - what's actually expected
    print A,K,F,e,R,T, "\n"
    print "An average of " + str(averageTransmissions_mean) + " transmissions were needed per frame with a 95% confidence interval of : [" + str(averageTransmissions_leftInverval) + "," + str(averageTransmissions_rightInverval) + "]"
    print "An average throughput of " + str(throughput_mean) + " bits/time_unit was achieved during the trial with a 95% confidence interval of : [" + str(throughput_leftInverval) + "," + str(throughput_rightInverval) + "]"

def calcStandardDeviation(arr, mean):
    result = 0
    for val in arr:
        result += (val - mean) * (val - mean)

    result = math.sqrt(result / (len(arr) - 1))
    return result

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
        elapsed_time += A + F # transmission time is the feedback time + 1 time unit per bit
        frames_total += 1

        if f.performErrorChance(e, rnd):
            # Successful transmission
            frames_correct += 1

    return [elapsed_time, frames_total, frames_correct]

if(len(sys.argv) > 6):

    A = int(sys.argv[1])
    K = int(sys.argv[2])
    F = int(sys.argv[3])
    e = float(sys.argv[4])
    R = int(sys.argv[5])

    T = map(int, sys.argv[6:])

    main(A, K, F, e, R, T);
else:
    print "Invalid Arguments passed in! Please pass in the format :"
    print "<FeedbackTime> <Number of Blocks> <Size of frame in bits> <probability of failure> <Length of simulation> <Number of Trials> <seed for trial 1> <seed for trial 2> ... <seed for trial N"
