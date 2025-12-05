from problema.estado import State
from problema.aspirador_problema import VacuumProblem
from busca.bfs import bfs
from busca.dfs import dfs

if __name__ == "__main__":
    # Estado inicial: agente em A, A está sujo, B está sujo
    initial = State("A", {"A": True, "B": True})

    problem = VacuumProblem(initial)

    print("=== BFS ===")
    sol_bfs, node_bfs = bfs(problem)
    print("Solução:", sol_bfs)
    print("Estado final:", node_bfs.state)

    print("\n=== DFS ===")
    sol_dfs, node_dfs = dfs(problem)
    print("Solução:", sol_dfs)
    print("Estado final:", node_dfs.state)
