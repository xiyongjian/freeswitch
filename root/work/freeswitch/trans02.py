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

# GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""
{
KEY HERE
}
"""

# recognize speech using Google Speech Recognition
try:
    # print("Google Speech Recognition thinks you said " + r.recognize_google(audio, key="google key here"))
    # print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    # print("Google Speech Recognition thinks you said " + r.recognize_google(audio, key="711580026403-1ii01eu76bo3n232pj4ubbgmarthsnov.apps.googleusercontent.com711580026403-1ii01eu76bo3n232pj4ubbgmarthsnov.apps.googleusercontent.com", show_all=True))
    # print("Google Speech Recognition thinks you said " + r.recognize_google(audio, credentials_json="711580026403-1ii01eu76bo3n232pj4ubbgmarthsnov.apps.googleusercontent.com711580026403-1ii01eu76bo3n232pj4ubbgmarthsnov.apps.googleusercontent.com", show_all=True))

    # result = r.recognize_google(audio)
    # result = r.recognize_google(audio, key="8b15aac9b5ad5463a741a70a049d4ed7cc211dc8")
    result = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, show_all=True)
    print("Google Speech Recognition thinks you said : " + str(result))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


