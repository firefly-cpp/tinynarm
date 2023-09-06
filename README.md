# tinyNARM

---

[![PyPI Version](https://img.shields.io/pypi/v/tinynarm.svg)](https://pypi.python.org/pypi/tinynarm)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinynarm.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tinynarm.svg)
[![Downloads](https://pepy.tech/badge/tinynarm)](https://pepy.tech/project/tinynarm)

## About

tinyNARM is an experimental effort in approaching/tailoring the classical Numerical Association Rule Mining (NARM) to limited hardware devices, e.g., ESP32 microcontrollers so that devices do not need to depend on remote servers for making decisions. Motivation mainly lies in smart agriculture, where Internet connectivity is unavailable in rural areas.

The current repository hosts a tinyNARM algorithm prototype initially developed in Python for fast prototyping.

## Detailed insights
The current version includes (but is not limited to) the following functions:

- loading datasets in CSV format,
- discretizing numerical features to discrete classes,
- association rule mining using the tinynarm approach,
- easy comparison with the NiaARM approach.

## Installation

### pip

Install tinyNARM with pip:

```sh
pip install tinynarm
```

## Usage

### Basic run

```python
from tinynarm import TinyNarm
from tinynarm.utils import Utils

tnarm = TinyNarm("new_dataset.csv")
tnarm.create_rules()

postprocess = Utils(tnarm.rules)
postprocess.add_fitness()
postprocess.sort_rules()
postprocess.rules_to_csv("rules.csv")
postprocess.generate_statistics()
postprocess.generate_stats_report(20)
```

### Discretization

```python
from tinynarm.discretization import Discretization

dataset = Discretization("datasets/sportydatagen.csv", 5)
data = dataset.generate_dataset()
dataset.dataset_to_csv(data, "new_dataset.csv")
```

## NARM references

[1] I. Fister Jr., A. Iglesias, A. Gálvez, J. Del Ser, E. Osaba, I Fister. [Differential evolution for association rule mining using categorical and numerical attributes](http://www.iztok-jr-fister.eu/static/publications/231.pdf) In: Intelligent data engineering and automated learning - IDEAL 2018, pp. 79-88, 2018.

[2] I. Fister Jr., V. Podgorelec, I. Fister. [Improved Nature-Inspired Algorithms for Numeric Association Rule Mining](https://link.springer.com/chapter/10.1007/978-3-030-68154-8_19). In: Vasant P., Zelinka I., Weber GW. (eds) Intelligent Computing and Optimization. ICO 2020. Advances in Intelligent Systems and Computing, vol 1324. Springer, Cham.

[3] I. Fister Jr., I. Fister [A brief overview of swarm intelligence-based algorithms for numerical association rule mining](https://arxiv.org/abs/2010.15524). arXiv preprint arXiv:2010.15524 (2020).

[4] Stupan, Ž., Fister, I. Jr. (2022). [NiaARM: A minimalistic framework for Numerical Association Rule Mining](https://joss.theoj.org/papers/10.21105/joss.04448.pdf). Journal of Open Source Software, 7(77), 4448.

## Cite us

Fister Jr, I., Fister, I., Galvez, A., & Iglesias, A. (2023, August). [TinyNARM: Simplifying Numerical Association Rule Mining for Running on Microcontrollers](https://link.springer.com/chapter/10.1007/978-3-031-42529-5_12). In International Conference on Soft Computing Models in Industrial and Environmental Applications (pp. 122-131). Cham: Springer Nature Switzerland.

## License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
