from tinynarm import TinyNarm
from tinynarm.item import Item

a = TinyNarm("datasets/nursery.csv", 5, 0.70)
a.create_bins()
a.generate_report()
print ("Start with a cartography")
a.cartography()
a.show_item_map()
a.create_rules()
a.rules_to_csv("rules.csv")
