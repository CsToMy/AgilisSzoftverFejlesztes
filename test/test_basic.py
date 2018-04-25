import unittest
import json
import pycurl
import os
from fuzzer.main import authenticate, queryData, Fuzzer


class Test(unittest.TestCase):
    def test_basic(self):
        print("I'm running :)")
        f = Fuzzer('{"a":1}')
        f.fuzz()
        f.fuzz()

    def test_fuzzing(self):
        fbase = '{"a":1}'
        f = Fuzzer(fbase)
        for x in range(5):
            f2 = f.fuzz()
            self.assertNotEqual(fbase, f2)
            fbase = f2

    def test_auth(self):
        url = "152.66.209.124/api/v1/auth"
        token = authenticate(url)
        self.assertNotEqual(token, "")
        url = "152.66.209.124"
        with self.assertRaises(json.decoder.JSONDecodeError):
            authenticate(url)
        url = "MAX POWER"
        with self.assertRaises(pycurl.error):
            authenticate(url)

    def test_query(self):
        url = "152.66.209.124/api/v1/auth"
        token = authenticate(url)
        data = json.dumps(json.load(open(os.path.join('test','json.txt'))))
        statuscode, result = queryData(token, url + '/projects', Fuzzer(data).fuzz())
        self.assertNotEqual("", result)
        self.assertGreater(int(statuscode), 99)
        self.assertLess(int(statuscode), 600)


if __name__ == '__main__':
    unittest.main()
