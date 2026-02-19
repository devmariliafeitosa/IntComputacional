# Redes Neurais Artificiais Clássicas

Este projeto foi desenvolvido para a disciplina de **Inteligência Computacional**. O objetivo é comparar o desempenho e as fronteiras de decisão de três modelos fundamentais de Redes Neurais Artificiais aplicados ao conjunto de dados Iris.

##  Modelos Implementados
* **Perceptron:** Classificador linear simples.
* **ADALINE:** Rede linear com treinamento via Gradiente Descendente (MSE).
* **MLP (Multilayer Perceptron):** Rede neural multicamadas capaz de aprender padrões não-lineares.

##  Estrutura do Projeto
```text
Projeto_Redes_Neurais_Iris/
├── cod/
│   └── experimento_modelos.ipynb  # Notebook com a lógica 
├── experimentos/
│   └── *.png                     # Gráficos de fronteiras e 
├── relatorio/
│   └── Relatótio de Experimentação Redes Neurais Artificiais Clássicas.pdf       # Documentação teórica e análise de resultados
└── README.md                     # Instruções do projeto
```

## Pré-Requisitos
Antes de rodar o projeto, você precisará ter o Python 3.x instalado e as seguintes bibliotecas:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

## Como Rodar

 Abra a pasta principal do projeto no VS Code.

1. Certifique-se de que a extensão Jupyter (da Microsoft) está instalada no seu VS Code.

2. Navegue até a pasta codigos/ e abra o arquivo experimento_modelos.ipynb.

3. Clique no botão Run All (ou Executar Tudo) no menu superior do notebook.

4. Os resultados estatísticos (Média e Desvio Padrão) aparecerão logo abaixo das células de código.

5. Os gráficos de fronteiras e matrizes de confusão serão salvos automaticamente na pasta experimentos/.

## Metodologia Experimental

Para garantir o rigor acadêmico exigido, o projeto segue:

- Padronização de Dados: Utilização de StandardScaler para normalizar os atributos.

- Validação Estatística: Mínimo de 10 execuções independentes com sementes aleatórias variadas para cada modelo.

- Divisão de Dados: 70% para treinamento e 30% para teste (Holdout).

- Métricas Obrigatórias: Acurácia média, desvio padrão e matriz de confusão agregada.

## Principais Resultados

Os experimentos demonstraram que:

- O Perceptron e o ADALINE apresentam fronteiras lineares, encontrando dificuldades na separação das classes Versicolor e Virginica.

- O MLP (Multilayer Perceptron) obteve a melhor performance (aprox. 94,44% de acurácia), devido à sua capacidade de gerar fronteiras de decisão não-lineares (curvas), adaptando-se melhor à sobreposição dos dados.