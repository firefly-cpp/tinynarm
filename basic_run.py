from tinynarm import TinyNarm
from tinynarm.utils import Utils
import time

# start timer -> for experimental purposes
start = time.time()

a = TinyNarm("new_dataset.csv")
a.create_features()
a.cartography()
a.create_rules()
print("Program execution --- %s seconds ---" % (time.time() - start))

postprocess = Utils(a.rules)
postprocess.rules_to_csv("rules.csv")
postprocess.generate_statistics()
