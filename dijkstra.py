
import graph
import math
import sys
import queue
import time  # borrar amb el main

# Dijkstra =====================================================================

def Dijkstra(g, start):
	no_visitats = set()
	for vertex in g.Vertices:
		if vertex == start:
			vertex.DijkstraDistance = 0.0
		else:
			vertex.DijkstraDistance = sys.float_info.max
		no_visitats.add(vertex)

	actual = start

	while no_visitats:
		for aresta in actual.Edges:
			if aresta.Destination in no_visitats:
				if (aresta.Length + actual.DijkstraDistance) < aresta.Destination.DijkstraDistance:
					# print(aresta.Length)
					aresta.Destination.DijkstraDistance = aresta.Length + actual.DijkstraDistance

		no_visitats.remove(actual)

		minim = sys.float_info.max

		for vertex in no_visitats:
			if vertex.DijkstraDistance <= minim:
				minim = vertex.DijkstraDistance
				actual = vertex

# DijkstraQueue ================================================================

def DijkstraQueue(g, start):
	visitats = {}
	kmeans = {}

	cua = queue.PriorityQueue()
	for node in g.Vertices:
		if node == start:
			node.DijkstraDistance = 0
		else:
			node.DijkstraDistance = sys.float_info.max
		visitats[node] = False
		kmeans[node] = None

	cua.put([start.DijkstraDistance, start])
	while not cua.empty():
		node_actual = cua.get()
		if not visitats[node_actual[1]]:
			for vei in node_actual[1].Edges:
				pes = vei.Destination.DijkstraDistance
				nova_dist = node_actual[0] + vei.Length
				if nova_dist < pes:
					vei.Destination.DijkstraDistance = nova_dist
					cua.put([vei.Destination.DijkstraDistance, vei.Destination])
					kmeans[vei.Destination] = node_actual[1]
			visitats[node_actual[1]] = True
	return kmeans

if __name__ == "__main__":

	# g1=graph.Graph()                     					# crear un graf
	# g1.Load("TestDijkstra/Desconectat.GR")     					# llegir el graf
	# g1.SetDistancesToEdgeLength()        					# Posar les longituts de les arestes a la distancia entre vertexs
	# start=g1.GetVertex("Start");         					# Obtenir el vertex origien de les distancies (distancia 0)
	# t0 = time.time()                    					# temps inicial
	# Dijkstra(g1,start)          							# Calcular les distancies
	# t1 = time.time()                    					# Temps final
	# print("temps: ",t1-t0)              					# imprimir el temps d'execució
	# g1.DisplayDistances()

	g = graph.Graph()  # crear un graf
	g.Load("TestDijkstra/Graf4.GR")  # llegir el graf
	g.SetDistancesToEdgeLength()  # Posar les longituts de les arestes a la distancia entre vertexs
	start = g.GetVertex("Start");  # Obtenir el vertex origien de les distancies (distancia 0)
	t0 = time.time()  # temps inicial
	DijkstraQueue(g, start)  # Calcular les distancies
	t1 = time.time()  # Temps final
	print("temps: ", t1 - t0)  # imprimir el temps d'execució
	g.DisplayDistances()

	for element in g.Vertices:
		if element.Name == "V0527" or element.Name == "V0552" or element.Name == "V0894" or element.Name == "V0914":
			print(element.DijkstraDistance)
