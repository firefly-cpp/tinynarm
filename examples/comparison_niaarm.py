from tinynarm.comparison import Compare
from tinynarm.utils import Utils

nia = Compare("new_dataset.csv", "niaarm_new_dataset.csv")
nia.compare_niaarm(50, 1000)

# postprocess
postprocess = Utils(nia.get_rules())
postprocess.generate_statistics()
postprocess.generate_stats_report(20)
