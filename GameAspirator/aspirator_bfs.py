from collections import deque


class Node:
  
    def __init__(self, estado, pai=None, acao=None):
        self.estado = estado    
        self.pai = pai          
        self.acao = acao        
        
    def caminho(self):
        caminho_acoes = []
        no_atual = self
        while no_atual.pai is not None:
            caminho_acoes.append(no_atual.acao)
            no_atual = no_atual.pai
        
        return caminho_acoes[::-1]


def aplicar_acao(estado_atual, acao):
    local, sala_a, sala_b = estado_atual
    novo_estado = None 

    if acao == 'Aspirar':
        if local == 'A':
            
            novo_estado = (local, 'L' if sala_a == 'S' else sala_a, sala_b)
        else: 
            novo_estado = (local, sala_a, 'L' if sala_b == 'S' else sala_b)
            
    elif acao == 'Mover_Direita':
        if local == 'A':
            novo_estado = ('B', sala_a, sala_b)
        
    elif acao == 'Mover_Esquerda':
        if local == 'B':
            novo_estado = ('A', sala_a, sala_b)
        
    return novo_estado if novo_estado and novo_estado != estado_atual else None


def teste_objetivo(estado):
    
    return estado[1] == 'L' and estado[2] == 'L'


def busca_aspirador_bfs(estado_inicial):

    ACOES = ['Aspirar', 'Mover_Direita', 'Mover_Esquerda']

    no_raiz = Node(estado_inicial)
    fronteira = deque([no_raiz])
    
    if teste_objetivo(estado_inicial):
        return []

    explorados = {estado_inicial}
    
    while fronteira:
        
        no_atual = fronteira.popleft() 
 
        for acao in ACOES:
            proximo_estado = aplicar_acao(no_atual.estado, acao)
            
      
            if proximo_estado and proximo_estado not in explorados:
                
                no_filho = Node(estado=proximo_estado, pai=no_atual, acao=acao)
                
                if teste_objetivo(no_filho.estado):
                    print(f"Objetivo alcançado no estado: {no_filho.estado}")
                    return no_filho.caminho()
              
                explorados.add(proximo_estado)
                fronteira.append(no_filho)
                
    return "Falha! Solução não encontrada."
