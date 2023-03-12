from unittest import TestCase
from tinynarm import TinyNarm
import os


class TestTinyNarm(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "Abalone.csv")
        narm = TinyNarm("new_dataset.csv")
        narm.create_features()
        narm.cartography()
        narm.create_rules()

        self.rules = narm.rules

    def test_generated_rules(self):
        assert len(self.rules) > 0, 'Not enough rules generated'

    #    interval0 = ['F', 'I', 'M']
    #    self.assertEqual(self.intervals[0].intervals, interval0)

    #def test_numerical_intervals(self):
    #    interval1 = [0.075, 0.32166666666666666, 0.5683333333333334, 0.815]
    #    self.assertEqual(self.intervals[1].intervals, interval1)

     #   interval2 = [0.055, 0.25333333333333335, 0.45166666666666666, 0.65]
      #  self.assertEqual(self.intervals[2].intervals, interval2)

      #  interval3 = [0.0, 0.37666666666666665, 0.7533333333333333, 1.13]
      #  self.assertEqual(self.intervals[3].intervals, interval3)
