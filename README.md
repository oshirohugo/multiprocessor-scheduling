# Multiprocessor Scheduling using Genetic Algorithms
This project implements a Multiprocessor Scheduling solver using Genetic 
Algorithms.

## Generating Random Intance
To generate a random instance of size `N`:

```bash
$./generate-instaces.py $N
```

This will generate output on file `loading-balance-N.txt`

## Setting script
To set parameters for the problem, edit source code for `multiprocessor-scheduling.py`.
For example:

```python
JOBS_FILE = "loading-balance-1000.txt"
OUTPUT_FILE = open("complete-output-7.txt", "w")

JOBS = read_jobs_from_file(JOBS_FILE)

POPULATION_SZ = 500
REPRODUCTION_RATE = 0.9
MUTATION_RATE = 0.9
NUMBER_OF_GENERATIONS = 500
NUMBER_OF_MACHINES = 15  # M

CROSSOVER_METHOD = crossover_s
MUTATION_METHOD = swap
FITNESS_FUNCTION = fitness_function
SELECTION_METHOD = championship
ELITISM = False
```
`JOBS` can also be set directly into code like this:

```python
JOBS = [(1, 2.0), (2, 3.0), (3, 4.0), (4, 6.0), (5, 2.0), (6, 2.0)]
```

In this case you don't need the line:
```python
JOBS = read_jobs_from_file(JOBS_FILE)
```

## Running
After config just run:
```bash
$./mutiprocessor-scheduling.py
```

