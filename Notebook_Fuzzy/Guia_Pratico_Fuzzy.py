#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


def triangular(x, parametros):
    a, b, c = parametros
    return max(min(((x-a)/(b-a)), ((c-x)/(c-b))), 0)

def gaussiana(x, parametros):
    media, dp = parametros
    return np.exp((-(x-media) **2)/(2*dp**2))


# In[ ]:


def formatar_regras(regras, X, Y):
    for precedente, consequentes in regras.items():
        if len(X) == 1:
            precedente_str = f"SE {X[0]} = {precedente[0]}"
        else:
            precedente_parts = [f"{X[i]} = {precedente[i]}" for i in range(len(X))]
            precedente_str = "SE " + " E ".join(precedente_parts)

        consequente_parts = []
        consequentes_ordenados = sorted(consequentes.items(), key=lambda item: item[1], reverse=True)

        for nome, peso in consequentes_ordenados:
            peso_formatado = f"{nome}({peso:.2f})"
            consequente_parts.append(peso_formatado)

        consequente_str = f" ENTÃO {Y} = " + " + ".join(consequente_parts)
        print(precedente_str + consequente_str)


# In[ ]:


class ConjuntoFuzzy(object):
    def __init__(self, nome, funcao, parametros, ponto_medio):
        self.nome = nome
        self.funcao = funcao
        self.parametros = parametros
        self.ponto_medio = ponto_medio

    def pertinencia(self, x):
        return self.funcao(x, self.parametros)

    def plot(self, eixo, intervalo):
        eixo.plot(intervalo, [self.pertinencia(k) for k in intervalo])

    def __str__(self):
        return "{}({})".format(self.nome, self.parametros)

def plot_conjuntos(eixo, conjuntos, intervalo):
    ticks = []
    ticks_names = []
    for nome, conj in conjuntos.items():
        conj.plot(eixo, intervalo)
        ticks.append(conj.ponto_medio)
        ticks_names.append(str(round(conj.ponto_medio, 2)) + "" + nome)

    eixo.set_xticks(ticks)
    eixo.set_xticklabels(ticks_names)


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = [k for k in np.arange(-3 * np.pi, 3 * np.pi, 0.2)]
y = [k**2 * np.exp(np.sin(k)) for k in x]

df = pd.DataFrame({'x': x, 'y': y})
print(df)

plt.plot(x, y)
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


# In[ ]:


conjuntos = {
    'x': {
        'Esquerda': ConjuntoFuzzy("Esquerda", triangular, [-10, -5, 0], -5),
        'Centro': ConjuntoFuzzy("Centro", triangular, [-5, 0, 5 ], 0),
        'Direita': ConjuntoFuzzy("Direita", triangular, [0, 5, 10], 5),
    },
    'y': {
        'Alto': ConjuntoFuzzy("Alto", gaussiana, [175,2], 175),
        'Médio': ConjuntoFuzzy("Médio", gaussiana, [100, 2], 100),
        'Baixo': ConjuntoFuzzy("Baixo", gaussiana, [0, 2], 0),
    }
}

fix, eixo = plt.subplots(2)
plot_conjuntos(eixo[0], conjuntos['x'], [k for k in np.linspace(-10,10,100)])
plot_conjuntos(eixo[1], conjuntos['y'], [k for k in np.linspace(0, 175, 100)])

plt.tight_layout()


# In[ ]:


from itertools import product

def inducao(dados, X, Y, conjuntos):
    dados_fuzzificados = []
    for indice in dados.index:
        linha = dados.loc[indice]
        linha_fuzzy = {}
        for variavel in conjuntos.keys():
            linha_fuzzy[variavel] = []
            for nome, conj in conjuntos[variavel].items():
                if conj.pertinencia(linha[variavel]) > 0:
                    linha_fuzzy[variavel].append(nome)
        dados_fuzzificados.append(linha_fuzzy)

    regras = {}
    for linha in dados_fuzzificados:
        x = [linha[k] for k in X]
        y = linha[Y]
        for precedente in product(*x):
            for consequente in y:
                if precedente not in regras:
                    regras[precedente] = {consequente: 1}
                else:
                    if consequente not in regras[precedente]:
                        regras[precedente][consequente] = 1
                    else:
                        regras[precedente][consequente] += 1

    for precedente in regras.keys():
        total = np.sum([regras[precedente][k] for k in regras[precedente].keys()])
        for k in regras[precedente].keys():
            regras[precedente][k] = regras[precedente][k] / total

    return regras


