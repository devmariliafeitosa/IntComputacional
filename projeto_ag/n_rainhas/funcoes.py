import random

def criar_individuo(n):
    # Cada índice é uma coluna, o valor é a linha (0 a n-1)
    return [random.randint(0, n-1) for _ in range(n)]

def calcular_fitness(cromossomo):
    n = len(cromossomo)
    conflitos = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            # Mesma linha (se não usarmos permutação pura)
            if cromossomo[i] == cromossomo[j]:
                conflitos += 1
            # Diagonais
            elif abs(i - j) == abs(cromossomo[i] - cromossomo[j]):
                conflitos += 1
                
    # Fitness máximo é quando conflitos = 0
    # Usamos uma base grande para maximização: (n*(n-1)/2)
    max_conflitos = (n * (n - 1)) // 2
    return max_conflitos - conflitos

def mutacao(cromossomo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        ponto = random.randint(0, len(cromossomo) - 1)
        cromossomo[ponto] = random.randint(0, len(cromossomo) - 1)
    return cromossomo

def cruzamento(pai1, pai2):
    # Cruzamento de ponto único
    ponto = random.randint(1, len(pai1) - 2)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2