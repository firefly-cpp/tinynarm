from tinynarm import TinyNarm

# TinyNarm class expects two parameters
# First parameter (5) defines how many intervals we create for numerical features.
# Second parameter (0.70) defines the threshold for including a neighbour in our rule.
a = TinyNarm("datasets/Abalone.csv", 5, 0.70)
a.create_intervals()
a.generate_report()
print ("Start with a cartography")
a.cartography()
a.show_item_map()
a.create_rules()
a.rules_to_csv("rules.csv")
