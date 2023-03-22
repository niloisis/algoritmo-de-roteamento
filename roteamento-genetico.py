import random

# Parâmetros do Algoritmo Genético
POPULATION_SIZE = 10
REPRODUCTION_RATE = 50
MUTATION_PROBABILITY = 0.5
STOP_CRIT = 75

# Leitura da matriz de entrada e armazenamento dos pontos de entrega
file = open('input-tests/input-02', 'r')
line = file.readline()

origin = []
coordinates = {}
points = []

row_counter = 0
for line in file:
    column_counter = 0
    for char in line:
        if char == '0':
            column_counter += 1
        elif char == 'R':
            origin = [row_counter, column_counter]
            column_counter += 1
        elif char != '\n' and char != ' ':
            coordinates[char] = [row_counter, column_counter]
            column_counter += 1
            points.append(char)
    row_counter += 1

points = sorted(points)
file.close()


# Função de avaliação da aptidão dos indivíduos
# (qualidade das soluções geradas em cada geração)
def fitness(population):
    # população de indivíduos, onde cada indivíduo é representado por uma lista
    # representa a ordem de visita aos pontos de entrega
    fitness_pop = []
    for i in range(len(population)):
        soma_dist = 0
        pt = str(population[i][0])
        soma_dist += manhattan_distance(origin[1], origin[0], coordinates[pt][0], coordinates[pt][1])
        for j in range(len(population[i])):
            if j == len(population[i]) - 1:
                pt = str(population[i][j])
                soma_dist += manhattan_distance(coordinates[pt][0], coordinates[pt][1], origin[1], origin[0])
                # adiciona a distância do último ponto de volta ao ponto de origem
                if pt != str(population[i][0]):
                    soma_dist += manhattan_distance(coordinates[pt][0], coordinates[pt][1],
                                                    coordinates[str(population[i][0])][0],
                                                    coordinates[str(population[i][0])][1])
            else:
                pt_a = str(population[i][j])
                pt_b = str(population[i][j + 1])
                soma_dist += manhattan_distance(coordinates[pt_a][0], coordinates[pt_a][1],
                                                coordinates[pt_b][0], coordinates[pt_b][1])
        fitness_pop.append([soma_dist, population[i]])
    return fitness_pop


# Função de cálculo da distância de Manhattan
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Função de seleção dos pais por roleta
def selection(population, reproduction_rate):
    pop = population * 1      # armazena cópia da população original
    count = 0
    fathers = []
    # quantidade de pais que devem ser selecionados para reprodução:
    rate = int(len(population) * ((reproduction_rate / 2) / 100))
    while count < rate:
        father = []
        for i in range(0, 2):
            limite = round(pop[int(len(pop) / 2)][3], 2)    # limite máximo da roleta
            # valor entre o menor valor de aptidão da população e o limite calculado
            pont_roul = round(random.uniform(pop[0][3] - 1, limite), 2)
            for j in range(0, len(pop) - 1):
                if j == 0:
                    inferior_lim = 0
                    superior_lim = pop[j][3]
                    if inferior_lim < pont_roul <= superior_lim:
                        father.append(pop[j])
                        pop.remove(pop[j])
                        break
                else:
                    inferior_lim = pop[(j - 1)][3]
                    superior_lim = pop[j][3]
                    if inferior_lim < pont_roul <= superior_lim:
                        father.append(pop[j])
                        pop.remove(pop[j])
                        break
        fathers.append(father)
        count += 1
    return fathers


# Função de Crossover
def crossover(father, mutation_probability):
    new_population = []
    ponto_corte = random.randint(1, len(father[0][0][1]) - 1)
    for i in range(0, len(father) - 1):
        father1 = father[i][0][1]
        father2 = father[i][1][1]
        child1 = father1[0:ponto_corte] + father2[ponto_corte:len(father2)]
        child2 = father2[0:ponto_corte] + father1[ponto_corte:len(father1)]
        child1 = mutation(child1, mutation_probability)
        child2 = mutation(child2, mutation_probability)
        organize(father1, child1)
        organize(father1, child2)
        new_population.append(child1)
        new_population.append(child2)
    new_population = sorted(fitness(new_population))
    return new_population


# Função de Mutação (troca de posição)
def mutation(child, mutation_rate):
    rate = random.uniform(0.0, 1.0)
    if rate < mutation_rate:
        id1 = random.randint(0, len(child) - 1)
        id2 = random.randint(0, len(child) - 1)
        child[id1], child[id2] = child[id2], child[id1]
    return child


# Função para impedir que pontos faltem e estejam repetidos
def organize(father, child):
    repeated_char = [k for k in father if child.count(k) > 1]
    missing_char = list(set(father).difference(set(child)))
    index = []
    if not repeated_char:
        return child
    else:
        for i in range(0, len(repeated_char)):
            c = 0
            for x in range(0, len(child)):
                if child[x] == repeated_char[i]:
                    c += 1
                    if c > 1:
                        index.append(x)
    for j in range(0, len(index)):
        child[index[j]] = missing_char[j]
    return child


# Função para ajuste e substituição da população
def substitution(population, population_size):
    while len(population) > population_size:
        size = len(population)
        individual1 = random.randint(0, size - 1)
        individual2 = random.randint(0, size - 1)
        if individual1 != individual2:
            if population[individual1][0] < population[individual2][0]:
                population.remove(population[individual2])
            else:
                population.remove(population[individual1])
    return population


# Algoritmo Genético
def genetic_algorithm(point, population_size, reproduction_rate, mutation_probability, stop_crit):
    # Inicializando a população
    population = []
    cont = 0
    while cont < population_size:
        pt = point * 1
        individual = []
        for i in range(0, len(point)):
            idt = random.randint(0, len(pt) - 1)
            individual.append(pt[idt])
            pt.remove(pt[idt])
        population.append(individual)
        cont += 1

    # Calculando 'fitness' da primeira população
    population = sorted(fitness(population))

    # Calculando 'fitness' das próximas populações
    generation = 1
    for k in range(stop_crit):
        total_fitness = 0
        for i in range(0, population_size):
            total_fitness = total_fitness + population[i][0]
        population = sorted(population)

        # Calculando probabilidades da seleção por roleta
        floor = 0
        for i in range(0, population_size):
            population[i].append(round(total_fitness / population[i][0], 2))
            population[i].append(round(floor + population[i][2], 2))
            floor = round(floor + population[i][2] + 0.01, 2)

        # Retornando os pares de pai para crossover
        fathers = selection(population, reproduction_rate)
        new_population = crossover(fathers, mutation_probability)
        population = sorted(population + new_population)

        # Ajuste populacional
        population = substitution(population, population_size)
        generation += 1
    return population


ag = genetic_algorithm(points, POPULATION_SIZE, REPRODUCTION_RATE, MUTATION_PROBABILITY, STOP_CRIT)
print("Solução ótima: {} | {}".format(ag[0][0], ag[0][1]))
