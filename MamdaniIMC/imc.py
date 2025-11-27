import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import warnings
import pandas as pd 

warnings.filterwarnings("ignore")

peso = ctrl.Antecedent(np.arange(40, 151, 1), 'peso')
altura = ctrl.Antecedent(np.arange(1.5, 2.01, 0.01), 'altura')
imc = ctrl.Consequent(np.arange(15, 46, 1), 'imc', defuzzify_method='centroid')


peso['leve']  = fuzz.trapmf(peso.universe,  [40, 40, 60, 75])
peso['medio'] = fuzz.trimf(peso.universe,  [70, 85, 100])
peso['alto']  = fuzz.trapmf(peso.universe,  [95, 110, 150, 150])

altura['baixa'] = fuzz.trapmf(altura.universe, [1.5, 1.5, 1.6, 1.7])
altura['media'] = fuzz.trimf(altura.universe,  [1.65, 1.75, 1.85])
altura['alta']  = fuzz.trapmf(altura.universe, [1.8, 1.9, 2.0, 2.0])

imc['muito_magro']    = fuzz.trimf(imc.universe, [15, 16, 18.5]) # < 18.5
imc['saudavel']       = fuzz.trimf(imc.universe, [18.5, 22, 25]) # 18.5 - 24.9
imc['sobrepeso']      = fuzz.trimf(imc.universe, [25, 27.5, 30]) # 25.0 - 29.9
imc['obesidade_I']    = fuzz.trimf(imc.universe, [30, 32.5, 35]) # 30.0 - 34.9
imc['obesidade_II']   = fuzz.trimf(imc.universe, [35, 37.5, 40]) # 35.0 - 39.9
imc['obesidade_III']  = fuzz.trapmf(imc.universe, [40, 42, 45, 45]) # >= 40.0


# Peso LEVE
regra1 = ctrl.Rule(peso['leve']  & altura['baixa'], imc['muito_magro'])
regra2 = ctrl.Rule(peso['leve']  & altura['media'], imc['muito_magro'])
regra3 = ctrl.Rule(peso['leve']  & altura['alta'],  imc['muito_magro'])

# Peso MEDIO
regra4 = ctrl.Rule(peso['medio'] & altura['baixa'], imc['saudavel'])
regra5 = ctrl.Rule(peso['medio'] & altura['media'], imc['saudavel'])
regra6 = ctrl.Rule(peso['medio'] & altura['alta'],  imc['saudavel'])

# Peso ALTO
regra7 = ctrl.Rule(peso['alto'] & altura['baixa'], imc['obesidade_II']) # Peso Alto/Baixa -> Obesidade Alta
regra8 = ctrl.Rule(peso['alto'] & altura['media'], imc['obesidade_I'])  # Peso Alto/Media -> Obesidade I
regra9 = ctrl.Rule(peso['alto'] & altura['alta'],  imc['sobrepeso'])    # Peso Alto/Alta -> Sobrepeso/Obesidade I

regra10 = ctrl.Rule(peso['medio'] & altura['baixa'], imc['sobrepeso'])  
regra11 = ctrl.Rule(peso['alto']  & altura['baixa'], imc['obesidade_III']) 
regra12 = ctrl.Rule(peso['alto']  & altura['alta'],  imc['obesidade_I']) 

regras = [
    regra1, regra2, regra3,
    regra4, regra5, regra6,
    regra7, regra8, regra9,
    regra10, regra11, regra12 
]

sistema_controle = ctrl.ControlSystem(regras)
simulador_imc = ctrl.ControlSystemSimulation(sistema_controle)

NUM_PONTOS = 100

np.random.seed(42) 
dataset_peso   = np.clip(np.random.normal(80, 15, NUM_PONTOS), 40, 150)
dataset_altura = np.clip(np.random.normal(1.75, 0.1, NUM_PONTOS), 1.5, 2.0)

dataset_imc_classico = dataset_peso / (dataset_altura ** 2)

dataset_imc_fuzzy = []

for p, a in zip(dataset_peso, dataset_altura):
    try:
        simulador_imc.input['peso'] = p
        simulador_imc.input['altura'] = a
        simulador_imc.compute()
        dataset_imc_fuzzy.append(simulador_imc.output['imc'])
    except:
        dataset_imc_fuzzy.append(np.nan)

dataset_imc_fuzzy = np.array(dataset_imc_fuzzy)

valid = ~np.isnan(dataset_imc_fuzzy)
imc_classico_valid = dataset_imc_classico[valid]
imc_fuzzy_valid    = dataset_imc_fuzzy[valid]

correlacao = np.corrcoef(imc_classico_valid, imc_fuzzy_valid)[0, 1]
print(f"📊 Correlação entre IMC Clássico e Fuzzy: {correlacao:.4f}")

erro_absoluto = np.abs(imc_classico_valid - imc_fuzzy_valid)
print(f"Erro absoluto médio: {erro_absoluto.mean():.4f}")
print(f"Erro absoluto máximo: {erro_absoluto.max():.4f}")
print(f"Erro absoluto mínimo: {erro_absoluto.min():.4f}")

plt.figure(figsize=(8, 6))
plt.scatter(imc_classico_valid, imc_fuzzy_valid, label='Pontos Simulados')
plt.plot([15, 45], [15, 45], 'r--', label='Linha de Igualdade (y=x)')
plt.xlabel("IMC Clássico")
plt.ylabel("IMC Fuzzy (Saída)")
plt.title("Comparação entre IMC Clássico e IMC Fuzzy")
plt.legend()
plt.grid(True)
plt.show()

def testar(peso_val, altura_val):
    simulador_imc.input['peso'] = peso_val
    simulador_imc.input['altura'] = altura_val
    try:
        simulador_imc.compute()
    except ValueError:
        print(f"Erro de cálculo para Peso={peso_val}kg, Altura={altura_val}m. Verifique os inputs.")
        return

    imc_class = peso_val / (altura_val ** 2)
    imc_fuzzy = simulador_imc.output['imc']

    print(f"\n--- Resultado da Simulação ---")
    print(f"Peso={peso_val}kg | Altura={altura_val}m")
    print(f"IMC clássico: {imc_class:.2f}")
    print(f"IMC fuzzy:    {imc_fuzzy:.2f}")

    imc.view(sim=simulador_imc)
    plt.show()


# --- 9. Exemplos de Teste ---

testar(65, 1.75)  # Ex: Saudável Clássico (21.22)
testar(105, 1.70) # Ex: Obesidade I Clássico (36.33)
testar(81, 1.73)  # Ex: Sobrepeso Clássico (27.06)
testar(130, 1.65) # Ex: Obesidade III Clássico (47.78 - fora da faixa do universo IMC, mas o fuzzy se aproxima do máximo)