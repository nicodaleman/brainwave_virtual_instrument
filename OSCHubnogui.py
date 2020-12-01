#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os
import time
from pythonosc import udp_client
from pythonosc.udp_client import SimpleUDPClient


# In[ ]:


eeg_data = pd.read_csv('rec02.csv', delimiter=";", decimal=",")
eeg_data = eeg_data.astype(float)
eeg_data_clean = eeg_data.drop(eeg_data.index[0:4])

ip = "127.0.0.1"
port = 5510 #'faust default'
client = SimpleUDPClient(ip, port)  # Create client

for i in range(eeg_data_clean.shape[0]):
    row = eeg_data_clean.iloc[i,:].values #prints row as array
    time.sleep(1) #delay
    for j in range(8):
        msg_freq = "/BrainwaveVirtualInstrument/Synth/Channel_%d/modFreq" % (j+1) #reads each value of a row and creates osc message with that value   
        value_freq = (20 + ((40*int(((j+1) * 0.5)+0.5)))) + row[j]
        client.send_message(msg_freq, value_freq )
        #print (msg_freq, value_freq)

    for k in range (8):
        msg_pan = "/BrainwaveVirtualInstrument/Synth/Channel_%d/pan" % (k+1)
        value_pan = (row[int(k/2)+2]) * 0.25 #scale 0.5 for 0-1 pan range, scale 0.25 for skew data values
        client.send_message(msg_freq, value_freq )
        #print (msg_pan, value_pan)


# In[ ]:





# In[ ]:




