#!/usr/bin/python
#main driver for genetic algorithm application.
import sys

import genetic
import knapsack

sys.setrecursionlimit(2000)

def main():
	if len(sys.argv) < 2:
		print "Usage: main.py FILE"
		return
	instance = knapsack.get_binaryknapsackinstance_from_file(sys.argv[1])
	print instance

	genetic.genetic_algorithm(instance)

	if instance.size() <= 30:
		knapsack.branch_and_bound(instance)

if __name__ == "__main__":
	main()
