from unittest import TestCase
from tinynarm import TinyNarm
from tinynarm.discretization import Discretization
from tinynarm.item import Item
from niaarm import Dataset
import os

# a series of tests utilizing sportydatagen.csv dataset

# duration,distance,average_hr,average_altitude,max_altitude,calories,ascent,descent
# 54.0,8.869410156,117,418.3103138,483.2000122,374,245.8000183,208.2000122
# 54.43333333,14.19421973,122,477.5547162,529.4000244,316,122.0002441,86.40023804
# 67.63333333,24.59965039,149,98.83924418,223.1999969,499,357.7999897,349.3999901
# 70.41666667,0.0,117,94.38214476,94.80000305,473,0.800003052,2.800003052
# 74.13333333,17.48390039,97,125.3543787,175.6000061,263,107.0,112.7999954

class TestSportydatagenDataset(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "sportydatagen.csv")
        dataset = Dataset(filename)

        self.transactions = dataset.transactions.to_numpy()
        self.features = dataset.features

    def test_len_dataset_correct(self):
        assert len(self.transactions) == 5, "Dataset is not correct"

    def test_len_features(self):
        assert len(self.features) == 8, "There should be 8 features"

    def test_features_name(self):
        names = ['duration', 'distance', 'average_hr', 'average_altitude', 'max_altitude', 'calories', 'ascent', 'descent']
        dataset_names = []
        for feat in self.features:
            dataset_names.append(feat.name)

        assert names == dataset_names, "Name of features not correct"

    def test_features_dtypes(self):
        types = ["float", "float", "int", "float", "float", "int", "float", "float"]
        dataset_types = []
        for feat in self.features:
            dataset_types.append(feat.dtype)

        assert types == dataset_types, "Datatypes not correct"
