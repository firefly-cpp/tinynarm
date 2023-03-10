from tinynarm.discretization import Discretization

dataset = Discretization("datasets/Abalone.csv", 5)

dataset.create_intervals()

data = dataset.generate_dataset()

dataset.dataset_to_csv(data, "new_dataset.csv")
