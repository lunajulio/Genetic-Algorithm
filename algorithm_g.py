# -*- coding: utf-8 -*-
"""Algorithm-G.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eTT6WjevBXThHiMAuR49ZZ0SOmDYRdzJ
"""

import numpy as np
import random
import csv

class genetic_A():
  #Declarated object about our model 
  def __init__(self, target, n_individuals, n_selection, mutation_rate, n_generations, probabilities = []):
    self.target = target
    self.n_individuals = n_individuals
    self.n_selection = n_selection
    self.mutation_rate = mutation_rate
    self.n_generations = n_generations
    self.probabilities = probabilities
    self.set_fitness = []
    self.set_probabilities = []
  
  #dada una lista de fitness, calcula la probabilidad de cada individuo
  def probabilityes(self, list_fitness):
    probabilities = [i/sum(list_fitness) for i in list_fitness]
    return probabilities

  #crea un individuo aleatorio
  def create_individual(self, min = 0, max = 9):
    individual = [random.choice(['A', 'B']) for i in range(len(self.target))]
    return individual
  
  #crea una población de individuos aleatorios
  def create_population(self):
    population = []
    while len(population) < self.n_individuals:
        individual = self.create_individual()
        if individual not in population:
            population.append(individual)
    return population

  #dada una población, calcula el fitness de cada individuo
  def fitness(self, population):
    # Evaluar el individuo
    list_fitness = []
    for i in range(len(population)):
      fitness = 0
      for j in range(len(population[i])):
        #ingresar a una posicion del individuo
        if population[i][j] == self.target[j]:
          if j == 0:
            fitness += 2 
          if j == 1:
            fitness += 2
          if j == 2:
            fitness += 3
          if j == 3:
            fitness += 1
      list_fitness.append(fitness)
        
    return list_fitness
  
  #dada una lista de lista de los fitness de cada individuo, selecciona un individuo de la población con mayor fitness
  def best_individual(self, list_fitness):
    best = max(list_fitness)
    index = list_fitness.index(best)
    return index

  #dada una lista de probabilidades acumuladas y un número aleatorio, selecciona un individuo de la población
  def random_choice(self, cumulative_probabilities):
    choice = np.random.uniform()
    selected_index = next(i for i, p in enumerate(cumulative_probabilities) if choice < p)
    return selected_index


  def selection(self, population, list_probabilities):
    selected = []
    remaining_population = population.copy()  # Crear una copia de la población original

    for _ in range(self.n_selection):
        cumulative_probabilities = np.cumsum(list_probabilities)
        choice = np.random.uniform()
        selected_index = next(i for i, p in enumerate(cumulative_probabilities) if choice < p)
        selected_individual = remaining_population[selected_index]
        selected.append(selected_individual)
        remaining_population.remove(selected_individual)  # Eliminar el individuo seleccionado

        # Recalcular las probabilidades y la lista de probabilidades después de cada selección
        list_probabilities = self.probabilityes(self.fitness(remaining_population))

    return selected
  
  #dada una lista de individuos, realiza el cruce entre ellos
  def crossover(self, selection):
    childs = []
    # Probability for each element of the list [0.25, 0.50, 0.75, 1.00]
    p_crossover = [-1, 0.25, 0.50, 0.75]
    
    cut = np.random.uniform(0, 1)
    closest_index = min(range(len(p_crossover)), key=lambda i: abs(p_crossover[i] - cut))

    childs.append(selection[0][:closest_index] + selection[1][closest_index:])
    childs.append(selection[1][:closest_index] + selection[0][closest_index:])
    
    return childs

  #dada una lista de individuos, realiza la mutación de cada uno de ellos
  def mutation(self, childs):
    for i in range(len(childs)):
      #create a list with random probabilities
      p_mutation = np.random.uniform(0, 1, len(childs[i]))
      for j in range(len(childs[i])):
        if p_mutation[j] <= self.mutation_rate:
          if childs[i][j] == 'A':
            childs[i][j] = 'B'
          else:
            childs[i][j] = 'A'
    return childs
  
  #dada una población, realiza el algoritmo genético
  def generations(self, population):
        f = self.fitness(population)
        self.set_fitness.append(f)
        print("Fitness: ", f)
        while f == [0,0,0,0]:  
          p = self.create_population()
          f = self.fitness(p)
        proba = self.probabilityes(f)
        self.set_probabilities.append(proba)
        print("Probabilities: ", proba)
        selected1 = self.selection(population, proba)
        selected2 = self.selection(population, proba)
        print("Selected 1: ", selected1)
        while selected1 == selected2:
          selected2 = self.selection(population, proba)
        print("Selected 2: ", selected2)
        crossover1 = self.crossover(selected1)
        crossover2 = self.crossover(selected2)
        crossover = crossover1 + crossover2
        print("Crossover: ", crossover)
        mutation = self.mutation(crossover)
        print("Mutation: ", mutation)
        population = mutation
        return population

def main():
  #Create a list with the gen that we want
  target = ['A', 'A', 'A', 'B']
  model = genetic_A(target = target,n_individuals = 4, n_selection = 2,mutation_rate=0.1, n_generations = 2, probabilities = [])
  p = model.create_population()
  print("Generation 1: ")
  print("Population: ",p)
  gen1 = model.generations(p)
  print("Generation 2: ")
  gen2 = model.generations(gen1)

  if model.best_individual(model.set_fitness[0]) >= model.best_individual(model.set_fitness[1]):
    print("The best individual is: ", p[model.best_individual(model.set_fitness[0])])

  # Save the data to a CSV file
  with open('genetic_data.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['Population', 'Fitness', 'Probabilities'])
      #save the data of the first generation
      for i in range(len(p)):
        writer.writerow([p[i], model.set_fitness[0][i], model.set_probabilities[0][i]])
  with open('genetic_data2.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      #save the data of the second generation
      for i in range(len(gen1)):
        writer.writerow([gen1[i], model.set_fitness[1][i], model.set_probabilities[1][i]])
      





if __name__ == '__main__':
  main()