"""
Basic run example showcasing tinynarm usage.

Before running this example, run the discretization example.
"""
import os
import time
from tinynarm import TinyNarm
from tinynarm.utils import Utils

# start timer -> for experimental purposes
start = time.time()

input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sportydatagen_discretized.csv")
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.csv")

tnarm = TinyNarm(input_path)
tnarm.create_rules()

print("Program execution --- %s seconds ---" % (time.time() - start))

postprocess = Utils(tnarm.rules)
postprocess.add_fitness()
postprocess.sort_rules()
postprocess.rules_to_csv(output_path)
postprocess.generate_statistics()
postprocess.generate_stats_report(20)
