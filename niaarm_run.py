from niaarm import NiaARM
from niaarm.dataset import Dataset
from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import Task, OptimizationType


if __name__ == '__main__':
    # load and preprocess the dataset from csv
    data = Dataset("new_dataset.csv")

    # Create a problem:::
    # dimension represents the dimension of the problem;
    # features represent the list of features, while transactions depicts the list of transactions
    # the following 4 elements represent weights (support, confidence, coverage, shrinkage)
    # A weight of 0.0 means that criteria are omitted and are, therefore, excluded from the fitness function
    problem = NiaARM(data.dimension, data.features, data.transactions, metrics=('support', 'confidence'), logging=True)

    # build niapy task
    task = Task(problem=problem, max_iters=100, optimization_type=OptimizationType.MAXIMIZATION)

    # use Differential Evolution (DE) algorithm from the NiaPy library
    # see full list of available algorithms: https://github.com/NiaOrg/NiaPy/blob/master/Algorithms.md
    algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)

    # run algorithm
    best = algo.run(task=task)

    # sort rules
    problem.rules.sort()

    # export all rules to csv
    problem.rules.to_csv('output.csv')
