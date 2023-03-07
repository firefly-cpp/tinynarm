from itertools import permutations, combinations
from niaarm import Dataset, Feature, Rule
from tinynarm.item import Item
import csv
import sys


class TinyNarm:
    r"""Main class for microNARM approach.

   Args:
       dataset (csv file): Dataset stored in csv file.
       num_bins (int): Number which defines how many bins we create for numerical features.
   """

    def __init__(self, dataset, num_bins, neighbour_threshold):
        # load dataset from csv
        self.data = Dataset(dataset)
        self.num_bins = num_bins
        self.neighbour_threshold = neighbour_threshold
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
        r"""If neighbour bin has a very similar occurence rate

        Note: in this case we merge both bins"""
        val_left = 0.0
        val_right = 0.0
        left, right = False, False
        if maxindex > 0 and maxindex < len(item.occurences)-1:
            # in the case both neighbours are within 20%
            val_left = float(item.occurences[maxindex-1] / item.occurences[maxindex])
            val_right = item.occurences[maxindex+1] / item.occurences[maxindex]

        if maxindex == 0:
            val_right = item.occurences[maxindex+1] / item.occurences[maxindex]

        if maxindex == (len(item.occurences)-1):
            val_left = float(item.occurences[maxindex-1] / item.occurences[maxindex])

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
                        categories=[item.bins[max_index]]))
                #print ("delam, ", item.bins[max_index])
            else:
                #left, right = self.if_neighbour(item, max_index)
                #l = 0
                #r = 0
                #if left:
                #    l = l - 1
                #if right:
                #    r = r + 1
                items.append(Feature(item.name,
                                     item.dtype,
                                     min_val=item.bins[max_index], # + l
                                     max_val=item.bins[max_index + 1])) # + r  # check again |

        # create rules for the combination of 2, 3 and 4 items

        for i in range(2, 4):
            comb = combinations(items, i)
            if i == 2:
                for j in list(comb):
                    rule = Rule([j[0]], [j[1]],
                                transactions=self.data.transactions)
                    print ("Rule: ", j[0], "=>", j[1], " support: ", rule.support)
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
