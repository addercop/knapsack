#!/usr/bin/python
#Suffers minor primitive obsession. Upgrade weight/value tuples to proper class.
#knapsack.py
import random
import sys
pruned = 0
def get_binaryknapsackinstance_from_file(filename):
	contents = open(filename,"r").read()
	contents = contents.split("\n")
	capacity = int(contents[0])
	pairs = []
	for line in contents[1:]:
		if len(line) <= 1:
			break
		sline = line.split()
		weight, value = int(sline[0]),int(sline[1])
		pairs.append((weight,value))

	return BinaryKnapsackInstance(capacity,pairs)

def get_random_instance(size=100):
	'''
	Create a random problem instance of 'size' number of weight/value pairs.
	'''
	pairs = []
	knapsack_capacity = 200
	weight_min = 10
	weight_max = 20
	value_min = 1
	value_max = 1000
	for i in range(size):
		pairs.append(  (random.randint(weight_min,weight_max), random.randint(value_min,value_max)   ))

	return BinaryKnapsackInstance(knapsack_capacity,pairs)

def compare_items(x,y):
	'''Sort first by increasing weight. If weights are equal, use decreasing value as a tiebreaker.'''
	if x[0] < y[0]:
		return -1
	elif x[0] == y[0]:
		if x[1] < y[1]:
			return 1 #!
		elif x[1] == y[1]:
			return 0
		elif x[1] > y[1]:
			return -1 #!
	elif x[0] > y[0]:
		return 1

class BinaryKnapsackInstance():
	'''
	A representation of the knapsack problem for a store with only one of each item.
	Each item can either be stolen or not.
	'''
	def __init__(self,knapsack_capacity,store_items = [(0,0)]):
		self.knapsack_capacity = knapsack_capacity
		#weight/value pairs. treat as immutable.
		self.store_items = list(store_items)
		self.store_items.sort(compare_items)

	def evaluate(self,solution):
		'''Compute the total (fitness,weight) of this solution against this instance.'''
		if solution.length() != len(self.store_items):
			raise Exception("Steal vector had len %d != %d" % (solution.length(), len(self.store_items)))
		fitness = 0
		weight = 0
		value = 0
		for i in range(solution.length()):
			if int(solution.at(i)):
				weight += self.store_items[i][0]
				value += self.store_items[i][1]

		if weight <= self.knapsack_capacity:
			fitness = value
		else:
			fitness = 0

		return (fitness,weight)

	def fitness(self,solution):
		return self.evaluate(solution)[0]

	def weight(self,solution):
		return self.evaluate(solution)[1]

	def get_random_population(self,size):
		'''Return a list of /size/ random solutions for this instance.'''
		return [self.get_random_solution() for i in range(size)]

	def get_random_solution(self):
		'''Return a random solution with weight less than knapsack capacity.'''
		#add random items until adding the next item would exceed capacity.
		vector = ['0']*len(self.store_items)
		indexes = range(0,len(self.store_items)-1)
		random.shuffle(indexes)
		total_weight = 0
		for i in indexes:
			item = self.store_items[i]
			if total_weight + item[0] > self.knapsack_capacity:
				break
			total_weight += item[0]
			vector[i] = '1'
			
		return BinaryKnapsackSolution("".join(vector))

	def get_best_solutions(self):
		'''Big-theta(2**n) exhaustive search for a best solutions.'''
		width = len(self.store_items)
		best_solutions = []
		best_fitness = -1

		for i in xrange(0,2**width):
			right = bin(i)[2:]
			solution_string = '0'*(width-len(right)) + right
			#print solution_string
			solution = BinaryKnapsackSolution(solution_string)
			fitness = self.fitness(solution)
			if fitness > best_fitness:
				best_solutions = [solution]
				best_fitness = fitness
			elif fitness == best_fitness:
				best_solutions.append(solution)

		return best_solutions

	def get_solutions_fast(self):
		'''Branch-and-bound pruning version of brute-force 2**n search.'''
		best_solutions = []
		best_fitness = self._get_solutions_fast(best_solutions,-1,0,0,0,"")
		print "Best fitness", best_fitness
		return best_solutions

	def _get_solutions_fast(self,best_solutions,best_score,weight,value,index,partial_solution):
		'''Private recursive search.'''
		if weight > self.knapsack_capacity:
			remainder = len(self.store_items) - len(partial_solution)
			global pruned
			pruned += 2**remainder
			print "Total pruned: %d" % pruned
			return 0
		if index == len(self.store_items) or weight == self.knapsack_capacity:
			partial_solution = partial_solution + "0"*(len(self.store_items) - len(partial_solution))
			if weight > self.knapsack_capacity:
				fitness = 0
			else:
				fitness = value 
			if fitness > best_score:
				while len(best_solutions) > 0:
					best_solutions.pop()
				print "New best fitness %d" % fitness
				bks = BinaryKnapsackSolution(partial_solution)
				print bks
				best_solutions.append(bks)
			elif fitness == best_score:
				print "Tied with best fitness %d" % fitness
				bks = BinaryKnapsackSolution(partial_solution)
				print bks
				best_solutions.append(bks)
			return fitness

		steal_weight = weight + self.store_items[index][0]
		steal_value  = value  + self.store_items[index][1]
		steal_score  = self._get_solutions_fast(best_solutions, best_score, steal_weight, steal_value, index+1, partial_solution+"1")
		best_score   = max(best_score, steal_score)
			
		leave_score = self._get_solutions_fast(best_solutions, best_score, weight, value,index+1, partial_solution+"0")
		best_score = max(best_score, leave_score)

		return best_score

	def maximum_profit(self):
		'''Dynamic programming algorithm to return maximum possible profit value.'''
		#Want m(self.size(),self.knapsack_capacity)
		return self._m(self.size(),self.knapsack_capacity)

	def _m(self,i,w):
		#i only decreases, so the base case is when i<0
		if i<0:
			return 0
		w_i = self.store_items[index][0]
		v_i = self.store_items[index][1]
		#m(i,w) = m(i-1,w) if w_i > w, addition of new item exceeds capacity.
		#This is the base case when we can no longer spend weight to obtain profit.
		

		#m(i,w) = max( m(i-1,w), m(i-1,w-w_i)+v_i ) otherwise
		#In this recursive case, we spend some weight to obtain some profit.
		pass

	def summary(self,solution):
		weight = self.weight(solution)
		total_weight = self.get_total_weight()

		value = self.fitness(solution)
		total_value = self.get_total_value()
		
		s = ""
		s += "%s\n" % solution
		s += "Fullness: %d of %d, %2.1f%%\n" % (weight, self.knapsack_capacity, 100*((weight*1.0)/self.knapsack_capacity))
		s += "Weight: %d of %d, %2.1f%%\n" % (weight, total_weight, 100*((weight*1.0)/total_weight))
		s += "Value: %d of %d, %2.1f%%\n" % (value, total_value, 100*((value*1.0)/total_value))

		return s
	
	def get_total_weight(self):
		return sum([item[0] for item in self.store_items])

	def get_total_value(self):
		return sum([item[1] for item in self.store_items])

	def size(self):
		return len(self.store_items)
			
	def __str__(self):
		s = ""
		s += "BinaryKnapsackInstance\n"
		s += "Knapsack capacity: %d weight units\n" % self.knapsack_capacity
		s += "Item count: %d\n" % len(self.store_items)
		s += "Weight/value\n"
		for item in self.store_items:
			s += "%d %d\n" % (item[0],item[1])

		return s