# In[ ]:


def inferencia_regressao(dado, X, Y, conjuntos, regras):
    xfuzzy = {}
    for variavel in X:
        xfuzzy[variavel] = {}
        for nome, conj in conjuntos[variavel].items():
            pert = conj.pertinencia(dado[variavel])
            if pert > 0:
                xfuzzy[variavel][nome] = pert

    regras_ativadas = {}
    conj = []
    for variavel in X:
        conj.append([k for k in xfuzzy[variavel].keys()])

    for precedente in product(*conj):
        if precedente in regras:
            consequente = 0
            regras_ativadas[precedente] = {}
            for yfuzzy in regras[precedente].keys():
                consequente += conjuntos[Y][yfuzzy].ponto_medio * regras[precedente][yfuzzy]
            regras_ativadas[precedente]['centro'] = consequente

            ativacao = []
            for contador, conjunto in enumerate(precedente):
                ativacao.append(xfuzzy[X[contador]][conjunto])
            regras_ativadas[precedente]['ativacao'] = np.min(ativacao)

    denominador = 0
    numerador = 0
    for regra in regras_ativadas.keys():
        denominador += regras_ativadas[regra]['ativacao']
        numerador += regras_ativadas[regra]['ativacao'] * regras_ativadas[regra]['centro']

    return numerador / denominador


# In[ ]:


regras = inducao(df, ['x'], 'y', conjuntos)
formatar_regras(regras, ['x'], 'y')

prever = lambda i: inferencia_regressao(df.iloc[i], ['x'], 'y', conjuntos, regras)
yy = [prever(k) for k in range(len(df.index))]

plt.plot(x,y)
plt.plot(x,yy)


# In[ ]:


# Dicionário que define os conjuntos fuzzy para as variáveis 'x' e 'y'.
conjuntos = {
    # Variável 'x' (Função Triangular, Domínio: -10 a 10)
    'x': {
        # Esquerda Extrema: [a, m, b] = [-10, -7.5, -5]
        'EsquerdaExt': ConjuntoFuzzy("EsquerdaExt", triangular, [-10, -7.5, -5], -7.5),
        # Esquerda
        'Esquerda': ConjuntoFuzzy("Esquerda", triangular, [-7.5, -5.0, -2.5], -5.0),
        # Esquerda Central
        'EsquerdaCent': ConjuntoFuzzy("EsquerdaCent", triangular, [-5.0, -2.5, 0], -2.5),
        # Centro
        'Centro': ConjuntoFuzzy("Centro", triangular, [-2.5, 0, 2.5], 0.0),
        # Direita Central
        'DireitaCent': ConjuntoFuzzy("DireitaCent", triangular, [0, 2.5, 5], 2.5),
        # Direita
        'Direita': ConjuntoFuzzy("Direita", triangular, [2.5, 5.0, 7.5], 5.0),
        # Direita Extrema
        'DireitaExt': ConjuntoFuzzy("DireitaExt", triangular, [5.0, 7.5, 10.0], 7.5)
    },

    # Variável 'y' (Função Gaussiana, Domínio: 0 a 175)
    'y': {
        # Alto: [Pico, Desvio Padrão (sigma)] = [175, 1]
        'Alto': ConjuntoFuzzy("Alto", gaussiana, [175, 1], 175),
        # Médio Alto
        'AltoMed': ConjuntoFuzzy("AltoMed", gaussiana, [135, 1], 135),
        # Médio
        'Medio': ConjuntoFuzzy("Medio", gaussiana, [100, 1], 100),
        # Médio Baixo
        'BaixoMed': ConjuntoFuzzy("BaixoMed", gaussiana, [50, 1], 50),
        # Baixo
        'Baixo': ConjuntoFuzzy("Baixo", gaussiana, [0, 1], 0),
    }
}

# Configura a figura com 2 gráficos (subplots) verticais.
fig, eixo = plt.subplots(2, figsize=[10,3])

# Plota os conjuntos de 'x' (-10 a 10) no primeiro eixo.
plot_conjuntos(eixo[0], conjuntos['x'], [k for k in np.linspace(-10,10,100)])

# Plota os conjuntos de 'y' (0 a 175) no segundo eixo.
plot_conjuntos(eixo[1], conjuntos['y'], [k for k in np.linspace(0, 175, 100)])

