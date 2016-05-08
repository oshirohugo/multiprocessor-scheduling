#!/usr/bin/env python
# Problem defined here http://otfried.org/courses/cs500/slides-approx.pdf

from random import randint
from random import shuffle

from jsonschema.tests.test_jsonschema_test_suite import missing_format

POPULATION_SZ = 10
REPRODUCTION_RATE = 0.5
MUTATION_RATE = 0.1
NUMBER_OF_GENERATIONS = 1000

NUMBER_OF_MACHINES = 3  # M
NUMBER_OF_JOBS = 6  # N

# JOBS = [2, 3, 4, 6, 2, 2]
JOBS = [(1, 4), (2, 3), (3, 2), (4, 5), (5, 1), (5, 2)]


# cromossome [ nofjobs_in_1, nofjobs_in_2, ... nofjobs_in_m, job1, job2, ..., jobn ]

########################################################################################################################
# auxiliary function
########################################################################################################################

def get_jobs_per_machine(individual, n_of_machines):
    return individual[:n_of_machines]


def get_jobs(individual, n_of_machines):
    return individual[n_of_machines:]


def generate_jobs_per_machine_part(n_of_jobs, n_of_machines):
    jobs_per_machine = []

    # random generate jobs for m - 1 machines
    machine = 0
    limit = n_of_jobs
    number_of_allocated_jobs = 0
    while machine < n_of_machines - 1:
        n_of_jobs_generated = randint(0, limit)
        jobs_per_machine.append(n_of_jobs_generated)
        number_of_allocated_jobs += n_of_jobs_generated
        limit -= n_of_jobs_generated
        machine += 1

    # atribute remaining jobs to last machine
    jobs_per_machine.append(n_of_jobs - number_of_allocated_jobs)

    shuffle(jobs_per_machine)
    return jobs_per_machine


def generate_chromossome(jobs, n_of_machines):
    jobs_per_machine = generate_jobs_per_machine_part(len(jobs), n_of_machines)
    _jobs = jobs
    shuffle(_jobs)
    return jobs_per_machine + _jobs


def crossover_d(a, b):
    cut_point = len(a) / 2
    aa = a[:cut_point] + b[cut_point:]
    bb = b[:cut_point] + a[cut_point:]
    return [aa, bb]


def crossover_s(a, b):
    i_a = randint(0, len(a))
    i_b = randint(0, len(a))
    aux = a[i_a]
    a[i_a] = b[i_b]
    b[i_b] = aux
    return [a, b]


def fst_part_crossover(parent_1, parent_2, crossover):
    return crossover(parent_1, parent_2)


def adjust_snd_part(child, parent):
    missing_elements = list(set(parent) - set(child))
    if len(missing_elements) == 0:
        return child

    seen = set()
    repeated_index = []
    for i in range(len(child)):
        if child[i] in seen:
            repeated_index.append(i)
        seen.add(child[i])

    for j in range(len(repeated_index)):
        child[repeated_index[j]] = missing_elements[j]

    return child


def snd_part_crossover(parent_1, parent_2, crossover):
    children = crossover(parent_1, parent_2)
    return [adjust_snd_part(child, parent_1) for child in children]


########################################################################################################################
# problem functions
########################################################################################################################

def fitness(individual, n_of_machines):
    jobs_per_machine = get_jobs_per_machine(individual, n_of_machines)
    jobs = get_jobs(individual, n_of_machines)

    # Extract total amount of time in for jobs allocated in each machine
    time_per_machine = []
    j = 0
    machine = 0
    while machine < n_of_machines:
        total_time = 0
        job = 0
        while job < jobs_per_machine[machine]:
            total_time += jobs[j + job][1]
            job += 1
        j = job

        time_per_machine.append(total_time)
        machine += 1

    return max(time_per_machine)


def initial_generation(pop_sz, jobs, n_of_machines):
    initial_population = []
    individual = 0
    while individual < pop_sz:
        initial_population.append(generate_chromossome(jobs, n_of_machines))
        individual += 1
    return initial_population


def roulette(population, next_gen_size, fitness_function):
    return


def select_individuals(population, next_gen_size, fitness_function):
    return sorted(population, key=fitness_function)[:next_gen_size]


def reproduce(population, rate, fitness_function, crossover_method, n_of_machines):
    individual = 0
    next_gen_size = round(len(population) * rate)
    selected = select_individuals(population, next_gen_size, fitness_function)
    next_gen = []

    while individual < len(selected):
        jobs_per_machine_parent_1 = get_jobs_per_machine(selected[individual], n_of_machines)
        jobs_per_machine_parent_2 = get_jobs_per_machine(selected[individual + 1], n_of_machines)
        jobs_per_machine_children = fst_part_crossover(jobs_per_machine_parent_1, jobs_per_machine_parent_2,
                                                       crossover_method)

        jobs_parent_1 = get_jobs(selected[individual], n_of_machines)
        jobs_parent_2 = get_jobs(selected[individual + 1], n_of_machines)
        jobs_children = snd_part_crossover(jobs_parent_1, jobs_parent_2, crossover_method)

        child_1 = jobs_per_machine_children[0] + jobs_children[0]
        child_2 = jobs_per_machine_children[1] + jobs_children[1]

        next_gen.append(child_1)
        next_gen.append(child_2)

        individual += 2

    return next_gen


def swap(chromosome):
    chromosome_sz = len(chromosome)
    i = randint(0, chromosome_sz)
    j = randint(0, chromosome_sz)

    if i == j:
        j = randint(0, chromosome_sz)

    aux = chromosome[i]
    chromosome[i] = chromosome[j]
    chromosome[j] = aux

    return chromosome


def seq_swap(chromosome):
    return crossover_d(chromosome, chromosome)[0]


def mutate(pop, mutation_rate, mutation_method, n_of_machines):
    individual = 0
    mutants_sz = round(mutation_rate * len(pop))
    selected = select_individuals(pop, mutants_sz, fitness_function)
    mutant_gen = []

    while individual < len(selected):
        jobs_per_machine = get_jobs_per_machine(selected[individual], n_of_machines)
        jobs_per_machine_mutant = mutation_method(jobs_per_machine)

        jobs = get_jobs(selected[individual], n_of_machines)
        jobs_mutant = mutation_method(jobs)

        mutant = jobs_per_machine_mutant + jobs_mutant
        mutant_gen.append(mutant)
        individual += 1

    return mutant_gen


########################################################################################################################
# solve
########################################################################################################################

def fitness_function(individual):
    return fitness(individual, NUMBER_OF_MACHINES)


CROSSOVER_METHOD = crossover_d
MUTATION_METHOD = swap
FITNESS_FUNCTION = fitness_function

population = initial_generation(POPULATION_SZ, JOBS, NUMBER_OF_MACHINES)

generation = 0
while generation < NUMBER_OF_GENERATIONS:
    population = reproduce(population, REPRODUCTION_RATE, FITNESS_FUNCTION, CROSSOVER_METHOD, NUMBER_OF_MACHINES)
    population = mutate(population, MUTATION_RATE, MUTATION_METHOD, NUMBER_OF_MACHINES)
    generation += 1

print "Finish"
