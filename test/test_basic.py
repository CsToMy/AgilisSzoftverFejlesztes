import unittest
# import json
# import pycurl

# from fuzzer.main import authenticate, queryData, Fuzzer
from fuzzer.main import Fuzzer


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

    # def test_auth(self):
    #     url = "10.152.106.224/api/v1/auth"
    #     token = authenticate(url)
    #     self.assertNotEqual(token, "")
    #     url = "10.152.106.224"
    #     with self.assertRaises(json.decoder.JSONDecodeError):
    #         authenticate(url)
    #     url = "MAX POWER"
    #     with self.assertRaises(pycurl.error):
    #         authenticate(url)
    #
    # def test_query(self):
    #     url = "10.152.106.224/api/v1/auth"
    #     token = authenticate(url)
    #     statuscode, result = queryData(token, url + '/projects', Fuzzer('{"a":1}').fuzz())
    #     self.assertNotEqual("", result)
    #     print(statuscode)
    #     self.assertGreater(int(statuscode), 99)
    #     self.assertLess(int(statuscode), 600)


if __name__ == '__main__':
    unittest.main()
