# Genetic-Algorithm
Search for the optimized gene containing all the adaptability characteristics of a plant

Descripción del problema:

Los biólogos de los invernaderos Hierbas, S.A. están trabajando buscando un nuevo tipo de cultivo que se adapte a unas condiciones climáticas específicas. Las plantas están destinadas al consumo humano y sólo son aprovechables las hojas. Los ingenieros genéticos han precisado que las características más importantes que se quieren explotar se centran en los siguientes genes: resistencia a la humedad (con valores Alta o Baja), resistencia al calor (Alta, Baja), número de hojas (Alto, Bajo) y altura del tallo (Alto, Bajo). El cromosoma estará formado por estos cuatro genes en el orden dado.

El objetivo es encontrar una planta que tenga alta resistencia a la humedad y al calor, con un número alto de hojas y con un tallo bajo. El cromosoma que expresa esta cadena de genes es **AAAB**.
Para medir la calidad de una planta se sumará una cantidad para aquellos genes que coincidan con los del objetivo. La cantidad que se suma dependerá de cada gen:

- Se sumarán 2 puntos para coincidencias con el gen referente a la resistencia a la humedad.
  
- 2 puntos para coincidencias con el gen referente a la resistencia al calor.
  
- 3 puntos si coincide el gen del número de hojas.
  
- 1 punto para coincidencias con el gen de la altura del tallo.
  
- 0 puntos si no hay coincidencia entre cuales quiera de los genes.
  

**Requerimientos del problema:**

1. Calcular 2 generaciones utilizando el método estándar de selección y sabiendo que la probabilidad de emparejamiento es **Pe = 0,7** y la de mutación **Pm = 0,1**. La población inicial consta de 4 individuos: BAAA, BBBB, ABBA, BABA.
  
2. Para realizar la mutación se utilizará el procedimiento de mirar gen a gen y en caso de que haya que aplicarla, simplemente se alterará el valor del gen por su complementario (sin elegir al azar el nuevo valor).
  

## Solución - Explicación paso por paso

Para darle solución a este problema se han creado una serie de métodos que realizan cada uno una tarea específica. Se definió una clase para modelar el funcionamiento del asunto genético en una población dada. Para ello es necesario tener un modelo deseado que en este caso es **target**, un número de individuos por población, un número de seleccionados que en este caso es por pareja, la probabilidad de mutación y el número de generaciones que se desea modelar.

```python
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
```

En primer lugar se tiene que crear una población para poder crear una generación y para ello, se utilizan los siguientes métodos (tener en cuenta que la población serán listas de cadenas conformadas por las letras **A** y **B**).

Esta función crea los individuos aleatoria mente con una longitud de 4.

```python
def create_individual(self, min = 0, max = 9):
    individual = [random.choice(['A', 'B']) for i in range(len(self.target))]
    return individual
```

Ahora, se crea una población con un total de 4 individuos, llamando la función **create_individual**. Aquí se tuvo en cuenta que no pueden haber miembros de la población iguales.

```python
  #crea una población de individuos aleatorios
  def create_population(self):
    population = []
    while len(population) < self.n_individuals:
        individual = self.create_individual()
        if individual not in population:
            population.append(individual)
    return population
```

Una vez creada la población es necesario calcular el fitness de cada individuo de la población. Para realizar esto, se usará la siguiente función que devuelve una lista con el fitness de cada individuo. Para hallar el fitness se tuvo en cuenta las condiciones de los requerimientos dichos en la descripción del problema. Como dato extra, la forma en que se calculó el fitness en este problema es un caso de las muchas formas en que se podría hacer.

```python
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
```

Una vez que se tenga la lista de los fitness es importante calcular la probabilidad de cada uno de esos individuos, por lo tanto se usa la siguiente función:

```python
  def probabilityes(self, list_fitness):
    probabilities = [i/sum(list_fitness) for i in list_fitness]
    return probabilities
```

Para resolver este problema en especifico se tienen que hacer cruces entre dos individuos, y teniendo 4 individuos se seleccionarán dos parejas, que no pueden estar conformadas por dos individuos con material genético igual, tienen que ser totalmente diferentes. Para elegir a esas parejas se utiliza la siguiente función:

```python
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
```

El funcionamiento de la función **selection** consiste en la elección de dos individuos de la población teniendo en cuenta un factor de probabilidad aleatorio, es decir, con una variable aleatoria se elige un porcentaje del 0 al 1, y teniendo la lista de probabilidades de cada individuo se elegirá a cada miembro del individuo si el número aleatorio cae en el intervalo de probabilidad de algún individuo de la población tomando el límite más cercano a ese valor. Esta función de selección esta diseñada para buscar una pareja, pero se necesitan dos parejas así que es necesario llamarla dos veces.

Luego de realizar la elección de parejas, en cada una se debe realizar un cruzamiento que va a dar como resultado hijos derivado de sus genes. Para realizar este cruce se toma una pareja, y luego para cada uno de los miembros de esa pareja se realiza un corte en una posición dada, para calcular esta posición se distribuye una lista de probabilidades que van de la siguiente forma: **[-1, 0.25, 0.50, 0.75]**, y teniendo en cuenta un una probabilidad aleatoria se calcula en qué intérvalo está y por ende se elige el límite más cercano, que en este caso representa el índice de la posición que se quiere cortar.

```python
 def crossover(self, selection):
    childs = []
    # Probability for each element of the list [0.25, 0.50, 0.75, 1.00]
    p_crossover = [-1, 0.25, 0.50, 0.75]
    
    cut = np.random.uniform(0, 1)
    closest_index = min(range(len(p_crossover)), key=lambda i: abs(p_crossover[i] - cut))

    childs.append(selection[0][:closest_index] + selection[1][closest_index:])
    childs.append(selection[1][:closest_index] + selection[0][closest_index:])
    
    return childs
```

Una vez realizados los cortes correspondientes, se formarán los hijos realizando una mezcla entre los cortes.

Luego, teniendo la lista de hijos, se debe realizar una serie de mutaciones. Teniendo la lista de hijos, a cada una de sus elementos se le asignará una probabilidad aleatoria la cual se usará para verificar que en cada uno de los hijos y si en algún elemento se debe hacer un intercambio de gen, es decir, cambiar el gen por su complemento (A por B o B por A). Es importante tener en cuenta que este cambio solo se hará si o si la probabilidad aleatoria seleccionada es menor que la tasa de mutación, en este problema es 0.1.

```python
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
```

y listo!, se devolverá una lista con los hijos de esa generación, y esa lista será la población para la siguiente población a calcular.

Ahora como en nuestro problema son dos generaciones, entonces todas las funciones se tienen que llamar dos veces, para resumirlo se creó la siguiente función **generations**:

```python
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
```

En el **main** establecemos el individuo ideal que es el **target**.

```python
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
```

Se crea una población y para esta población inicial se derivan dos generaciones.

Como el objetivo de este caso es buscar la mejor combinación de genes de plantas más resistentes, se comparan las poblaciones resultantes de la generación 1 y 2, mediante sus fitness, para buscar el mayor fitness.

```python
 if model.best_individual(model.set_fitness[0]) >= model.best_individual(model.set_fitness[1]):
   print("The best individual is: ", p[model.best_individual(model.set_fitness[0])])
```

La función que busca el mejor fitness de cada población es:

```python
  def best_individual(self, list_fitness):
    best = max(list_fitness)
    index = list_fitness.index(best)
    return index
```

Al final se imprime el resultado deseado!
