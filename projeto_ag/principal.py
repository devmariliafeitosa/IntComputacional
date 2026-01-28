from n_rainhas.algoritimo import executar_ag_rainhas

def testar_n_rainhas():
    print("\n--- Configuração N-Rainhas ---")
    n = int(input("Número de Rainhas (ex: 8): "))
    pop = int(input("Tamanho da População (ex: 100): "))
    ger = int(input("Máximo de Gerações (ex: 200): "))
    mut = float(input("Taxa de Mutação (0.0 a 1.0): "))

    print("\nEvoluindo...")
    melhor_solucao, historico = executar_ag_rainhas(n, pop, ger, mut)
    
    print("-" * 30)
    print(f"Melhor Indivíduo Final: {melhor_solucao}")
    # O fitness máximo é n*(n-1)/2. Se o melhor fitness for igual a isso, conflitos = 0.
    fitness_maximo = (n * (n - 1)) // 2
    conflitos_finais = fitness_maximo - historico[-1]
    print(f"Número de Conflitos: {conflitos_finais}")
    
    if conflitos_finais == 0:
        print("Sucesso! Solução ótima encontrada.")
    else:
        print("O algoritmo parou em um ótimo local ou precisa de mais gerações.")

if __name__ == "__main__":
    testar_n_rainhas()