#!/usr/bin/python
'''Classes to represent binary knapsack problem items, inventories, and problem
instances.'''
#knapsack.py
import random


def get_problem_from_file(path):
    '''Parse a BinaryKnapsackProblem instance from a file.'''
    contents = open(path, "r").read()
    contents = contents.split("\n")
    capacity = int(contents[0])
    items = []
    for line in contents[1:]:
        if len(line) <= 1:
            break
        weight, value = line.split()
        weight, value = int(weight), int(value)
        items.append(Item(weight, value))

    inventory = Inventory(items)

    return BinaryKnapsackProblem(capacity, inventory)


def get_random_problem(size=100):
    '''
    Create a random problem instance of 'size' number of weight/value pairs.
    '''
    items = []
    weight_min = 10
    weight_max = 100
    value_min = 20
    value_max = 200

    capacity = (((weight_min + weight_max) / 2) * size) / 10

    for _index in range(size):
        weight = random.randint(weight_min, weight_max)
        value = random.randint(value_min, value_max)
        item = Item(weight, value)
        items.append(item)

    inventory = Inventory(items)

    return BinaryKnapsackProblem(capacity, inventory)


def get_random_population(problem, size=100):
    '''Create a list of random solutions for this problem problem.'''
    return [get_random_solution(problem) for _i in range(size)]


def get_random_solution(instance):
    '''Return a random solution with weight less than knapsack capacity.'''
    #add random items until adding the next item would exceed capacity.
    vector = ['0'] * instance.size()
    indexes = range(0, instance.size() - 1)
    random.shuffle(indexes)
    total_weight = 0
    for i in indexes:
        item = instance.inventory.item_at(i)
        if total_weight + item.weight > instance.knapsack_capacity:
            break
        total_weight += item.weight
        vector[i] = '1'

    return BinaryKnapsackSolution("".join(vector))


class Inventory():
    '''A collection of Items.'''
    def __init__(self, items):
        self.items = items
        self.items.sort()

    def item_at(self, i):
        '''Return the item at zero-based index i.'''
        return self.items[i]

    def weight(self, i):
        '''Return weight of item at zero-based index i.'''
        return self.items[i].weight

    def value(self, i):
        '''Return value of item at zero-based index i.'''
        return self.items[i].value

    def size(self):
        '''Return the number of Items in this Inventory.'''
        return len(self.items)

    def __str__(self):
        ret = ""
        ret += "Inventory size: %d\n" % len(self.items)
        ret += "Weight/value\n"
        ret += "\n".join("%d %d" % (item.weight, item.value) \
            for item in self.items)

        return ret


class Item():
    '''An item in a 0-1 knapsack problem with a weight and a value.
    Treat as immutable.'''
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __cmp__(self, other):
        '''Sort by increasing weight.
        If weights are equal, use *decreasing* value as a tie breaker.'''
        if self.weight < other.weight:
            return -1
        elif self.weight == other.weight:
            if self.value < other.value:
                return 1  # !
            elif self.value == other.value:
                return 0
            elif self.value > other.value:
                return -1  # !
        elif self.weight > other.weight:
            return 1


class BinaryKnapsackProblem():
    '''    A representation of the 0-1 knapsack problem.'''
    def __init__(self, knapsack_capacity, inventory):
        '''knapsack_capacity, an integer,
        and inventory, an Inventory object.'''
        self.knapsack_capacity = knapsack_capacity
        self.inventory = inventory

    def fitness(self, solution):
        '''Compute the fitness of this solution against this instance.'''
        if solution.size() != self.inventory.size():
            raise Exception("Steal vector had size %d != %d" % \
                (solution.size(), self.inventory.size()))
        weight = 0
        value = 0
        for i in range(solution.size()):
            if int(solution.get_bit(i)):
                weight += self.inventory.weight(i)
                value += self.inventory.value(i)

        if weight <= self.knapsack_capacity:
            return value
        return 0

    def size(self):
        '''Return the number of items in this problem's inventory.'''
        return self.inventory.size()

    def __str__(self):
        ret = ""
        ret += "BinaryKnapsackProblem\n"
        ret += "Knapsack capacity: %d weight units\n" % self.knapsack_capacity
        ret += str(self.inventory)

        return ret


class BinaryKnapsackSolution():
    '''
    A solution to a BinaryKnapsackProblem. Treat as immutable.
    '''
    def __init__(self, solution):
        self.solution = solution

    def size(self):
        '''Return the number of bits in this solution.'''
        return len(self.solution)

    def reproduce(self, other):
        '''Construct a child instance
        by reproducing with the other instance.'''
        if self.size() != other.size():
            raise Exception("Parent lengths didn't match: %d, %d" % \
                (self.size(), other.size()))

        boundary = random.randint(0, self.size())
        child_solution = self.solution[0:boundary] + other.solution[boundary:]
        return BinaryKnapsackSolution(child_solution)

    def mutate(self):
        '''Construct a mutated version of this solution.'''
        mutated_solution = ""
        opposites = {"0": "1", "1": "0"}
        for bit in self.solution:
            if random.randint(0, 100) == 0:
                mutated_solution += opposites[bit]
            else:
                mutated_solution += bit
        return BinaryKnapsackSolution(mutated_solution)

    def get_bit(self, i):
        '''Get the bit at zero-based index i.'''
        return self.solution[i]

    def __str__(self):
        return "BinaryKnapsackSolution: [%s]" % self.solution


def demo(infile):
    '''Poor man's unit tests.'''
    problem = get_problem_from_file(infile)
    print problem
    print problem.size()
    problem = get_random_problem()
    population = get_random_population(problem)
    for member in population:
        print member
        print member.mutate()
        print problem.fitness(member)
        print member.get_bit(0)
    print population[0].reproduce(population[1])

    inventory = problem.inventory
    print inventory.weight(0)
    print inventory.value(0)
    item = inventory.get_bit(0)
    print item.weight
    print item.value


if __name__ == "__main__":
    demo("../data/10_instance.txt")
