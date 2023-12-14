import gin
import os
import cv2
import torch

import numpy as np

from loguru import logger
from rich.progress import track
from torch.utils.data import Dataset
from torchvision import transforms
from utils import check_and_retrieveVocabulary

data = np.load('vocab/GrandStaff_bekrnw2i.npy', allow_pickle=True)


print((data.item()))
print(len(data.item()))

krnlines = []
Y = []

with open('/Users/hodori/Desktop/grandstaff/beethoven/piano-sonatas/sonata01-1/original_m-70-75.bekrn') as krnfile:
    krn = krnfile.read()
    krn = krn.replace(" ", " <s> ")
    krn = krn.replace("·", " ")
    lines = krn.split("\n")
    for line in lines:
        line = line.replace("\t", " <t> ")
        line = line.split(" ")
        if len(line) > 1:
            line.append("<b>")
            krnlines.append(line)
    Y.append(sum(krnlines, []))

mididict = {'c': 60, 'd': 62, 'e': 64, 'f': 65, 'g': 67, 'a': 69, 'b': 71}
def notetomidi(note, accidental):
    '''
    Given a note in the bekrn notation, and an accidental in the bekrn
    notation, converts it to midi pitch class.
    '''
    # midi middle c 'c' is 60
    midi = mididict[note[0].lower()]
    octave = 12;
    if note.isupper():
        octave *= -1
        midi += octave

    if len(note) > 1:
        midi += (len(note) - 1) * octave

    for accidental_component in accidental:
        if accidental_component == '-':
            midi -= 1
        elif accidental_component == '#':
            midi += 1

    return midi

print(notetomidi('c'))
print(notetomidi('cc'))
print(notetomidi('D'))
print(notetomidi('DD'))

currclef = [0 for i in range(2)]
currkey = [[0, 0, 0, 0, 0, 0, 0] for i in range(2)]
currmods = []

for krnline in krnlines:
    newline = ""
    voice = 0
    for token in krnline:
        if '*k' in token:
            pass
        elif token == '<t>':
            voice += 1
            newline += '\t'
        elif token == '*^':
            pass
        elif token[0].lower() in mididict:
            newline += str(notetomidi(token))
        elif token == 'X':
            # display the accidental of the current note no matter what

    print(newline)