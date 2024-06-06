import graph
import math
import sys
import queue
import dijkstra


def SalesmanTrackBranchAndBound2(g, visits):
    # if len(g.Vertices)>80:
    #     return graph.Track(g)

    def calcular_llargada(track):
        return sum(aresta.Length for aresta in track.Edges)

    candidats = visits.Vertices

    n = len(candidats)
    indexs = {candidats[i]: i for i in range(n)}

    camins_optims = np.full((n, n), None, dtype=object)
    llargades_optims = np.zeros((n, n))

    maxims = [0 for _ in range(n)]
    minims = [sys.float_info.max for _ in range(n)]

    for i in range(n):  # -1
        actual = candidats[i]
        camins = dijkstra.DijkstraQueue(g, actual)

        for node in candidats:

            if node is not actual:  # and node is not final:
                index = indexs[node]
                if camins_optims[i, index] is None:
                    track = graph.Track(g)
                    seg = node
                    while seg is not actual:
                        aresta = camins[seg]
                        track.AddFirst(aresta)
                        seg = aresta.Origin

                    camins_optims[i, index] = track
                    llargades_optims[i, index] = calcular_llargada(track)

    for i in range(n):
        for j in range(n):
            if camins_optims[i][j] is not None:
                maxims[i] = max(maxims[i], llargades_optims[i][j])
                minims[i] = min(minims[i], llargades_optims[i][j])

    no_visitats = [i for i in range(n)]
    cota_superior_global = sum(maxims)
    cota_inferior_global = sum(minims)
    final = graph.Track(g)
    cua = []
    cami = [0]
    heapq.heappush(cua, (cota_inferior_global, cota_superior_global, cami, no_visitats, 0))  # candidats[0] ))

    while no_visitats:
        cota_inferior = cua[0][0]
        cota_superior = cua[0][1]
        cami = cua[0][2]
        no_visitats = cua[0][3][:]
        actual = cua[0][4]

        if len(no_visitats) == 1:
            break

        # index1 = indexs[actual]
        no_visitats.remove(actual)
        heapq.heappop(cua)
        maxs = []

        # for node in candidats:
        for index2 in range(n):
            # index2 = indexs[node]
            if actual != index2 and index2 in no_visitats:  # if node is not actual and index2 in no_visitats:#not nodellista(node, visitats):# and node is not candidats[-1]:

                ultim = indexs[candidats[-1]]
                if len(no_visitats) == 1 and index2 is ultim:  # node is candidats[-1]:

                    nou_cami = cami + [index2]
                    llargada = llargades_optims[actual][index2]

                    superior = cota_superior - maxims[index2] + llargada
                    inferior = cota_inferior - minims[index2] + llargada
                    maxs.append(superior)
                    if cota_superior_global + 1e-5 >= inferior:
                        heapq.heappush(cua, (inferior, superior, nou_cami, no_visitats,
                                             index2))  # node )) #afegim id per poder comparar si els dos primers elemnts son iguals


                else:
                    if index2 is not ultim:
                        nou_cami = cami + [index2]
                        llargada = llargades_optims[actual][index2]
                        superior = cota_superior - maxims[index2] + llargada
                        maxs.append(superior)
                        inferior = cota_inferior - minims[index2] + llargada

                        if cota_superior_global + 1e-5 >= inferior:
                            heapq.heappush(cua, (inferior, superior, nou_cami, no_visitats, index2))  # node ))

        cota_superior_global = min(maxs)
        no_visitats = cua[0][3][:]

    cami_final = cua[0][2]
    for i in range(len(cami_final) - 1):
        final.Append(camins_optims[cami_final[i], cami_final[i + 1]])

    return final


if __name__ == '__main__':
    g = graph.Graph()  # crear un graf
    g.Load("TestSalesMan/Graf10_20_5.GR")  # llegir el graf
    g.SetDistancesToEdgeLength()  # Posar les longituts de les arestes a la distancia entre vertexs
    vis = graph.Visits(g);  # Crear visites
    vis.Load("TestSalesMan/Graf10_20_5.VIS")  # Llegir les vistes
    t0 = time.time()  # temps inicial

    # Cerca cami que pasi per les visites
    trk = SalesmanTrackBranchAndBound2(g, vis)  # test branch&bound
    # trk = graph.Track(g)

    t1 = time.time()  # Temps final
    print("temps: {:.20f}".format(t1 - t0))  # imprimir el temps d'execució amb molts decimals
    trk.Display(vis)