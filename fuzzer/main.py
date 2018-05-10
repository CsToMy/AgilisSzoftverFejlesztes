#!/usr/bin/env python3.6
import argparse
import time
import os
import logging
from fuzzer import *
import pycurl
import json
from io import BytesIO


# ##### Logging ######
if not os.path.exists('log'):
    os.mkdir('log')
log = logging.getLogger("Main")
filename = "log/log_file_" + str(time.ctime()).replace(' ', '_').replace(':', '-') + '.log'
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')


def authenticate(url):
    buffer = BytesIO()
    payload = json.dumps({'password': 'asdf@1234', 'type': 'normal', 'username': 'user1'})
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS, payload)
    c.setopt(pycurl.HTTPHEADER, ["Content-type: application/json"])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    auth_token = json.loads(buffer.getvalue().decode())['auth_token']
    log.info("Authentication successfully")
    print("Authentication successfully")

    return auth_token


def queryData(token, url, payload):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS, payload)
    c.setopt(pycurl.HTTPHEADER, ["Content-type: application/json", "Authorization: Bearer " + token])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    result = buffer.getvalue().decode()
    statuscode = c.getinfo(pycurl.HTTP_CODE)
    return (statuscode, result)


def main(payload, url, auth_token):
    statuscode, result = queryData(auth_token, url + '/projects', payload)
    print("The query statuscode is " + str(statuscode) + "\n")
    print(json.dumps(json.loads(result), indent=4, sort_keys=True))


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="JSON Fuzzer main")
        parser.add_argument("-j", "--json", action="store", default=None, help="correct JSON file path")
        parser.add_argument("-u", "--url", action="store", default=None, help="webserver URL")
        parser.add_argument("-i", "--iterations", action="store", default=None, help="number of iterations")
        args = parser.parse_args()

        log.info("Correct JSON file path: %s" % args.json)
        log.info("Webserver URL: %s" % args.url)
        log.info("Number of iterations: %s" % args.iterations)

        data = json.dumps(json.load(open(args.json)))
        fuzzer = Fuzzer(data)

        auth_token = authenticate(args.url + '/auth')

        for _ in range(int(args.iterations)):
            fuzzed = fuzzer.fuzz()
            log.info("Fuzzed JSON: " + fuzzed)
            main(fuzzed, args.url, auth_token)
    except Exception as e:
        raise e