# Ajusta o layout para evitar sobreposições.
plt.tight_layout()


# In[ ]:


regras = inducao(df, ['x'], 'y', conjuntos)

formatar_regras(regras, ['x'], 'y')

prever = lambda i: inferencia_regressao(df.iloc[i], ['x'], 'y', conjuntos, regras)

yy = [prever(k) for k in range(len(df.index))]

plt.plot(x,y)
plt.plot(x,yy)


# In[ ]:


dp = 0.05
conjuntos = {
    'x': {
        'EsquerdaExt': ConjuntoFuzzy("EsquerdaExt", gaussiana, [-7.5, dp], -10),
        'Esquerda': ConjuntoFuzzy("Esquerda", gaussiana, [-5.0, dp], -5.0),
        'EsquerdaCent': ConjuntoFuzzy("EsquerdaCent", gaussiana, [-2.5, dp], -2.5),
        'Centro': ConjuntoFuzzy("Centro", gaussiana, [0, dp], 0.0),
        'DireitaCent': ConjuntoFuzzy("DireitaCent", gaussiana, [2.5, dp], 2.5),
        'Direita': ConjuntoFuzzy("Direita", gaussiana, [5.0, dp], 5.0),
        'DireitaExt': ConjuntoFuzzy("DireitaExt", gaussiana, [7.5, dp], 7.5)
    },
    'y': {
        'Alto': ConjuntoFuzzy("Alto", gaussiana, [175, 1], 175),
        'AltoMed': ConjuntoFuzzy("AltoMed", gaussiana, [135, 1], 135),
        'Medio': ConjuntoFuzzy("Medio", gaussiana, [100, 1], 100),
        'BaixoMed': ConjuntoFuzzy("BaixoMed", gaussiana, [50, 1], 50),
        'Baixo': ConjuntoFuzzy("Baixo", gaussiana, [0, 1], 0),
    }
}

fig, eixo = plt.subplots(2, figsize=[10,3])

plot_conjuntos(eixo[0], conjuntos['x'], [k for k in np.linspace(-10,10,100)])
plot_conjuntos(eixo[1], conjuntos['y'], [k for k in np.linspace(0, 175, 100)])

plt.tight_layout()


# In[ ]:


regras = inducao(df, ['x'], 'y', conjuntos)

formatar_regras(regras, ['x'], 'y')

prever = lambda i: inferencia_regressao(df.iloc[i], ['x'], 'y', conjuntos, regras)

yy = [prever(k) for k in range(len(df.index))]

plt.plot(x,y)
plt.plot(x,yy)


# In[ ]:


_x = [k for k in np.linspace(np.min(x)*1.1, np.max(x)*1.1, 15)]
_y = [k for k in np.linspace(np.min(y)*1.1, np.max(y)*1.1, 7)]

conjuntos = {
    'x': {"x"+str(k) : ConjuntoFuzzy("x"+str(k), gaussiana, [_x[k], 0.05], _x[k]) for k in range(15) },
    'y': {"y"+str(k) : ConjuntoFuzzy("y"+str(k), gaussiana, [_y[k], 0.1], _y[k]) for k in range(7) }
}

fig, ax = plt.subplots(2, figsize=[10,3])

plot_conjuntos(ax[0], conjuntos['x'], [k for k in np.linspace(-10, 10, 100)])
plot_conjuntos(ax[1], conjuntos['y'], [k for k in np.linspace(0, 175, 100)])

plt.tight_layout()


# In[ ]:


regras = inducao(df, ['x'], 'y', conjuntos)
# regras
formatar_regras(regras, ['x'], 'y')
prever = lambda i: inferencia_regressao(df.iloc[i], ['x'], 'y', conjuntos, regras)

yy = [prever(k) for k in range(len(df.index))]

plt.plot(x,y)
plt.plot(x,yy)


# In[ ]:


conjX = 25
conjY = 10

_x = [k for k in np.linspace(np.min(x)*1.1, np.max(x)*1.1, conjX)]
_y = [k for k in np.linspace(np.min(y)*1.1, np.max(y)*1.1, conjY)]

conjuntos = {
    'x': {"x"+str(k) : ConjuntoFuzzy("x"+str(k), gaussiana, [_x[k], 0.05], _x[k]) for k in range(conjX) },
    'y': {"y"+str(k) : ConjuntoFuzzy("y"+str(k), gaussiana, [_y[k], 0.1], _y[k]) for k in range(conjY) }
}

