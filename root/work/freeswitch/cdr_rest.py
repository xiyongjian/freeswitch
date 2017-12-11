
import requests
import json

#===============================================================================
# post_cdr : call REST API post cdr record
#===============================================================================
def post_cdr(url, payload) :
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == '__main__' :
    cdr = {}
    cdr['DOMAIN'] = 'bluemsp'
    cdr['FROM_USER_ID'] = 1234
    cdr['DURATION'] = 300
    cdr['TO_USERS'] = [{"TO_USER_ID" : 1001}, {"TO_USER_ID" : 1002}]

    payld = json.dumps(cdr, indent=4)
    print("cdr json payld : " + payld)

    url = "http://192.168.151.101:8080/ngDesk-fsapi/cdr"
    response = requests.post(url, data=payld) 
    print("post result status : %d" % response.status_code)
    print("post result jso : %s" % json.dumps(response.json(), indent=4))




