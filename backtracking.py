import graph
import sys
import time

def SalesmanTrackBacktracking(g, visits):

    camiFinal = graph.Track(g)
    camiActual = graph.Track(g)
    distanciaFinal = sys.float_info.max
    arestesVisitades = set()
    compFi = len(visits.Vertices)

    # Marcar els vèrtexs que estan a la llista de visits com a visitats que seran els vèrtexs a visitar, a més a més, 
    #afegim un nou paràmetre per indicar si ha estat visitat
    for vertex in g.Vertices:
        vertex.visitada = vertex in visits.Vertices
        if vertex.visitada:
            vertex.estaVisitat = 0

    visits.Vertices[0].estaVisitat = 1 # Comencem pel primer vèrtex, així que el podem marcar com ha que ha estat visitat

    def backtracking(vertexActual, distanciaActual, camiActual, comp):

        # Definir variables locals per evitar modificar les globals
        nonlocal distanciaFinal, camiFinal
        
        # Verificar si el camí actual visita tots els vèrtexs de la llista (es va sumant al comptador per cada vèrtex visitat) i acaba amb l'últim vèrtex de `visits`
        if  comp >= compFi and vertexActual is visits.Vertices[-1]:
            # Si la distància actual és menor que la distància final, actualitzar distància i camí
            if distanciaActual < distanciaFinal:
                distanciaFinal = distanciaActual
                camiFinal.Edges[:] = camiActual.Edges[:]
            return
        
        # Poda l'arbre de cerca, és a dir, tornem enrere si la distància actual ja és major que la distància final
        if distanciaActual >= distanciaFinal:
            return
        
        # Explorar les arestes adjacents al vèrtex actual
        for aresta in vertexActual.Edges:
            # Verificar si l'aresta no ha estat visitada abans
            if aresta not in arestesVisitades:
                vei = aresta.Destination
                """
                # Marcar el vèrtex visitat
                if vei.visitada:
                    boolea = vei.estaVisitat 
                    vei.estaVisitat += 1
                    if boolea < 1 or (vei is visits.Vertices[-1]): #and boolea != 1):
                        comp+=1
                """
                if vei.visitada and  vei.estaVisitat==1:
                    vei.estaVisitat = 1
                    comp += 1

                # Marcar l'aresta com a visitada
                arestesVisitades.add(aresta)
                camiActual.AddLast(aresta)
                
                # Crida recursiva amb el nou veí
                backtracking(vei, distanciaActual + aresta.Length, camiActual, comp)
                
                # Desmarcar l'aresta com a no visitada
                arestesVisitades.remove(aresta)

                # Retirar l'aresta del camí actual
                camiActual.Edges.pop()

                # Desmarcar el vèrtex visitat
                if vei.visitada:
                    vei.estaVisitat = boolea   
                    if boolea < 1 or (vei is visits.Vertices[-1]): #and boolea > 1):
                        comp-=1
        
        return
    
    # Iniciar la cerca amb el primer vèrtex de visits amb distància 0
    backtracking(visits.Vertices[0], 0, camiActual, 1)

    # Retornar el millor camí trobat
    return camiFinal

if __name__ == '__main__':
    g=graph.Graph()                     					# crear un graf
    g.Load("TestSalesMan/Graf10_20_5.GR")  				# llegir el graf
    g.SetDistancesToEdgeLength()        					# Posar les longituts de les arestes a la distancia entre vertexs
    vis=graph.Visits(g);									# Crear visites
    vis.Load("TestSalesMan/Graf10_20_5.VIS")				# Llegir les vistes
    t0 = time.time()                    					# temps inicial



    #Cerca cami que pasi per les visites
    #trk=greedy.SalesmanTrackGreedy(g,vis)                       #test greedy   
    trk=SalesmanTrackBacktracking(g,vis)          #test backtracking
    #trk=SalesmanTrackBacktrackingGreedy(g,vis)    #test backtracking-greedy
    #trk=branchAndBound.SalesmanTrackBranchAndBound2(g,vis)     #test branch&bound
    #trk = graph.Track(g)

    t1 = time.time()                    					# Temps final
    print("temps: {:.20f}".format(t1-t0))              					# imprimir el temps d'execució amb molts decimals
    trk.Display(vis)
