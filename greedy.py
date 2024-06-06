
import graph
import math
import sys
import queue
import dijkstra
import time
import copy

# SalesmanTrackGreedy ==========================================================

def SalesmanTrackGreedy(g, visits):
    v = visits.Vertices[0]
    candidats = visits.Vertices[1:-1]

    track = graph.Track(g)
    
    while candidats:
        llista_arestes = []
        camins = dijkstra.DijkstraQueue(g, v)
        
        minim = sys.float_info.max
        v1 = None
        for node in candidats:
            if node.DijkstraDistance < minim:
                v1, minim = node, node.DijkstraDistance

        ver = v1
        while v1 is not v:
            vei = camins[v1]
            if v1 in candidats:
                candidats.remove(v1)
            for aresta in vei.Edges: 
                if aresta.Destination is v1:
                    llista_arestes.append(aresta)
                    break
            v1 = vei
        v = ver

        llista_arestes = llista_arestes[::-1]
        for aresta in llista_arestes:
            track.AddLast(aresta)

    llista_arestes = []
    camins = dijkstra.DijkstraQueue(g, v)

    ver = visits.Vertices[-1]
    while ver is not v:
        vei = camins[ver]
        for aresta in vei.Edges: 
            if aresta.Destination is ver:
                llista_arestes.append(aresta)
                break
        ver = vei

    llista_arestes = llista_arestes[::-1]
    for aresta in llista_arestes:
        track.AddLast(aresta)

    return track
