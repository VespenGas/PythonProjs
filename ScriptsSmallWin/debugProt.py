# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 19:20:30 2022

@author: Evgeny
"""

from scipy import signal
import numpy
import math
import ctypes
import matplotlib.pyplot as plt
saw_freq_coeff = 9 #frequency coefficient of sawtooth waveform (9-15)
saw_amp_coeff = 1.2 # relative coefficient of sawtooth waveform amplitude
out_V_coeff = 5 # peak output voltage of PWM
sample_rate = 1000 
u = numpy.linspace(0,0.02,sample_rate)
base_freq = 50.0 #Hz
T = (1.0/base_freq)*1000000.0 #us
delay_per_iteration = T/u.size #us
#--------------------------------------------------------------------------------
def micros():
        "return a timestamp in microseconds (us)"
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()  #get ticks on the internal 2MHz PC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))   #get the actual freq. of the internal 2MHz PC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
        t_us = tics.value*1e6/freq.value  #calculate the current main timer value
        return t_us
#---------------------------------------------------------------------------------
# a function that delays the execution of next line of code by given amount of delay per iteration
def delayMicroseconds(delay_us):
    t_start = micros()
    while (micros() - t_start < delay_us):
      pass #do nothing 
    return 
#---------------------------------------------------------------------------------
# function that generates the output script
def PWMFunc(saw_freq_coeff, saw_amp_coeff, out_V_coeff, sample_rate):
    sin_freq = 50 #Hz, unchanged
    sin_freq = sin_freq/1000
    t = numpy.linspace(0,20,sample_rate) #time in ms (1 period of sin)
    v1 = numpy.zeros(sample_rate)
    v2 = numpy.zeros(sample_rate) #arrays being initialised
    V = -1*saw_amp_coeff*signal.sawtooth(2.0*math.pi*sin_freq*saw_freq_coeff*t-(math.pi/2.0),0.5)
    #^sawtooth waveform using scipy
    x = numpy.sin(2.0*math.pi*sin_freq*t) #sin wave
    neg_x = -1*x #-sin wave
    for i in range(0,t.size): #sin comparator
        if V[i]>=x[i]:
            v1[i] = 0 
        else:
            v1[i] = 1*out_V_coeff
    for i in range(0,t.size): #-sin comparator
        if V[i]>=neg_x[i]:
            v2[i] = 0
        else:
            v2[i] = 1*out_V_coeff
    fin = v1-v2 #subtraction of 2 comparator signals
    return fin #final unipolar PWM
#---------------------------------------------
out = PWMFunc(15,1.2,5,u.size)
out2 = out
#time delay confirmation
actual_delay = []
prev_timer = micros()
delay_graph = []
sum1 = 0
for i in range(0,u.size):
    prev_timer = micros()
    print('Out is:\n')
    print(out2[i])
    delayMicroseconds(delay_per_iteration)
    time_diff = micros()-prev_timer
    print(f'Delay is {time_diff} us')
    delay_graph.append(time_diff)
    sum1 = sum1 + time_diff
plt.plot(delay_graph)
print('Avg delay is: ')
print(sum1/int(u.size))

