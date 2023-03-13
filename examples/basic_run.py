from tinynarm import TinyNarm
from tinynarm.utils import Utils
import time

# start timer -> for experimental purposes
start = time.time()

tnarm = TinyNarm("new_dataset.csv")
tnarm.create_rules()

print("Program execution --- %s seconds ---" % (time.time() - start))

postprocess = Utils(tnarm.rules)
postprocess.rules_to_csv("rules.csv")
postprocess.generate_statistics()
postprocess.generate_stats_report(20)
