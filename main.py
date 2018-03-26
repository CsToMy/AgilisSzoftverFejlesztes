#!/usr/bin/env python3.6
import argparse
import time
import os
import logging
from fuzzer import *
import pycurl
import json
from StringIO import StringIO
###### Logging ######
if not os.path.exists('log'):
    os.mkdir('log')
log = logging.getLogger("Main")
filename = "log/log_file_" + str(time.ctime()).replace(' ', '_').replace(':', '-') + '.log'
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')


def authenticate(url):
    buffer = StringIO()
    payload=json.dumps({'password':'asdf@1234', 'type':'normal',"username":"daniel.kovacs"})
    c=pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS,payload)
    c.setopt(pycurl.HTTPHEADER, ["Content-type: application/json"])
    c.setopt(c.WRITEDATA, buffer)
    #print(payload+'\n')
    c.perform()
    auth_token=json.loads(buffer.getvalue())['auth_token']
    statuscode=c.getinfo(pycurl.HTTP_CODE)
    #print json.loads(buffer.getvalue(), indent=4, separators=(',', ': '))
    return auth_token

def queryData(token, url, payload):
    buffer = StringIO()
    c=pycurl.Curl()
    c=pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS,payload)
    c.setopt(pycurl.HTTPHEADER, ["Content-type: application/json","Authorization: Bearer "+token])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    result = buffer.getvalue()
    statuscode=c.getinfo(pycurl.HTTP_CODE)
    return result

def main(json, url, iterations):
    # TODO
    pass


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="JSON Fuzzer main")
        parser.add_argument("-j", "--json", action="store", default=None, help="correct JSON file path")
        parser.add_argument("-u", "--url", action="store", default=None, help="webserver URL")
        parser.add_argument("-i", "--iterations", action="store", default=None, help="number of iterations")
        args = parser.parse_args()
        log.info("Correct JSON file path: " + args.json)
        log.info("Webserver URL: " + args.url)
        log.info("Number of iterations: " + args.iterations)
        fuzzer = Fuzzer()
        auth_token=authenticate(args.url+'/auth')
        payload=json.dumps({'description':'Teszt','name':'Teszt Projekt'})
        queryData(auth_token,args.url+'/projects',payload)
	#main(args.json, args.url, args.iterations)
    except Exception as e:
        print(e)
