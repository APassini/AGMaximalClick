#PROBLEMA DO MAXCLIQUE É DADO POR UM VETOR G = (V, E), EM QUE "V" É UM VETOR CONTENDO OS VÉRTICES
#E "E" É UM VETOR DE ARESTAS.
#UMA SOLUÇÃO FACTÍVEL DO PROBLEMA É UM V' EM QUE "i" E "j" EXISTAM EM V' E (i,j) SEJA UMA ARESTA
#A FUNÇÃO OBJETIVO DO PROBLEMA É O TAMANHO DE V' E UMA SOLUÇÃO ÓTIMA É UM CLIQUE V' QUE MAXIMIZE |V'|.

#NOSSO ALGORITMO SERÁ CARACTERIZADO POR POSSUIR UMA MUTAÇÃO CLÁSSICA E CROSSOVER EM UM PONTO
#POSSUIRÁ TAMBÉM UMA POPULAÇÃO CONSTANTE E UMA SELEÇÃO DE ROLETA.


#CROMOSSOMO É UM VETOR BINÁRIO POSSUINDO 0 E 1, EM QUE 1 INDICA A PRESENÇA NO SUBGRAFO E 0 A AUSÊNCIA NO SUBGRAFO
#EXEMPLO VETOR=[1,0,1,0,0] QUER DIZER QUE OS VÉRTICES "1" E "3" ESTÃO NO SUBGRAFO.

#A FUNÇÃO DE FITNESS É DADA PARA UM CERTO CROMOSSOMO X, X[i]*X[j] SE EXISTE UMA ARESTA (i,j)
#CASO NÃO EXISTA ESSA ARESTA, O CROMOSSOMO SERÁ PENALIZADO N VEZES A SOMA DO PRODUTO X[i]*X[j]

#OU SEJA F(X) = SUM(X[i]*X[j]) PARA CASO "i" E "j" EXISTAM NAS ARESTAS
#E F(X) = SUM(X[i]*X[j]) - N * SUM(X[i]*X[j])

import numpy as np
import random

vertices = []
arestas = []

numRepeticoes = 200
numPopulacao = 100
nPunitive = 5

def takeSecond(elem):
    return elem[1]

def ler_arquivo():
    global vertices
    global arestas
    f = open('Figura_1.txt', 'r')
    for linha in f:
        if linha.count(';') > 0:
            s = linha.split(';')
            for tupla in s:
                t = tupla.split(',')
                tint = [int(t[0]), int(t[1])]
                arestas.append(tint)
        else:
            v = linha.split(',')
            for item in v:
                vertices.append(int(item))

def exist_edge(verticeUm, verticeDois):
    return [verticeUm, verticeDois] in arestas

def crossover(individuoUm, individuoDois):
    crossoverPoint = random.randint(0,len(vertices) - 1)
    filhoUm = np.append(individuoUm[:crossoverPoint], individuoDois[crossoverPoint:])
    filhoDois = np.append(individuoDois[:crossoverPoint], individuoUm[crossoverPoint:])
    return filhoUm, filhoDois

def mutacao(individuo):
    if random.choice([True, False]):
        randomNumber = random.randint(0,len(individuo)-1)
        if individuo[randomNumber] == 1:
            individuo[randomNumber] = 0
        else:
            individuo[randomNumber] = 1
    return individuo
        

def calcula_fitness(individuo):
    fitness = 0
    for x in range(len(individuo)):
        if individuo[x] == 1:
            for y in range(x+1, len(individuo)):
                if individuo[y] == 1:
                    if exist_edge(x, y):
                        fitness = fitness + individuo[x] * individuo[y]
                    else:
                        fitness = fitness - nPunitive * individuo[x] * individuo[y]
    return fitness


def cria_populacao(numVertices, numIndividuos):
    populacao = []
    for i in range(numIndividuos):
        cromossomo = np.random.choice([0, 1], size=numVertices, p=[.5, .5])
        populacao.append(cromossomo)
    return populacao

def main():
    ler_arquivo()
    populacao = cria_populacao(len(vertices),numPopulacao)
    for i in range(numRepeticoes):
        populacaoWithFitness = []
        for individuo in populacao:
            fitness = calcula_fitness(individuo)
            populacaoWithFitness.append((individuo, fitness))
        populacaoWithFitness.sort(key=takeSecond, reverse=True)
        populacaoWithFitness = populacaoWithFitness[:len(populacaoWithFitness)//2]
        melhorIndividuo = populacaoWithFitness[0]
        populacao = []
        for individuo in populacaoWithFitness:
            individuoUm, individuoDois = crossover(individuo[0], populacaoWithFitness[random.randint(0,10)][0])
            populacao.append(individuoUm)
            populacao.append(individuoDois)
    for individuo in populacao:
        fitness = calcula_fitness(individuo)
        populacaoWithFitness.append((individuo, fitness))
    populacaoWithFitness.sort(key=takeSecond, reverse=True)
    populacaoWithFitness = populacaoWithFitness[:len(populacaoWithFitness)//2]
    melhorIndividuo = populacaoWithFitness[0]
    print(melhorIndividuo)
            

if __name__ == "__main__":
    main()