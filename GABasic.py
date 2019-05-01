import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10
POP_SIZE = 100
CROSS_RATE = 0.8
MUTATION_RATE = 0.8
N_GENERATIONS = 200
X_BOUND = [0, 5]

def F(x): return np.sin(10 * x) * x + np.cos(2 * x) * x
    
#find non-zero fitness for selection

def get_fitness(pred): return pred + 1e-3-np.min(pred)

def translateDNA(pop): return pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * X_BOUND[1]
    
def select(pop, fitness):
    #nature selection wrt pop's fitness

    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True, p=fitness / fitness.sum())
    print(idx)
    return pop[idx]

def crossover(parent, pop):  #mating process (genes crossover)
        #parent zhi shi yi ge dan du de DNA ran se ti , gai bian ta ben shen de yige difang ji ke.
    if np.random.rand() < CROSS_RATE:
        i_ = np.random.randint(0, POP_SIZE, size=1)
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        parent[cross_points] = pop[i_, cross_points]
    return parent


def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child

# begin

pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))

plt.ion()  # something about plotting

x = np.linspace(*X_BOUND, 200)
plt.plot(x, F(x))


for _ in range(N_GENERATIONS):
    F_values = F(translateDNA(pop))
    
    #something about plotting

    if 'sca' in globals(): sca.remove()
    sca = plt.scatter(translateDNA(pop), F_values, s=200, lw=0, c='red', alpha=0.5); plt.pause(0.05)
    
    #GA part
    fitness = get_fitness(F_values)
    print("Most fitted DNA: " ,pop[np.argmax(fitness),:])
    pop = select(pop, fitness)
    pop_copy = pop.copy()
    for parent in pop:
        child = crossover(parent, pop_copy)
        child = mutate(child)
        parent[:] = child

plt.ioff(); plt.show()
    

