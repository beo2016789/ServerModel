import os
import librosa
import numpy as np
import math
import pickle
import warnings
warnings.filterwarnings("ignore")

labels = ["BK", "turnOff", "turnOn"]
commands = ["hey BK", "turn off", "turn on"]

def removeSilence(audio):
    clip = librosa.effects.trim(audio, top_db = 10)
    return clip[0]

def get_mfcc(file_path):
    y, sr = librosa.load(file_path)
    y = removeSilence(y)
    hop_length = math.floor(sr*0.01)
    win_length = math.floor(sr*0.025)
    mfcc = librosa.feature.mfcc(
        y, sr, n_mfcc=12, n_fft = 1024, hop_length=hop_length, win_length=win_length,
    )
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1, 1))
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)

    X = np.concatenate([mfcc, delta1, delta2], axis=0)
    return X.T

model = {}
for key in labels:
    name = f"server_model/models/models_train_model_{key}.pkl"
    with open(name, 'rb') as file:
        model[key] = pickle.load(file)

def getPredict(filePath):
    record_mfcc = get_mfcc(filePath)
    scores = [model[label].score(record_mfcc) for label in labels]
    index = np.argmax(scores)
    return commands[index]