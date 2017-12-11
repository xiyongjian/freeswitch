
from freeswitch import *

import speech_recognition as sr
import sys
from os import path

import requests
import json
from datetime import datetime

rec_file = "";
cdr_api_url = "http://192.168.151.101:8080/ngDesk-fsapi/cdr"

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
    result = ""
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
    return result


def handler(session,args):
    global rec_file
    rec_file = session.getVariable("recording_file")
    # freeswitch.consoleLog("info", "recording_file: %s\n" % rec_file)
    consoleLog("info", "call_recogn handler - recording_file: %s\n" % rec_file)
	
    consoleLog("info", "call_recogn handler - setup HangupHook to recognite speech\n")
    # result = session.setHangupHook(hangup_hook)
    # -- seems no use -- #session.setHangupHook(hangup_hook)
    consoleLog("info", "call_recogn handler - SKIP setup HangupHook DONE\n")
    consoleLog("info", "call_recogn handler - session %s\n" % str(dir(session)).replace(",", ",\n"))


def fsapi(session,stream,event,args): 
    rec_file = session.getVariable("recording_file")
    consoleLog("info", "call_recogn fsapi - recogn recording_file: %s\n" % rec_file)
    transcript = recogn_file(rec_file)

    # prepare JSON payload
    cdr = {}
    cdr['DOMAIN'] = session.getVariable("domain")
    cdr['DOMAIN_NAME'] = session.getVariable("domain_name")
    cdr['FROM_USER_ID'] = session.getVariable("caller_id_number")

    to_users = [];
    to_users.append({'TO_USER_ID' : session.getVariable("destination_number")})
    cdr['TO_USERS'] = to_users
    
    recording_time = session.getVariable("recording_time")
    cdr['DATE_CREATED'] = recording_time
    
    d00 = datetime.strptime(recording_time, '%Y-%m-%d-%H-%M-%S')
    d01 =  datetime.now();
    cdr['DURATION'] = str(int((d01-d00).total_seconds()))
    
    cdr['TRANSCRIPT'] = transcript

    payld = json.dumps(cdr, indent=4)

    # write JSON to file first
    with open(rec_file + ".json", 'w') as the_file:
        the_file.write(payld)

    # post JSON to REST API (CDR)
    consoleLog("info", "json payload : %s\n" % payld)
    consoleLog("info", "post json to url : %s" % cdr_api_url)
    response = requests.post(cdr_api_url,data=payld)
    consoleLog("info", "post result status : %d" % response.status_code)
    consoleLog("info", "post result json : %s" % json.dumps(response.json(), indent=4))