fig, ax = plt.subplots(2, figsize=[10,3])

plot_conjuntos(ax[0], conjuntos['x'], [k for k in np.linspace(-10, 10, 100)])
plot_conjuntos(ax[1], conjuntos['y'], [k for k in np.linspace(0, 175, 100)])

plt.tight_layout()


# In[ ]:


regras = inducao(df, ['x'], 'y', conjuntos)
# regras
formatar_regras(regras, ['x'], 'y')
prever = lambda i: inferencia_regressao(df.iloc[i], ['x'], 'y', conjuntos, regras)

yy = [prever(k) for k in range(len(df.index))]

plt.plot(x,y)
plt.plot(x,yy)


# In[ ]:


x1 = [k for k in np.linspace(-3*np.pi, 3*np.pi, 120)]
x2 = [k for k in np.linspace(-2, 2, 120)]

y = [np.sin(x1[i]) * np.exp(x2[i]) for i in range(0, 120)]
df = pd.DataFrame({'x1': x1, 'x2': x2, 'y': y})

df


# In[ ]:


plt.plot(x2, y)
plt.xlabel("x2")
plt.ylabel("y")


# In[ ]:


_x1 = [k for k in np.linspace(min(x1)*1.2, max(x1)*1.2, 15)]
_x2 = [k for k in np.linspace(min(x2)*1.2, max(x2)*1.2, 15)]
_y = [k for k in np.linspace(min(y)*1.2, max(y)*1.2, 10)]

conjuntos = {
    'x1': {'x1' + str(k) : ConjuntoFuzzy('x1' + str(k), triangular, [_x1[k-1], _x1[k], _x1[k+1]], _x1[k]) for k in range(1, 14)},
    'x2': {'x2' + str(k) : ConjuntoFuzzy('x2' + str(k), triangular, [_x2[k-1], _x2[k], _x2[k+1]], _x2[k]) for k in range(1, 14)},
    'y': {'y' + str(k) : ConjuntoFuzzy('y' + str(k), triangular, [_y[k-1], _y[k], _y[k+1]], _y[k]) for k in range(1, 9)}
}

fig, ax = plt.subplots(3, figsize=[10, 5])

plot_conjuntos(ax[0], conjuntos['x1'], _x1)
plot_conjuntos(ax[1], conjuntos['x2'], _x2)
plot_conjuntos(ax[2], conjuntos['y'], _y)

plt.tight_layout()


# In[ ]:


regras = inducao(df, ['x1', 'x2'], 'y', conjuntos)
formatar_regras(regras, ['x1', 'x2'], 'y')

gerar = lambda i: inferencia_regressao(df.iloc[i], ['x1', 'x2'], 'y', conjuntos, regras)

yy = [gerar(k) for k in range(len(df.index))]

plt.plot(df['x1'].values, df['y'].values)
plt.plot(df['x1'].values, yy)


# In[ ]:


conjuntos = {
    'x1': {'x1' + str(k) : ConjuntoFuzzy('x1' + str(k), gaussiana, [_x1[k], 0.03], _x1[k]) for k in range(1, 14) },
    'x2': {'x2' + str(k) : ConjuntoFuzzy('x2' + str(k), gaussiana, [_x2[k], 0.01], _x2[k]) for k in range(1, 14) },
    'y': {'y' + str(k) : ConjuntoFuzzy('y' + str(k), gaussiana, [_y[k], 0.01], _y[k]) for k in range(1, 9) }
}

fig, ax = plt.subplots(3, figsize=[10, 5])

plot_conjuntos(ax[0], conjuntos['x1'], _x1)
plot_conjuntos(ax[1], conjuntos['x2'], _x2)
plot_conjuntos(ax[2], conjuntos['y'], _y)

plt.tight_layout()


# In[ ]:


regras = inducao(df, ['x1', 'x2'], 'y', conjuntos)
formatar_regras(regras, ['x1', 'x2'], 'y')

gerar = lambda i: inferencia_regressao(df.iloc[i], ['x1', 'x2'], 'y', conjuntos, regras)

yy = [gerar(k) for k in range(len(df.index))]

plt.plot(df['x1'].values, df['y'].values)
plt.plot(df['x1'].values, yy)

