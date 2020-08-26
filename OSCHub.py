import numpy as np
import pandas as pd
import os
import time
import pythonosc

if __name__ == "__main__":

    # read csv data
    eeg_data = pd.read_csv('rec02.csv', delimiter=";", decimal=",")
    eeg_data = eeg_data.astype(float)
    eeg_data_clean = eeg_data.drop(eeg_data.columns[8:], axis=1)

    #Set up osc client
    ip = "127.0.0.1"
    port = 5510 #'faust default'
    client = SimpleUDPClient(ip, port)  # Create client

    #read from file and create osc message
    for i in range(eeg_data_clean.shape[0]):
        row = eeg_data_clean.iloc[i,:].values #prints row as array
        time.sleep(1) #delay
        for j in range(len(row)):
            msg = "/BrainwaveInstrument/Synth/Channel_%d/modFreq" % (j+1) #reads each value of a row and creates osc message with that value
            client.send_message(msg, row[j])
