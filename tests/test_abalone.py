from unittest import TestCase
from tinynarm import TinyNarm
from tinynarm.item import Item
from niaarm import Dataset
from tinynarm.utils import Utils
import os

class TestAbaloneRules(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            "datasets",
            "new_dataset.csv")
        self.narm = TinyNarm(filename)
        self.narm.create_rules()

    def test_rules(self):
        postprocess = Utils(self.narm.rules)
        postprocess.sort_rules()
        assert len(self.narm.rules) > 5, "Not enough rules generated"

    def test_the_best_rule(self):
        ant1 = "Sex(M)"
        antecedent = self.narm.rules[0].antecedent
        con1 = "Length(interval_4)"
        consequent = self.narm.rules[0].consequent
        supp1 = 0.2221690208283457
        support = self.narm.rules[0].support

        assert ant1 == str(antecedent[0]), "Antecedents do not match"
        assert con1 == str(consequent[0]), "Consequents do not match"
        assert supp1 == support, "Support values do not match"
