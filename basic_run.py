from tinynarm import TinyNarm
import time

# start timer -> for experimental purposes
start = time.time()

# TinyNarm class expects two parameters
# First parameter (5) defines how many intervals we create for numerical features.
# Second parameter (0.70) defines the threshold for including a neighbour
# in our rule.
a = TinyNarm("datasets/Abalone.csv", 5, 0.70)
a.create_intervals()
# a.generate_report()
#print ("Start with a cartography")
a.cartography()
# a.show_item_map()
a.create_rules()
print("Program execution --- %s seconds ---" % (time.time() - start))
a.rules_to_csv("rules.csv")
a.generate_statistics()
