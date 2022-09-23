import unittest
from my_server import MyServer


class AggregatorTest(unittest.TestCase):
    def setUp(self):
        self.server = MyServer()

    def test_execute(self):
        self.server.start()
