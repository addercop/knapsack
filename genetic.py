#genetic.py
import random

def genetic_algorithm(instance,population_size=1000,generations=10000):
	'''A template method for running a genetic algorithm.'''
	population = instance.get_random_population(population_size)
	print "Starting with random population of size",len(population)

	for i in range(generations):
		print "Generation %d of %d" % (i+1,generations)
		current_max = max_score(instance,population)
		print "Current best fitness", current_max
		population = cull(instance,population,50)
		population = reproduce(population,population_size)
		population = [member.mutate() for member in population]

	best = max_scorers(instance,population)

	print ""
	print_report(instance,best,"Evolved solutions")

def print_report(instance,population,name):
	'''Format a report for a population assumed to all have the same score.'''
	print "Population name: %s" % name
	print "%d-way tie" % len(population)
	for member in population:
		print str(member)
	if len(population) > 0:
		print "Score: %d" % instance.fitness(population[0])

def cull(instance,population,percentile=10):
	scores = [instance.fitness(member) for member in population]
	sorted_scores = list(scores)
	sorted_scores.sort()
	cutoff = sorted_scores[ (len(population)/100) * percentile ]
	culled_population = [member for member in population if instance.fitness(member) > cutoff]

	if len(culled_population) == 0:
		max_score = max(scores)
		culled_population = [member for member in population if instance.fitness(member) == max_score]

	return culled_population
	

def reproduce(population,target_size):
	'''Create children from the population until the population reaches target size.'''
	children = []
	for i in range(target_size-len(population)):
		parent1 = random.choice(population)
		parent2 = random.choice(population)
		children.append(parent1.reproduce(parent2))
	population.extend(children)
	return population

def max_score(problem_instance,population):
	scores = [problem_instance.fitness(member) for member in population]
	return max(scores)

def max_scorers(problem_instance,population):
	score = max_score(problem_instance,population)
	return [member for member in population if problem_instance.fitness(member) == score]
