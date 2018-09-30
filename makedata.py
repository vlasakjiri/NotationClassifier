import os
import pickle
import random

import music21
import numpy as np


def GetPitchCounts(pitches):
    for pitch in pitches:
        pitchCount[pitch.step] += 1
    values = np.array(list(pitchCount.values()), dtype="float")
    values /= values.max()
    return values


def serialize():
    os.chdir("data")
    for composer in composers:
        label = composerNames[composer[0]]
        os.chdir(label)
        with open("pitches.dat", "wb+") as f:
            pickle.dump(composer[1], f)
        os.chdir("..")
    os.chdir("..")


numScores = 80
composerNames = ["bach", "trecento"]

pitchCount = {"C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "A": 0, "B": 0}

scorePaths = [
    random.sample(music21.corpus.getComposer(composer), numScores)
    for composer in composerNames
]

composers = []
composerPitches = []
for j, composer in enumerate(scorePaths):
    composerPitches = []
    for score in composer:
        score = music21.corpus.parse(score)
        key = score.analyze("key")
        i = music21.interval.Interval(key.tonic, music21.note.Note('C').pitch)
        score = score.transpose(i)
        pitchCounts = GetPitchCounts(score.pitches)
        composerPitches.append(pitchCounts)
    composers.append((j, composerPitches))

serialize()