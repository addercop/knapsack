#!/usr/bin/python

import sys
import random

def make_random_instance(length):
	items = []

	weight_min = 10
	weight_max = 100

	value_min = 20
	value_max = 200

	capacity = (((weight_min + weight_max)/2) * length)/10

	for i in range(length):
		items.append( (random.randint(weight_min,weight_max), random.randint(value_min,value_max) ) )

	print capacity
	for item in items:
		print item[0], item[1]
	


def main():
	make_random_instance(int(sys.argv[1]))

if __name__ == "__main__":
	main()
