from unittest import TestCase
from tinynarm import TinyNarm
from niaarm import Dataset
import os


class TestDataset(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "Abalone.csv")
        dataset = Dataset(filename)
        self.transactions = dataset.transactions.to_numpy()

    def test_len_dataset_correct(self):
        self.assertEqual(len(self.transactions), 4177)
