#!/usr/bin/env python
# Problem defined here http://otfried.org/courses/cs500/slides-approx.pdf

from random import randint
from random import uniform
from random import shuffle

POPULATION_SZ = 100
REPRODUCTION_RATE = 0.8
MUTATION_RATE = 0.2
NUMBER_OF_GENERATIONS = 1000

NUMBER_OF_MACHINES = 3  # M

''# JOBS = [(1, 4.0), (2, 3.0), (3, 2.0), (4, 5.0), (5, 1.0), (6, 2.0)]
JOBS = [(1, 2.0), (2, 3.0), (3, 4.0), (4, 6.0), (5, 2.0), (6, 2.0)]

# cromossome [ nofjobs_in_1, nofjobs_in_2, ... nofjobs_in_m, job1, job2, ..., jobn ]

########################################################################################################################
# auxiliary function
########################################################################################################################
def print_generation(gen):
    for individual in gen:
        print individual


def print_solution(population, fit_function, n_of_machines):
    best = championship(population, 1, fit_function)[0]
    jobs_per_machine = get_jobs_per_machine(best, n_of_machines)
    jobs = get_jobs(best, n_of_machines)

    machine = 0
    j = 0
    while machine < len(jobs_per_machine):
        print "machine %d: " % (machine + 1),
        n_of_jobs_in_machine = jobs_per_machine[machine]
        machine_job = 0
        total = 0
        while machine_job < n_of_jobs_in_machine:
            total += jobs[j + machine_job][1]
            print str(jobs[j + machine_job]) + " ",
            machine_job += 1
        j += machine_job
        machine += 1
        print " : %f\n" % total,


def print_best_fitness(population, fit_function):
    best = championship(population, 1, fit_function)[0]
    print best,
    print " : " + str(fit_function(best))


def check_repetitions(population, fit_function, n_of_machines, last, repetition):
    best = championship(population, 1, fit_function)[0]

    if not last:
        return best, 0

    if best == last:
        return best, repetition + 1
    return best, 0


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
    aa = list(a)
    bb = list(b)
    i_a = randint(0, len(a) - 1)
    i_b = randint(0, len(b) - 1)
    aux = aa[i_a]
    aa[i_a] = bb[i_b]
    bb[i_b] = aux
    return [aa, bb]


def adjust_fst_part(child, parent):
    correct = sum(parent)
    test = sum(child)

    if correct == test:
        return child

    if test < correct:
        diff = correct - test
        i = 0
        while diff != 0:
            if child[i] < correct:
                child[i] += 1
                diff -= 1
            i += 1
            if i == len(child):
                i = 0
        return child

    # test > correct
    diff = test - correct
    i = 0
    while diff != 0:
        if child[i] > 0:
            child[i] -= 1
            diff -= 1
        i += 1
        if i == len(child):
            i = 0
    return child


def fst_part_crossover(parent_1, parent_2, crossover):
    _children = crossover(parent_1, parent_2)
    return [adjust_fst_part(child, parent_1) for child in _children]


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
    base = 0
    machine = 0
    unused = 0
    while machine < n_of_machines:
        total_time = 0
        job = 0
        while job < jobs_per_machine[machine]:
            total_time += jobs[base + job][1]
            job += 1
        base += job

        time_per_machine.append(total_time)

        if jobs_per_machine[machine] == 0:
            unused += 1

        machine += 1



    unused = float(unused)
    return max(time_per_machine) + unused


def initial_generation(pop_sz, jobs, n_of_machines):
    initial_population = []
    individual = 0
    while individual < pop_sz:
        initial_population.append(generate_chromossome(jobs, n_of_machines))
        individual += 1
    return initial_population


def accumu(lis):
    total = 0
    for x in lis:
        total += x
        yield total


def select_by_fitness(r, fit_sum):
    for i in range(len(fit_sum)):
        if fit_sum >= r:
            return i
    # Should never get here
    return -1


def roulette(population, next_gen_size, fit_function):
    all_elements_fit = [fit_function(chromosome) for chromosome in population]
    a_t = sum(all_elements_fit)
    fit_sum = list(accumu(all_elements_fit))

    next_pop = []
    elements = 0
    while elements < next_gen_size:
        r = uniform(0, a_t)
        selected_index = select_by_fitness(r, fit_sum)
        next_pop.append(population[selected_index])
        elements += 1

    return next_pop


