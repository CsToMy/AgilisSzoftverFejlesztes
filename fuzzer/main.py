#!/usr/bin/env python3.6
import argparse
import time
import os
import logging
from fuzzer.fuzzer import Fuzzer
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
    log.info("Authentication successful")
    print("Authentication successful")

    return auth_token


def queryData(token, url, payload):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS, payload)
    if token is not None:
        c.setopt(pycurl.HTTPHEADER, ["Content-type: application/json", "Authorization: Bearer " + token])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    if c.getinfo(pycurl.HTTP_CODE) == 500:
        result = "{}"
    else:
        result = buffer.getvalue().decode()
    statuscode = c.getinfo(pycurl.HTTP_CODE)
    return (statuscode, result)


def main(payload, url, auth_token):
    if auth_token is not None:
        statuscode, result = queryData(auth_token, url + '/projects', payload)
        print("The query statuscode is " + str(statuscode) + "\n")
        print(json.dumps(json.loads(result), indent=4, sort_keys=True))
    else:
        statuscode, result = queryData(None, url, payload)
        print("The query statuscode is " + str(statuscode) + "\n")
        print(json.dumps(json.loads(result), indent=4, sort_keys=True))


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="JSON Fuzzer main")
        parser.add_argument("-j", "--json", action="store", default=None, help="correct JSON file path", required=True)
        parser.add_argument("-u", "--url", action="store", default=None, help="webserver URL", required=True)
        parser.add_argument("-i", "--iterations", action="store", default=None, help="number of iterations",
                            required=True)
        parser.add_argument("-n", action="store_true", default=False, help="Is it necessary to authenticate?"
                                                                           " Default: Yes")
        args = parser.parse_args()

        log.info("Correct JSON file path: %s" % args.json)
        log.info("Webserver URL: %s" % args.url)
        log.info("Number of iterations: %s" % args.iterations)

        data = json.dumps(json.load(open(args.json)))
        fuzzer = Fuzzer(data)

        if args.n:
            print("No need to authenticate")
            auth_token = None
        else:
            auth_token = authenticate(args.url + '/auth')

        for _ in range(int(args.iterations)):
            fuzzed = fuzzer.fuzz()
            log.info("Fuzzed JSON: " + fuzzed)
            main(fuzzed, args.url, auth_token)
    except Exception as e:
        raise e
