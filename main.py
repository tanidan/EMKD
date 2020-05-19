import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import math
import random
from tkinter import *


def RandomVertexGenerating(count):
    f = open('inputVertex.txt', 'w')
    f.write(str(count) + '\n')

    for i in range(count):
        f.write(str(random.randint(1, 100)) + " " + str(random.randint(1, 100)) + '\n')

    f.close()


def ReadVertex():
    f = open('inputVertex.txt')
    n = int(f.readline())
    listOfVertex = []
    for i in range(n):
        vertexCoords = list(map(int, (f.readline().split())))
        listOfVertex.append((vertexCoords[0], vertexCoords[1]))
    return listOfVertex


def CreateDistanceMatrix():
    listOfVertex = ReadVertex()
    distMatrix = []
    for i in range(len(listOfVertex)):
        tempMatrixLine = []
        for j in range(len(listOfVertex)):
            distance = math.sqrt((listOfVertex[j][0]-listOfVertex[i][0])**2 + (listOfVertex[j][1]-listOfVertex[i][1])**2)
            tempMatrixLine.append(round(distance,2))
        distMatrix.append(tempMatrixLine)
    return distMatrix


def CreateGraphWithVertexPositioning():
    G = nx.Graph()
    listOfVertex = ReadVertex()
    distMatrix = CreateDistanceMatrix()
    for i in range(len(listOfVertex)):
        G.add_node(i, pos=(listOfVertex[i][0], listOfVertex[i][1]))

    for i in range(len(distMatrix)):
        for j in range(len(distMatrix))[i:]:
            if distMatrix[i][j] > 0:
                G.add_edge(i, j, length=distMatrix[i][j])
    return G


def minDistance(dist, mstSet, V):
    min = sys.maxsize
    for v in range(V):
        if mstSet[v] is False and dist[v] < min:
            min = dist[v]
            min_index = v
    return min_index


def prims(G):
    V = len(G.nodes())  # V - кількість вершин
    dist = []  # dist[i] містить мінімальне значення довжини ребра вершини i для включення у МКД
    parent = [None] * V  # parent[i] містить вершину, що поєднана з і ребром МКД
    mstSet = []  # mstSet[i] true якщо вершина включена у МКД
    # для кожної вершини, dist[] ініціалізується максимальним значенням та mstSet[] - False
    for i in range(V):
        dist.append(sys.maxsize)
        mstSet.append(False)
    dist[0] = 0
    parent[0] = -1  # початкова вершина є коренем і не має батьківської
    for count in range(V - 1):
        u = minDistance(dist, mstSet, V)  # обирається вершина на мінімальній відстані
        mstSet[u] = True
        # оновлення даних про вершини, що суміжні з поточною
        for v in range(V):
            if (u, v) in G.edges():
                if mstSet[v] == False and G[u][v]['length'] < dist[v]:
                    dist[v] = G[u][v]['length']
                    parent[v] = u

    outputG = nx.Graph()
    listOfVertex = ReadVertex()
    distMatrix = CreateDistanceMatrix()
    for i in range(len(listOfVertex)):
        outputG.add_node(i, pos=(listOfVertex[i][0], listOfVertex[i][1]))
    for X in range(V):
        if parent[X] != -1:
            if (parent[X], X) in G.edges():
                outputG.add_edge(parent[X], X, length=distMatrix[parent[X]][X])
    return outputG


def DrawGraph(G):
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, font_size=6)  # with_labels=true is to show the node number in the output graph
    edge_labels = nx.get_edge_attributes(G, 'length')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)  # prints weight on all the edges
    return pos


def mainStaff(count):
    RandomVertexGenerating(count)
    CreateDistanceMatrix()
    G = CreateGraphWithVertexPositioning()
    outputG = prims(G)
    DrawGraph(outputG)
    plt.show()


root = Tk()
root.title('Побудова ЕМКД')
root.geometry('300x100')
canvas = Canvas(root, width=300, height=100)
label = Label(root, text='Введіть кількість точок:')
label.place(x=10, y=10)
entry = Entry(root)
entry.place(x=12, y=30)
btn_show = Button(root, text='Сгенерувати')
btn_show.bind('<Button-1>', lambda event: mainStaff(int(entry.get())))
btn_show.place(x=12, y=55)
canvas.pack()
root.mainloop()
