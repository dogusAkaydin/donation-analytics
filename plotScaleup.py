#!/usr/bin/env python3
import matplotlib.pyplot as plt
n      = [1       , 10       , 100      , 1e3     , 1e4    , 1e5    , 1e6   , 10e6] 
nValid = [1       , 10       , 100      , 992     , 9237   , 96561  , 972183, 10e6] 
t      = [0.004179, 0.0138431, 0.0878222, 0.804581, 7.88627, 77.3247, 791.32, 6387]   
tOn    = [0.0008  , 0.008    , 0.08     , 0.8     , 8.0    , 80.0   , 800   , 8e3 ] 
plt.figure(1)
plt.xlabel('Number of Records')
plt.ylabel('Wall Clock Time [s]')
plt.loglog(n, t, 'o-k', label='this approach')
plt.loglog(n, tOn, '-.k', label='O(n)')
#plt.loglog(nValid, t, '.-r')
plt.legend()
plt.xticks(n, ['1', '10', '100', '1k', '10k', '100k', '1M', '10M'])
#plt.xlim(0,10e3)
#plt.ylim(0,8e3)
plt.show(1)

