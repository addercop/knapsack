#!/usr/bin/python
'''Helper script to generate problem instances and write them to stdout.'''
import sys
import knapsack


def print_random_problem(size):
    '''Print out a random problem instance of the given size.'''
    problem = knapsack.get_random_problem(size)
    print problem.knapsack_capacity
    for item in problem.inventory.items:
        print "%d %d" % (item.weight, item.value)


def main():
    '''Print a problem instance of the size given on command line, if given.'''
    if len(sys.argv) < 2:
        print_random_problem(20)
    else:
        print_random_problem(int(sys.argv[1]))


if __name__ == "__main__":
    main()
