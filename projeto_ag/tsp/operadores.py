import random

def cruzamento_pmx(pai1, pai2):
    tamanho = len(pai1)
    f1, f2 = [None]*tamanho, [None]*tamanho
    
    # Seleciona dois pontos de corte
    p1, p2 = sorted(random.sample(range(tamanho), 2))
    
    # Copia o segmento central
    f1[p1:p2+1] = pai1[p1:p2+1]
    f2[p1:p2+1] = pai2[p1:p2+1]
    
    # Função auxiliar para preencher o restante sem repetir
    def preencher(filho, pai_doador, segmento):
        for i in range(tamanho):
            if i < p1 or i > p2:
                val = pai_doador[i]
                while val in segmento:
                    # Mapeamento: encontra onde o valor está no outro pai e pega o correspondente
                    idx_no_outro = pai_doador.index(val)
                    # Lógica simplificada de mapeamento para garantir permutação
                    val = pai_doador[(idx_no_outro + 1) % tamanho] 
                    # Nota: Para um PMX rigoroso, usa-se um dicionário de mapeamento.
                    # Esta é uma versão funcional para garantir validade.
                filho[i] = val

    # Implementação simplificada de preenchimento de permutação
    def completar_permutacao(filho, pai):
        existentes = set(filho)
        indices_vazios = [i for i, x in enumerate(filho) if x is None]
        valores_faltantes = [x for x in pai if x not in existentes]
        for i, idx in enumerate(indices_vazios):
            filho[idx] = valores_faltantes[i]
        return filho

    return completar_permutacao(f1, pai2), completar_permutacao(f2, pai1)

def mutacao_troca(cromossomo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromossomo)), 2)
        cromossomo[idx1], cromossomo[idx2] = cromossomo[idx2], cromossomo[idx1]
    return cromossomo