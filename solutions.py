#!/usr/bin/python
import knapsack


class BinaryKnapsackSolver():
	def __init__(self,instance):
		self.instance = instance
		
	def solve(self):
		raise Exception("Method not implemented")

class BruteForceBinaryKnapsackSolver(BinaryKnapsackSolver):
	pass

class PruningBruteForceBinaryKnapsackSolver(BinaryKnapsackSolver):
	pass

class DynamicProgrammingBinaryKnapsackSolver(BinaryKnapsackSolver):
	pass