def championship(population, next_gen_size, fit_function):
    return sorted(population, key=fit_function)[:next_gen_size]


def reproduce(population, rate, fit_function, crossover_method, n_of_machines, selection_method):
    individual = 0
    next_gen_size = int(round(len(population) * rate))
    selected = selection_method(population, next_gen_size, fit_function)
    next_gen = []

    while individual < len(selected) - 1:
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
    i = randint(0, chromosome_sz - 1)
    j = randint(0, chromosome_sz - 1)

    if i == j:
        j = randint(0, chromosome_sz - 1)

    aux = chromosome[i]
    chromosome[i] = chromosome[j]
    chromosome[j] = aux

    return chromosome


def seq_swap(chromosome):
    return crossover_d(chromosome, chromosome)[0]


def mutate(pop, mutation_rate, mutation_method, n_of_machines):
    individual = 0
    mutants_sz = int(round(mutation_rate * len(pop)))
    shuffled_pop = list(pop)
    shuffle(shuffled_pop)
    selected = shuffled_pop[:mutants_sz]
    while individual < len(selected):
        replace_index = pop.index(selected[individual])

        jobs_per_machine = get_jobs_per_machine(selected[individual], n_of_machines)
        jobs_per_machine_mutant = mutation_method(jobs_per_machine)

        jobs = get_jobs(selected[individual], n_of_machines)
        jobs_mutant = mutation_method(jobs)

        mutant = jobs_per_machine_mutant + jobs_mutant
        pop[replace_index] = mutant
        individual += 1

    return pop


########################################################################################################################
# solve
########################################################################################################################

def fitness_function(individual):
    return fitness(individual, NUMBER_OF_MACHINES)


CROSSOVER_METHOD = crossover_d
MUTATION_METHOD = seq_swap
FITNESS_FUNCTION = fitness_function
SELECTION_METHOD = championship
ELITISM = True

repetition_counter = 0
old_generation = initial_generation(POPULATION_SZ, JOBS, NUMBER_OF_MACHINES)
generation = 0
last_best = []

if not ELITISM:
    while generation < NUMBER_OF_GENERATIONS:
        children = reproduce(old_generation, REPRODUCTION_RATE, FITNESS_FUNCTION, CROSSOVER_METHOD, NUMBER_OF_MACHINES,
                             SELECTION_METHOD)
        children_after_mutations = mutate(children, MUTATION_RATE, MUTATION_METHOD, NUMBER_OF_MACHINES)
        # children_after_mutations = children

        # M - N
        old_new_diff = len(old_generation) - len(children_after_mutations)
        best_from_old = championship(old_generation, old_new_diff, FITNESS_FUNCTION)

        new_generation = children_after_mutations + best_from_old
        old_generation = new_generation

        # print_generation(new_generation)

        print "Generation %d" % generation,
        print_best_fitness(new_generation, FITNESS_FUNCTION)
        last_best, repetition_counter = check_repetitions(new_generation, FITNESS_FUNCTION, NUMBER_OF_MACHINES, last_best,
                                                          repetition_counter)

        if repetition_counter == 3:
            break

        generation += 1


if ELITISM:
    while generation < NUMBER_OF_GENERATIONS:
        best_from_old = championship(old_generation, 1, FITNESS_FUNCTION)
        children = reproduce(old_generation, REPRODUCTION_RATE, FITNESS_FUNCTION, CROSSOVER_METHOD, NUMBER_OF_MACHINES,
                             SELECTION_METHOD)
        children_after_mutations = mutate(children, MUTATION_RATE, MUTATION_METHOD, NUMBER_OF_MACHINES)

        new_generation = children_after_mutations + best_from_old
        old_generation = new_generation

        # print_generation(new_generation)

        print "Generation %d" % generation,
        print_best_fitness(new_generation, FITNESS_FUNCTION)
        last_best, repetition_counter = check_repetitions(new_generation, FITNESS_FUNCTION, NUMBER_OF_MACHINES, last_best,
                                                          repetition_counter)

        if repetition_counter == 3:
            break

        generation += 1


print "Finish!"

print_solution(new_generation, FITNESS_FUNCTION, NUMBER_OF_MACHINES)
