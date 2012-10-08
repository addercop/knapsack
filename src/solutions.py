#!/usr/bin/python
'''Algorithms for solving the BinaryKnapsackProblem.'''
import random

import knapsack


class BinaryKnapsackSolver():
    '''Strategy pattern interface for solving a BinaryKnapsackProblem.
    Subclasses should implement a method called solve that takes no
    parameters and returns a list of BinaryKnapsackSolutions.'''
    def __init__(self, problem):
        self.problem = problem

    def name(self):
        '''Return this object's class's name by reflection.'''
        return self.__class__.__name__


class BruteForceBinaryKnapsackSolver(BinaryKnapsackSolver):
    '''Solve the problem by Big-theta(2**n) exhaustive search.'''
    def solve(self):
        '''Strategy method to solve the problem with exhaustive search.'''
        return self.get_best_solutions()

    def get_best_solutions(self):
        '''Big-theta(2**n) exhaustive search.'''
        width = self.problem.size()
        best_solutions = []
        best_fitness = -1

        for i in xrange(0, 2 ** width):
            right = bin(i)[2:]
            solution_string = '0' * (width - len(right)) + right
            solution = knapsack.BinaryKnapsackSolution(solution_string)
            fitness = self.problem.fitness(solution)
            if fitness > best_fitness:
                best_solutions = [solution]
                best_fitness = fitness
            elif fitness == best_fitness:
                best_solutions.append(solution)

        return best_solutions


class BranchAndBoundBinaryKnapsackSolver(BinaryKnapsackSolver):
    '''Solve the problem by brute force search with pruning.'''
    def solve(self):
        '''Strategy method to solve the problem by brute force with pruning.'''
        return self.search()

    def search(self):
        '''Branch-and-bound pruning version of brute-force 2**n search.'''
        best_solutions = []
        self._search(best_solutions, -1, 0, 0, 0, "")
        return best_solutions

    def _search(self, \
        best_solutions, best_score, weight, value, index, partial_solution):
        '''Private recursive search.'''
        if weight > self.problem.knapsack_capacity:
            return 0
        if index == self.problem.size() \
            or weight == self.problem.knapsack_capacity:
            partial_solution += "0" * \
                (self.problem.size() - len(partial_solution))
            if weight > self.problem.knapsack_capacity:
                fitness = 0
            else:
                fitness = value
            if fitness > best_score:
                while len(best_solutions) > 0:
                    best_solutions.pop()
                bks = knapsack.BinaryKnapsackSolution(partial_solution)
                best_solutions.append(bks)
            elif fitness == best_score:
                bks = knapsack.BinaryKnapsackSolution(partial_solution)
                best_solutions.append(bks)
            return fitness

        steal_weight = weight + self.problem.inventory.weight(index)
        steal_value = value + self.problem.inventory.value(index)
        steal_score = self._search(best_score, \
            best_solutions, steal_weight, steal_value, index + 1, \
            partial_solution + "1")
        best_score = max(best_score, steal_score)

        leave_score = self._search(best_score, \
            best_solutions, weight, value, index + 1, partial_solution + "0")
        best_score = max(best_score, leave_score)

        return best_score


class BinaryKnapsackProblemPopulation():
    '''A collection of BinaryKnapsackSolution objects
    that act as a population for a genetic algorithm.'''
    def __init__(self, problem):
        self.problem = problem
        self.population = knapsack.get_random_population(problem)
        self.size = len(self.population)

    def cull(self, percentile=50):
        '''Discard members with fitness less than percentile.'''
        scores = [self.problem.fitness(member) for member in self.population]
        sorted_scores = list(scores)
        sorted_scores.sort()
        cutoff = sorted_scores[(len(self.population) / 100) * percentile]
        culled_population = \
            [member for member in self.population \
             if self.problem.fitness(member) > cutoff]

        if len(culled_population) == 0:
            max_score = max(scores)
            culled_population = \
                [member for member in self.population \
                 if self.problem.fitness(member) == max_score]

        self.population = culled_population

    def reproduce(self):
        '''Create children from the population
        until the population reaches target size.'''
        children = []
        for _index in range(self.size - len(self.population)):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            children.append(parent1.reproduce(parent2))
        self.population.extend(children)

    def mutate(self):
        '''Mutate each member of the population.'''
        self.population = [member.mutate() for member in self.population]

    def max_score(self):
        '''Return the maximum fitness from the members of the population.'''
        scores = [self.problem.fitness(member) for member in self.population]
        return max(scores)

    def max_scorers(self):
        '''Return a list of the most fit members of the population.'''
        score = self.max_score()
        return [member for member in self.population \
                if self.problem.fitness(member) == score]


class GeneticAlgorithmBinaryKnapsackSolver(BinaryKnapsackSolver):
    '''Solves the problem by a genetic algorithm.'''
    def solve(self):
        '''Strategy method to solve the problem with a genetic algorithm.'''
        return self.genetic_algorithm(100)

    def genetic_algorithm(self, generations=10000):
        '''A template method for running a genetic algorithm.'''
        population = BinaryKnapsackProblemPopulation(self.problem)
        for _index in range(generations):
            population.cull()
            population.reproduce()
            population.mutate()

        return population.max_scorers()


#class DynamicProgrammingBinaryKnapsackSolver(BinaryKnapsackSolver):
#    '''Finds the maximum profit to be extracted from the problem.'''
#    pass


def solve_and_print(solver):
    '''Execute the solver and print out the results.'''
    print solver.name()
    solutions = solver.solve()
    print "%d solution(s)" % len(solutions)
    for solution in solutions:
        print solution
    print


def get_solvers(problem):
    '''Factory function to create solvers for this problem.'''
    solvers = []

    #balk if the size is too big.
    if problem.size() < 25:
        solvers.append(BruteForceBinaryKnapsackSolver(problem))
        solvers.append(BranchAndBoundBinaryKnapsackSolver(problem))

    solvers.append(GeneticAlgorithmBinaryKnapsackSolver(problem))

    return solvers


def solve(problem):
    '''Solves the problem with several algorithms.'''
    solvers = get_solvers(problem)
    print problem
    for solver in solvers:
        solve_and_print(solver)


if __name__ == "__main__":
    KNAPSACK_PROBLEM = \
        knapsack.get_problem_from_file("../data/10_instance.txt")
    solve(KNAPSACK_PROBLEM)
