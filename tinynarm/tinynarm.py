from itertools import permutations, combinations
from niaarm import Dataset, Feature, Rule
from tinynarm.item import Item
import csv
import sys


class TinyNarm:
    r"""Main class for microNARM approach.

   Args:
       dataset (csv file): Dataset stored in csv file.
       num_intervals (int): Number which defines how many intervals we create for numerical features.
   """

    def __init__(self, dataset, num_intervals, neighbour_threshold):
        # load dataset from csv
        self.data = Dataset(dataset)

        self.num_intervals = num_intervals
        self.neighbour_threshold = neighbour_threshold
        self.feat = []
        self.rules = []

    def create_intervals(self):
        r"""Create intervals.

        Note: The number of intervals for categorical feature is equal to number of categories.
        """
        for feature in self.data.features:
            if feature.categories is None:
                intervals = self.numerical_interval(
                    feature.min_val, feature.max_val)
                occurences = [0] * self.num_intervals
            else:
                intervals = feature.categories
                occurences = [0] * len(feature.categories)

            self.feat.append(
                Item(
                    feature.name,
                    feature.dtype,
                    intervals,
                    occurences))

    # TODO min and max should be exact
    def numerical_interval(self, min_val, max_val):
        r"""Create intervals for numerical feature."""
        val_range = (max_val - min_val) / (self.num_intervals + 1)
        intervals = []
        for i in range(self.num_intervals + 1):
            intervals.append(min_val + (i * val_range))
        return intervals

    # create item/attribute map
    def cartography(self):
        r"""Count the occurences"""
        item_map = []
        transactions = self.data.transactions.to_numpy()
        for transaction in transactions:
            for i in range(len(transaction)):
                if self.feat[i].dtype == "cat":
                    for j in range(len(self.feat[i].intervals)):
                        if transaction[i] == self.feat[i].intervals[j]:
                            self.feat[i].occurences[j] += 1
                else:
                    for j in range(len(self.feat[i].intervals) - 1):
                        if ((transaction[i] >= self.feat[i].intervals[j]) and (
                                transaction[i] < self.feat[i].intervals[j + 1])):
                            self.feat[i].occurences[j] += 1

    def ant_con(self, combination, cut):
        ant = combination[:cut]
        ant1 = []
        for i in range(len(ant)):
            ant1.append(ant[i])
        con = combination[cut:]
        con1 = []
        for i in range(len(con)):
            con1.append(con[i])

        return ant1, con1

    def if_neighbour(self, item, maxindex):
        r"""If neighbour interval has a very similar occurence rate

        Note: in this case we merge both intervals"""
        val_left = 0.0
        val_right = 0.0
        left, right = False, False
        if maxindex > 0 and maxindex < len(item.occurences) - 1:
            # in the case both neighbours are within 20%
            val_left = float(
                item.occurences[maxindex - 1] / item.occurences[maxindex])
            val_right = item.occurences[maxindex +
                                        1] / item.occurences[maxindex]

        if maxindex == 0:
            val_right = item.occurences[maxindex +
                                        1] / item.occurences[maxindex]

        if maxindex == (len(item.occurences) - 1):
            val_left = float(
                item.occurences[maxindex - 1] / item.occurences[maxindex])

        if val_left > self.neighbour_threshold:
            left = True
        if val_right > self.neighbour_threshold:
            right = True

        return left, right

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
                        categories=[item.intervals[max_index]]))
            else:
                left, right = self.if_neighbour(item, max_index)
                l = 0
                r = 0
                if left:
                    l = l - 1
                if right:
                    r = r + 1
                items.append(Feature(item.name,
                                     item.dtype,
                                     min_val=item.intervals[max_index + l],
                                     max_val=item.intervals[max_index + 1 + r]))

        # create rules for the combination of 2, 3 and 4 items

        for i in range(2, 4):
            comb = combinations(items, i)
            if i == 2:
                for j in list(comb):
                    rule = Rule([j[0]], [j[1]],
                                transactions=self.data.transactions)
                    print(
                        "Rule: ",
                        j[0],
                        "=>",
                        j[1],
                        " support: ",
                        rule.support)
                    if rule.support > 0.0:
                        self.rules.append(rule)
            else:
                for j in list(comb):
                    for cut in range(1, i - 1):
                        ant, con = self.ant_con(j, cut)
                        rule = Rule(
                            ant, con, transactions=self.data.transactions)
                        if rule.support > 0.0:
                            self.rules.append(rule)
        self.rules.sort(key=lambda x: x.support, reverse=True)

    def rules_to_csv(self, filename):
        with open(filename, 'w',) as csvfile:
            writer = csv.writer(csvfile)
            # header of our csv file
            writer.writerow(
                ['Antecedent', 'Consequent', 'Support', 'Confidence'])
            for rule in self.rules:
                writer.writerow(
                    [rule.antecedent, rule.consequent, rule.support, rule.confidence])

    def generate_report(self):
        for f in self.feat:
            print(f"Feat INFO:\n"
                  f"Name: {f.name}\n"
                  f"Bins: {f.intervals}")

    def show_item_map(self):
        for item in self.feat:
            print(f"Bin {item.name}:\n"
                  f"Bins: {item.intervals}\n"
                  f"Occurences: {item.occurences}")
