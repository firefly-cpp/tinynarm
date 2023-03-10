import csv

class Utils:

    def __init__(self, rules):
        self.rules = rules

    def calculate_fitness(self, support, confidence):
        return (support + confidence) / 2

    def rules_to_csv(self, filename):
        r"""Store rules to CSV file."""
        with open(filename, 'w',) as csvfile:
            writer = csv.writer(csvfile)
            # header of our csv file
            writer.writerow(['Antecedent', 'Consequent',
                             'Support', 'Confidence', 'Fitness'])
            for rule in self.rules:
                # calculate fitness (for comparison pursposes)
                fitness = self.calculate_fitness(rule.support, rule.confidence)

                writer.writerow(
                    [rule.antecedent, rule.consequent, rule.support, rule.confidence, fitness])

    def generate_statistics(self):
        r"""Generate statistics for experimental purposes"""
        fitness = 0.0
        support = 0.0
        confidence = 0.0
        for rule in self.rules:
            fitness += self.calculate_fitness(rule.support, rule.confidence)
            support += rule.support
            confidence += rule.confidence

        print("Total rules: ", len(self.rules))
        print("Average fitness: ", fitness / len(self.rules))
        print("Average support: ", support / len(self.rules))
        print("Average confidence: ", confidence / len(self.rules))
