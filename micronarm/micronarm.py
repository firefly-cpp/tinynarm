from itertools import permutations, combinations
from niaarm import Dataset, Feature, Rule
from micronarm.item import Item
import sys

class MicroNarm:
     r"""Main class for microNARM approach.

    Args:
        dataset (csv file): Dataset stored in csv file.
        num_bins (int): Number which defines how many bins we create for numerical features.
    """

     def __init__(self, dataset, num_bins):
        # load dataset from csv
        self.data = Dataset(dataset)
        self.num_bins = num_bins
        self.feat = []
        self.rules = []

     def create_bins(self):
        r"""Create bins.

        Note: The number of bins for categorical feature is equal to number of categories.
        """
        for feature in self.data.features:
            if feature.categories is None:
                bins = self.numerical_bin(feature.min_val, feature.max_val)
                occurences = [0] * self.num_bins
            else:
                bins = feature.categories
                occurences = [0] * len(feature.categories)

            self.feat.append(
                Item(
                    feature.name,
                    feature.dtype,
                    bins,
                    occurences))

    # TODO min and max should be exact
     def numerical_bin(self, min_val, max_val):
        r"""Create bins for numerical feature."""
        val_range = (max_val - min_val) / (self.num_bins + 1)
        bins = []
        for i in range(self.num_bins + 1):
            bins.append(min_val + (i * val_range))
        return bins

    # create item/attribute map
     def cartography(self):
        r"""Count the occurences"""
        item_map = []
        transactions = self.data.transactions.to_numpy()
        for transaction in transactions:
            for i in range(len(transaction)):
                if self.feat[i].dtype == "cat":
                    for j in range(len(self.feat[i].bins)):
                        if transaction[i] == self.feat[i].bins[j]:
                            self.feat[i].occurences[j] += 1
                else:
                    for j in range(len(self.feat[i].bins) - 1):
                        if ((transaction[i] >= self.feat[i].bins[j]) and (
                                transaction[i] < self.feat[i].bins[j + 1])):
                            self.feat[i].occurences[j] += 1

     def generate_report(self):
        for f in self.feat:
            print(f"Feat INFO:\n"
                  f"Name: {f.name}\n"
                  f"Bins: {f.bins}")

     def show_item_map(self):
        for item in self.feat:
            print(f"Bin {item.name}:\n"
                  f"Bins: {item.bins}\n"
                  f"Occurences: {item.occurences}")

     def build_rule(self, antecedent, consequent):
        r"""Create rule consisting of antecedent and consequence"""
        return Rule(
            [antecedent],
            [consequent],
            transactions=self.data.transactions)

     def evaluate_rules(self, rule):
        r"""Print the support, confidence and lift of an association rule"""
        print(rule)
        print(f'Support: {rule.support}')
        print(f'Confidence: {rule.confidence}')
        print(f'Lift: {rule.lift}')

     def ant_con(self, combination, cut):
        print ("combination: ", combination)
        ant = combination[0]
        con = combination[cut:] #FIXME
        return ant, con

     def create_rules(self):
        r"""Create new association rules."""
        items = []
        for item in self.feat:
            max_index = item.occurences.index(max(item.occurences))
            if item.dtype == "cat":
                items.append(
                    Feature(
                        item.name,
                        item.dtype,
                        categories=item.bins[max_index]))
            else:
                items.append(Feature(item.name,
                                     item.dtype,
                                     min_val=item.bins[max_index - 1],
                                     max_val=item.bins[max_index]))  # check again |

        # create rules for the combination of 2, 3 and 4 items

        for i in range(2, 5):
            comb = combinations(items, i)
            if i == 2:
                for j in list(comb):
                    self.rules.append(self.build_rule(j[0], j[1]))
            else:
                for j in list(comb):
                    for cut in range(1, i-1):
                        ant, con = self.ant_con(j, cut)
                        print ("Antecedent: ", ant, " Consequent: ", con)
                        self.rules.append(self.build_rule(ant, con))
