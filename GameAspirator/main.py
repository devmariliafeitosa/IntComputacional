from aspirator_bfs import busca_aspirador_bfs

# ====================================================================
# PASSO 4: EXECUÇÃO E ANÁLISE DA SOLUÇÃO
# ====================================================================

def rodar_simulacao():

    ESTADO_INICIAL = ('A', 'S', 'S')  

    print("--- 🤖 Jogo do Aspirador: Execução da Busca em Largura (BFS) ---")
    print(f"Estado Inicial: **{ESTADO_INICIAL}** (Aspirador em {ESTADO_INICIAL[0]}, A: {ESTADO_INICIAL[1]}, B: {ESTADO_INICIAL[2]})")
    
    # Chama a função de busca implementada no outro arquivo
    solucao_acoes = busca_aspirador_bfs(ESTADO_INICIAL)

    if isinstance(solucao_acoes, list):
        
        print("\n✅ [Resultado Ótimo Encontrado (BFS)]")
        print(f"Número **mínimo** de ações: **{len(solucao_acoes)}**")
        print("Sequência de Ações:")
      
        for i, acao in enumerate(solucao_acoes):
            print(f"{i+1}. **{acao}**")
            
        print("\n--- Análise Passo a Passo ---")
        simular_caminho(ESTADO_INICIAL, solucao_acoes)
            
    else:
        print("\n❌ Falha: Solução não encontrada.")


def simular_caminho(estado_inicial, caminho_acoes):
    
    from aspirator_bfs import aplicar_acao, teste_objetivo
    
    estado_atual = estado_inicial
    print(f"Início: {estado_atual}")
    
    for i, acao in enumerate(caminho_acoes):
        
        proximo_estado = aplicar_acao(estado_atual, acao)
        
        
        if proximo_estado:
             print(f"Passo {i+1}: Ação **{acao}** -> Novo Estado: **{proximo_estado}**")
             estado_atual = proximo_estado
        else:
            
            print(f"Passo {i+1}: Ação **{acao}** -> Estado inalterado: **{estado_atual}**")

    print(f"\nEstado Final: **{estado_atual}**. Objetivo alcançado? **{teste_objetivo(estado_atual)}**")


if __name__ == '__main__':
    rodar_simulacao()