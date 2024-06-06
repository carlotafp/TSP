import graph
import math
import sys
import queue
import dijkstra


def SalesmanTrackBacktracking(g,visits):

    # Aquesta funció auxiliar és una funció recursiva que trobar el camí més curt possible en el graf.
    def SalesmanTrackBacktracking_Rec(actual,visits,cami_actual,cami_optim):
        
        # Comprovem si el camí actual és més llarg o igual que el camí més curt fins ara.
        if cami_actual[1]>=cami_optim[1] and cami_optim[1]>0:
            # Si es compleix aquesta condició, llavors el camí actual no pot ser la solució, així que retornem None.
            return None

        # Ara comprovem si el node actual és el node final a visitar i si ja hem visitat tots els nodes que volíem visitar.
        elif actual==ultim:
            if all(v.explorat>0 for v in visits.Vertices):
                # Si és així, hem trobat la solució.
                # Actualitzem el camí més curt fins ara.
                cami_optim[0].Edges=list(cami_actual[0])
                cami_optim[1]=cami_actual[1]
                return None
        
        # Recorrem per tots els veins.
        for edge in actual.Edges:
            # Comprovem si no és visitat aquesta aresta per poder pasar-hi.
            if not edge.Saved:

                # Determinem l'aresta com a visitat.
                edge.Saved=True

                # Comprovem si és visitat l'aresta.
                if edge.Destination.visitat:
                    # Visitem el node explorat
                    edge.Destination.explorat+=1

                # Afegim l'edge al cami_actual.
                cami_actual[0].append(edge)
                # I li sumem a longitud de l'aresta per aconseguir el total del camí.
                cami_actual[1]+=edge.Length

                # Fem crida a la funció recursiva.
                SalesmanTrackBacktracking_Rec(edge.Destination,visits,cami_actual,cami_optim)

                # Apliquem Backtracking.
                edge_borrat=cami_actual[0].pop(-1)
                edge_borrat.Saved=False
                cami_actual[1]-=edge_borrat.Length
                # Si el node esta visitat, borrem una aresta de visitat.
                if edge_borrat.Destination.visitat:
                    edge_borrat.Destination.explorat-=1

    # Incialitem els vertexs primer i ultim.
    primer=visits.Vertices[0]
    ultim=visits.Vertices[-1]

    # Se li crea un atribut a tots els vertex on és True si és un vertex que cal visitar o False si no, 
    # i en el cas que calgui visitar-lo li posem un 0 si no s'ha explorat mai i un 1 si si que s'ha fet.
    for v in g.Vertices:
        v.visitat = False 
    for visit in visits.Vertices:
        visit.visitat = True
        visit.explorat = 0
    primer.explorat = 1

    track_final = graph.Track(g)
    # Inicialitzem una llista, on guardem el Track òptim i el pes total d'aquest Track. 
    cami_optim=[track_final,0]
    # Creem una pila on emmagatzem tots els edges que formaran el Track candidat per ser el camí òptim.
    cami_actual=[[],0]  

    # Fem crida a la funció recursiva.
    SalesmanTrackBacktracking_Rec(primer,visits,cami_actual,cami_optim)

    return track_final
