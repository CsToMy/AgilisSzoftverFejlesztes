#!/usr/bin/env python3.5
import argparse
import time
import os
import logging
from fuzzer import *

###### Logging ######
if not os.path.exists('log'):
    os.mkdir('log')
log = logging.getLogger("Main")
filename = "log/log_file_" + str(time.ctime()).replace(' ', '_').replace(':', '-') + '.log'
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')


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
        main(args.json, args.url, args.iterations)
    except Exception as e:
        print(e)
