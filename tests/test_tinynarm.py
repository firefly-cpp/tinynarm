from unittest import TestCase
from tinynarm import TinyNarm
import os


class TestTinyNarm(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "new_dataset.csv")
        self.narm = TinyNarm(filename)
        self.narm.create_rules()

        self.rules = self.narm.rules

    def test_generated_rules(self):
        assert len(self.rules) > 0, 'Not enough rules generated'

    def test_generated_features(self):
        assert len(self.narm.feat) > 0, 'No features generated'


