from freeswitch import *

import speech_recognition as sr
import sys
from os import path

import json
from datetime import datetime

def handler(session,args):
    wav_file = "/tmp/recording.wav"
    consoleLog("info", "using wave file %s to recogn-replay\n" % wav_file)

    consoleLog("info", "tts.py started")
    session.execute("set","tts_engine=flite")
    session.execute("set","tts_voice=kal")
    consoleLog("info", "setup variables")
    consoleLog("info", "start speak")
    session.execute("speak","This is testing for TTS working properly")

    msg = ""
    while "quit" not in msg :
        session.execute("speak","say something, let me guess what you said...")
        rtn = session.recordFile(wav_file, 20, 500, 3);

        r = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio = r.record(source)  # read the entire audio file

        result = ""
        try:
            result = r.recognize_google(audio)
            consoleLog("info", "call_recogn recogn_file - Google Speech Recognition result : %s\n" % str(result))
        except sr.UnknownValueError:
            consoleLog("info", "call_recog recogn_file - Google Speech Recognition could not understand audio\n")
        except sr.RequestError as e:
            consoleLog("info", "call_recog recogn_file - Could not request results from Google Speech Recognition service; {0}\n".format(e))

        session.execute("speak","you just said something like : " + str(result))
        session.execute("sleep","1000")
        msg = str(result);





