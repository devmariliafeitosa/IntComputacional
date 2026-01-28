import random

def torneio(populacao, fitnesses, k=3):
    # Seleciona k indivíduos aleatórios e retorna o melhor deles
    selecionados = random.sample(list(zip(populacao, fitnesses)), k)
    selecionados.sort(key=lambda x: x[1], reverse=True)
    return selecionados[0][0]