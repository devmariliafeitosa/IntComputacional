from .funcoes import criar_individuo, calcular_fitness, mutacao, cruzamento
from comum.selecao import torneio

def executar_ag_rainhas(n, tam_populacao, geracoes, taxa_mutacao):
    populacao = [criar_individuo(n) for _ in range(tam_populacao)]
    historico_fitness = []

    for geracao in range(geracoes):
        fitnesses = [calcular_fitness(ind) for ind in populacao]
        melhor_fitness = max(fitnesses)
        historico_fitness.append(melhor_fitness)

        # Se encontrou a solução perfeita (zero conflitos)
        if melhor_fitness == (n * (n - 1)) // 2:
            print(f"Solução encontrada na geração {geracao}!")
            break

        nova_populacao = []
        while len(nova_populacao) < tam_populacao:
            pai1 = torneio(populacao, fitnesses)
            pai2 = torneio(populacao, fitnesses)
            
            f1, f2 = cruzamento(pai1, pai2)
            nova_populacao.append(mutacao(f1, taxa_mutacao))
            if len(nova_populacao) < tam_populacao:
                nova_populacao.append(mutacao(f2, taxa_mutacao))
        
        populacao = nova_populacao

    return populacao[0], historico_fitness