
from freeswitch import *

import speech_recognition as sr
import sys
from os import path


rec_file = "";

def hangup_hook(uuid) :
    consoleLog("info", "call_recogn hangup_hook - uuid : %s\n" % str(uuid))
    recogn_file(rec_file)

def recogn_file(wav_file) :
    consoleLog("info", "call_recogn recogn_file - start recognite speech : %s\n" % wav_file)
    r = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = r.record(source)  # read the entire audio file

    rsl_file = wav_file + ".txt"
    
    # recognize speech using Google Speech Recognition
    try:
	result = r.recognize_google(audio)
        consoleLog("info", "call_recogn recogn_file - Google Speech Recognition result : %s\n" % str(result))
        consoleLog("info", "call_recogn recogn_file - write result to : %s\n" % rsl_file)
        with open(rsl_file, 'w') as the_file:
            the_file.write(str(result))
    except sr.UnknownValueError:
        consoleLog("info", "call_recog recogn_file - Google Speech Recognition could not understand audio\n")
    except sr.RequestError as e:
        consoleLog("info", "call_recog recogn_file - Could not request results from Google Speech Recognition service; {0}\n".format(e))


def handler(session,args):
    global rec_file
    rec_file = session.getVariable("recording_file")
    # freeswitch.consoleLog("info", "recording_file: %s\n" % rec_file)
    consoleLog("info", "call_recogn handler - recording_file: %s\n" % rec_file)
	
    consoleLog("info", "call_recogn handler - setup HangupHook to recognite speech\n")
    # result = session.setHangupHook(hangup_hook)
    session.setHangupHook(hangup_hook)
    consoleLog("info", "call_recogn handler - setup HangupHook DONE\n")
    consoleLog("info", "call_recogn handler - session %s\n" % str(dir(session)).replace(",", ",\n"))


def fsapi(session,stream,event,args): 
    rec_file = session.getVariable("recording_file")
    consoleLog("info", "call_recogn fsapi - recogn recording_file: %s\n" % rec_file)
    recogn_file(rec_file)
