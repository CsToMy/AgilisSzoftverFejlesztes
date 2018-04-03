import unittest

from fuzzer.fuzzer import Fuzzer

class Test(unittest.TestCase):
    def test_basic(self):
        print("I'm running :)")
        f = Fuzzer('{"a":1}')
        f.fuzz()
        f.fuzz()

if __name__ == '__main__':
    unittest.main()
