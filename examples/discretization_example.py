import os
from tinynarm.discretization import Discretization

input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets", "sportydatagen.csv")
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sportydatagen_discretized.csv")

dataset = Discretization(input_path, 5)
data = dataset.generate_dataset()
dataset.dataset_to_csv(data, output_path)