class BinaryKnapsackSolution():
	'''
	An immutable solution to a BinaryKnapsackInstance.
	'''
	def __init__(self,s):
		self.solution = s

	def length(self):
		return len(self.solution)

	def reproduce(self,other):
		if self.length() != other.length():
			raise Exception("Parent lengths didnt match: %d, %d" % (self.length(), other.length()))

		boundary = random.randint(0,self.length())
		child_solution = self.solution[0:boundary] + other.solution[boundary:]
		return BinaryKnapsackSolution(child_solution)

	def mutate(self):
		mutated_solution = ""
		opposites = {"0":"1","1":"0"}
		count = 0
		for c in self.solution:
			if random.randint(0,100) == 0:
				mutated_solution += opposites[c]
				count += 1
			else:
				mutated_solution += c
		return BinaryKnapsackSolution(mutated_solution)

	def at(self,i):
		return self.solution[i]

	def __str__(self):
		return "BinaryKnapsackSolution: [%s]" % self.solution

def brute_force(problem):
	solutions = problem.get_best_solutions()
	print "Brute force summary:"
	for s in solutions:
		print problem.summary(s)

def branch_and_bound(problem):
	solutions = problem.get_solutions_fast()
	print "Branch and bound summary:"
	for s in solutions:
		print problem.summary(s)
	total =  2**(len(problem.store_items))
	print "Total search space size" , total
	global pruned
	print "Pruned", pruned 
	percentage = ((total-pruned)*1.0)/(1.0*total) * 100.0
	print "Only searched %2.1f%% of search space" % percentage

def demo(infile):
	problem = get_binaryknapsackinstance_from_file(infile)
	#brute_force(problem)
	branch_and_bound(problem)

def main():
	demo(sys.argv[1])

if __name__ == "__main__":
	main()
