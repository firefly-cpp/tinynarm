from unittest import TestCase
from tinynarm import TinyNarm
import os

class TestDataset(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "datasets", "Abalone.csv")
        narm = TinyNarm("datasets/Abalone.csv", 3, 0.70)
        narm.create_intervals()
        self.intervals = narm.feat

    def test_intervals_correct(self):
        interval0 = ['F', 'I', 'M']
        interval1 = [0.075, 0.26, 0.445, 0.6299999999999999]

        self.assertEqual(self.intervals[0].intervals, interval0)
        self.assertEqual(self.intervals[1].intervals, interval1)


