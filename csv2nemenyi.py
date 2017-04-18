#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Generador de gráfico Nemenyi a partir de fichero CSV
"""

import numpy
import Orange
import matplotlib.pyplot as plt



def leer_nombre_csv(msg):
    """ Sirve para leer el nombre del fichero CSV """
    nombre = input(msg)
    partes = nombre.strip().split('.')
    if len(partes) < 2 or partes[-1].lower() != 'csv':
        nombre += '.csv'
    return nombre

def calcular_ranking_medio(matriz):
    """ Calcula el ranking medio de cada sistema """
    matrix = 100 - numpy.matrix(matriz)
    index_matrix = numpy.argsort(matrix)
    (rows, cols) = index_matrix.shape
    ranking = numpy.array([0.0]*cols)

    for row in range(rows):
        c1 = 0
        while c1 < cols:
            c2 = c1 + 1
            while c2 < cols and matrix[row, index_matrix[row, c1]] == matrix[row, index_matrix[row, c2]]:
                # print("fila %d: encontré empate entre %d y %d" % (row,c1,c2))
                c2 += 1

            # ties = c2-c1
            ranking_value = (c1+c2-1)/2.0
            for col in range(c1, c2):
                ranking[index_matrix[row, col]] += ranking_value + 1
                # print(ranking[index_matrix[row, col]], end=' ')
            c1 = c2

        # print(' -> ', ranking)

    return ranking/rows



# Main

print('Selecciona el alpha value para todos los test:')
print('a) 0.1\nb) 0.05 (defecto)')
alpha_value = input('cual? ').lower()
while alpha_value != 'a' and alpha_value != 'b' and alpha_value != '':
    alpha_value = input('Opción incorrecta!! Prueba otra vez: ').lower()

if alpha_value == 'a':
    alpha_value = '0.1'
else:
    alpha_value = '0.05'

print('Usando alpha='+alpha_value+' para todos los tests.')

nombre_fichero = leer_nombre_csv('Nombre del CSV (quit para salir):')

while nombre_fichero.lower() != 'quit.csv':

    fichero_csv = open(nombre_fichero, 'r')

    sistemas = []
    conjuntos = []
    matriz_raw = []

    l = fichero_csv.readline()
    linea = l.strip().split(',')
    sistemas = linea[1:]
    for l in fichero_csv:
        linea = l.strip().split(',')
        conjunto = linea[0]
        conjuntos.append(conjunto)
        vector_fila = []
        for c in range(1, len(linea)):
            vector_fila.append(float(linea[c]))
        matriz_raw.append(vector_fila)

    print('Hay %d sistemas:' % len(sistemas))
    for s in sistemas:
        print('\t'+s)

    num_conjuntos = len(conjuntos)
    print('Hay %d conjuntos:' % num_conjuntos)
    #for c in conjuntos:
    #    print('\t'+c)

    ranking_medio = calcular_ranking_medio(matriz_raw)
    print('Ranking medio:')
    i = 0
    for s in sistemas:
        print(s+': '+str(ranking_medio[i]))
        i = i+1

    # Drawing
    cd = Orange.evaluation.compute_CD(ranking_medio,
                                      num_conjuntos,
                                      alpha=alpha_value, test='nemenyi')
    Orange.evaluation.graph_ranks(ranking_medio, sistemas,
                                  cd=cd, width=6, textspace=1.5)

    plt.show()

    nombre_fichero = leer_nombre_csv('Nombre del CSV (quit para salir):')

print('Que tengas un buen día!!')
