import random
import math

def calcular_distancia_total(rota, matriz_distancias):
    distancia = 0
    for i in range(len(rota) - 1):
        distancia += matriz_distancias[rota[i]][rota[i+1]]
    # Retorno à origem
    distancia += matriz_distancias[rota[-1]][rota[0]]
    return distancia

def calcular_fitness(rota, matriz_distancias):
    dist = calcular_distancia_total(rota, matriz_distancias)
    return 1 / dist if dist != 0 else 0

def criar_individuo(num_cidades):
    rota = list(range(num_cidades))
    random.shuffle(rota)
    return rota