#!/usr/bin/python
'''Main driver for genetic algorithm application.'''

import sys

import knapsack
import solutions

sys.setrecursionlimit(2000)


def main():
    '''Read a 0-1 knapsack problem instance from a file and solve it.'''
    if len(sys.argv) < 2:
        print "Usage: main.py FILE"
        return
    problem = knapsack.get_problem_from_file(sys.argv[1])
    solutions.solve(problem)

if __name__ == "__main__":
    main()
