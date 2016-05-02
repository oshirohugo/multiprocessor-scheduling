#!/usr/bin/env python
# Problem defined here http://otfried.org/courses/cs500/slides-approx.pdf

from random import randint
from random import shuffle

POPULATION_SZ = 10
REPRODUCTION_RATE = 0.5
NUMBER_OF_GENERATIONS = 1000

NUMBER_OF_MACHINES = 3  # M
NUMBER_OF_JOBS = 6  # N

JOBS_TIME = [2, 3, 4, 6, 2, 2]


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


def generate_chromossome(jobs_time):
    jobs_per_machine = generate_jobs_per_machine_part()
    jobs = jobs_time
    shuffle(jobs)
    return jobs_per_machine + jobs

def fst_part_crossover(parent_1, parent_2):
    return

def snd_part_crossover(parent_1, parent_2):
    return

########################################################################################################################
# problem functions
########################################################################################################################

def fitness(individual, n_of_machines):
    jobs_per_machine = get_jobs_per_machine(individual)

    # Extract total amount of time in for jobs allocated in each machine
    j = n_of_machines
    time_per_machine = []
    machine = 0
    while machine < n_of_machines:
        total_time = 0
        job = 0
        while job < jobs_per_machine[machine]:
            total_time += individual[j + job]
            job += 1
        j = job

        time_per_machine.append(total_time)
        machine += 1

    return max(time_per_machine)


def initial_generation(pop_sz, jobs_time):
    initial_population = []
    individual = 0
    while individual < pop_sz:
        initial_population.append(generate_chromossome())
        individual += 1
    return initial_population


def reproduce(population, rate):
    individual = 0
    while individual < len(population):
        jobs_per_machine_parent_1 = get_jobs_per_machine(population[individual])
        jobs_per_machine_parent_2 = get_jobs_per_machine(population[individual + 1])
        jobs_parent_1 = get_jobs(population[individual])
        jobs_parent_2 = get_jobs(population[individual + 1])

        jobs_per_machine_child = fst_part_crossover(jobs_per_machine_parent_1, jobs_per_machine_parent_2)
        jobs_child = snd_part_crossover(jobs_per_machine_parent_1, jobs_per_machine_parent_2)
        child = jobs_per_machine_child + jobs_child
        individual += 2
    return


def mutate(population, mutation_rate):
    return
########################################################################################################################
# solve
########################################################################################################################

population = initial_generation(POPULATION_SZ, JOBS_TIME)

generation = 0
while generation < NUMBER_OF_GENERATIONS:
    population = reproduce(population, REPRODUCTION_RATE)
    population = mutate(population, MUTATION_RATE)
    generation += 1

print "Finish"
