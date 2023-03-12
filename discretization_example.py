from tinynarm.discretization import Discretization

dataset = Discretization("datasets/sportydatagen.csv", 5)
data = dataset.generate_dataset()
dataset.dataset_to_csv(data, "new_dataset.csv")
