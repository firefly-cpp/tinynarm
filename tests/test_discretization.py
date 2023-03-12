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


class TestSportydatagenDiscretizationA(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "sportydatagen.csv")
        self.dataset = Discretization(filename, 3)
        self.transactions = self.dataset.generate_dataset()

    def test_len_items(self):
        assert len(self.dataset.feat) == 8, "Not correct number of features"
        # assert len(self.transactions) == 5, "Dataset is not correct"

    def test_intervals_duration(self):
        # first interval (54.0, 60.71)
        # second interval (60.71, 67.42)
        # third interval (67.42, 74.13)
        intervals = [54.0, 60.71111111, 67.42222222, 74.13333333]
        interval_duration = self.dataset.feat[0].intervals
        assert intervals == interval_duration, "Not correct interval for duration feature"

    def test_intervals_avhr(self):
        intervals = [97.0, 114.33333333333333, 131.66666666666666, 149.0]
        interval_avhr = self.dataset.feat[2].intervals
        assert intervals == interval_avhr, "Not correct interval for average_hr feature"

    def test_len_generated_transactions(self):
        assert len(self.transactions) == 5, "The correct lenght is 5"

    def test_discrete_classes(self):
        classes_duration = []
        classes_average_hr = []

        duration = [
            'interval_1',
            'interval_1',
            'interval_3',
            'interval_3',
            'interval_3']
        average_hr = [
            'interval_2',
            'interval_2',
            'interval_3',
            'interval_2',
            'interval_1']

        for i in range(len(self.transactions)):
            classes_duration.append(self.transactions[i][0])
            classes_average_hr.append(self.transactions[i][2])

        assert classes_duration == duration, "Not correct"
        assert classes_average_hr == average_hr, "Not correct"


class TestSportydatagenDiscretizationB(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "sportydatagen.csv")
        self.dataset = Discretization(filename, 5)
        self.dataset.create_intervals()
        self.transactions = self.dataset.generate_dataset()

    def test_intervals_duration(self):
        # first interval (54.0, 58.02)
        # second interval (58.02, 62.05)
        # third interval (62.05, 66.07)
        # fourth interval (66.07, 70.10)
        # fifth interval (70.10, 74.13)
        intervals = [
            54.0,
            58.026666666,
            62.053333332,
            66.079999998,
            70.106666664,
            74.13333333]
        interval_duration = self.dataset.feat[0].intervals
        assert intervals == interval_duration, "Not correct interval for duration feature"

    def test_intervals_avhr(self):
        intervals = [97.0, 107.4, 117.8, 128.2, 138.6, 149.0]
        interval_avhr = self.dataset.feat[2].intervals
        assert intervals == interval_avhr, "Not correct interval for average_hr feature"

    def test_discrete_classes_scenarioB(self):
        classes_duration = []
        classes_average_hr = []

        duration = [
            'interval_1',
            'interval_1',
            'interval_4',
            'interval_5',
            'interval_5']
        average_hr = [
            'interval_2',
            'interval_3',
            'interval_5',
            'interval_2',
            'interval_1']

        for i in range(len(self.transactions)):
            classes_duration.append(self.transactions[i][0])
            classes_average_hr.append(self.transactions[i][2])
        assert classes_duration == duration, "Not correct"
        assert classes_average_hr == average_hr, "Not correct"
