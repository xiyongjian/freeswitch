#!/usr/bin/env python3

# from https://pythonprogramminglanguage.com/speech-recognition/

import speech_recognition as sr
import sys
from os import path

if len(sys.argv) <= 1 :
    # load audio file from same directory
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "xyj01x.wav")
else :
    AUDIO_FILE = sys.argv[1]
    
print ('recog audio file : ', AUDIO_FILE)

# use audio file as input
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Google Speech Recognition
try:
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


