from micronarm import MicroNarm
from micronarm.item import Item

a = MicroNarm("datasets/Abalone.csv", 5)
a.create_bins()
a.generate_report()
print ("Start with a cartography")
a.cartography()
a.show_item_map()
print ("Winners: ")

a.create_rules()
