#!/usr/bin/env python
import random
import argparse
import os
import sys
import threading
import itertools
import time

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-q", "--queen", help = "queen count",  type=int, default = 8)
parser.add_argument("-p", "--population",help = "population count per generation", type=int, default = 100)
 
# Read arguments from command line
args = parser.parse_args()
population_per_gen = args.population
queen_count = args.queen

queen = "Q  "
empty = "#  "

def random_chromosome(size): #making random chromosomes
    return [ random.randint(1, size) for _ in range(size) ]

def show_board(chromosome):
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if j == chromosome[i]-1:
                print(f"{queen}",end="")
            else:
                print(f"{empty}",end="")
        print("")    

def fitness(chromosome):
    chromosome = list(chromosome)
    horizontal_collisions = sum((chromosome.count(queen)-1 for queen in chromosome))/2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(maxFitness - (horizontal_collisions + diagonal_collisions)) #28-(2+3)=23


def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness

def mutate(x):  #randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    
    total = sum(w for c, w in populationWithProbabilty)
    
    r = random.uniform(0, total)
    upto = 0
    
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def reproduce(x, y): #doing cross_over between two chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def genetic_queen(population, fitness):
    mutation_probability = 0.03
    new_population = []
    probabilities = (probability(n, fitness) for n in population)
    probabilities = list(probabilities)

    for i in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        
        if random.random() < mutation_probability:
            child = mutate(child)
            # print_chromosome(child)
        
        new_population.append(child)
        
        if fitness(child) == maxFitness: break
    return new_population

#here is the animation
def animate():
    for c in itertools.cycle(["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]):
        if done:
            break
        sys.stdout.write(f'\rrunning {c} | gen:{generation}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!')

if __name__ == "__main__":
    population = tuple(random_chromosome(queen_count) for _ in range(population_per_gen))
    maxFitness = (queen_count*(queen_count-1))/2  # 8*7/2 = 28
    generation = 1

    done = False
    t = threading.Thread(target=animate)
    t.start()

    # print the intial population
    # for chromosome in population:
    #     print(f"{chromosome}: {fitness(chromosome)}")
     
    while not maxFitness in (fitness(chrom) for chrom in population):
        # os.system("clear")        
        # os.system('shutdown /s /t 1')

        # print(f"=== Generation {generation} ===")
        population = genetic_queen(population, fitness)

        # print("")
        # print(f"Maximum Fitness = {max((fitness(chromosome) for chromosome in population))}")

        generation += 1
    done = True
    chrom_out = []
    print("\nSolved in Generation {}!".format(generation-1))
    for chrom in population:
        if fitness(chrom) == maxFitness:
            print("");
            print("solutions Found: ")
            chrom_out = chrom
            print(f"chromosome = {chrom} \n")
            
            show_board(chrom)
    # print(fitness(chromosome))

