# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import random


# A Server object, with a serverId and a boolean assigned value
class Server():
        def __init__(self, serverId, assigned):
                self.serverId = serverId
                self.assigned = assigned
                pass

# Distributed hashing
class DHash():
        def __init__(self):

                # constants
                self.million = 1000000
                self.tenperc = int(self.million*0.1)
                self.oneperc = int(self.million*0.01)

                # S, Servers, systems
                # E, Extents
                # N, Nodes, reflections, duplicates
                self.S = 10
                self.E = 10000
                self.N = 3
                
                self.nextS = 0

                self.Nodes = self.fillNodes(self.N)
                pass

        # Fill the Nodes with None and False values,
        # "Empty" objects in N
        def fillNodes(self, N):
                Nodes = [[] for n in range(N)]

                for i in range(self.N):
                        for j in range(self.E):
                                Nodes[i].append(Server(None, False))
                                pass
                        pass

                return Nodes

        # Update simulation function that reads the serverId of
        # the index in every node for a million (using) simulated writes
        def update(self):
                counts = [0 for s in range(self.S)]
                
                conflicts = 0
                ccounts = [0 for s in range(self.S)]
                cplaces = []

                using = self.oneperc

                for i in range(using):
                        randi =  random.randint(0, self.E-1)

                        for Node in self.Nodes:
                                counts[Node[randi].serverId] += 1
                                pass

                        
                        pass

                # Change the format to percentages
                for c in range(self.S):
                        counts[c] = round((float(counts[c])/(using*3))*100, 2)
                        pass

                return str(counts)+", "+str(sum(counts))+"\nConflicts: "+str(conflicts)+", "+str(ccounts)+", "+str(cplaces)

        # Add snew into nodes
        #   for each node:
        #               choose a random place, make that place "assigned"
        #               run down the node and add the server handle until it reaches the next server in that node 
        #                                                                                                          or the same server value is already at that place in other nodes
        def addToNodes(self, snew):
                randis = [random.randint(0, self.E-1) for ri in range(self.N)]

                # Randomed index can't be the same as the start of an already-there server
                # OR the new serverId can't be the same as the one already-there
                for ri in range(self.N):
                        for n in self.Nodes:
                                while snew == n[randis[ri]].serverId:
                                        randis[ri] = random.randint(0, self.E-1)
                                        pass
                                pass
                        pass
                
                
                # Add the rest of values
                for n in range(self.N):
                        ri = randis[n]
                        self.addToNode(n, snew, ri)
                        pass

                pass

        # Add snew to a single node n, at point ri, start indicates whether we're coming from addToNodes or not
        def addToNode(self, n, snew, ri, start):

                # Place the starting points of the server in each node, "assigned" points
                self.Nodes[n][ri].serverId = snew
                self.Nodes[n][ri].assigned = True

                i = (ri-1)%self.E
                while snew != self.Nodes[n][i].serverId:

                        # Check other Nodes for the snew id, 
                        #       if it's already in other Nodes:
                        #       -       send it through addToNode again, with a new sid
                        ids = []
                        for Node in self.Nodes:
                                ids.append(Node[i].serverId)
                                pass
                        if snew in ids:
                                self.addToNode(n, (snew+1)%self.S, i, True)
                                break

                        # Check for the start of other servers
                        if self.Nodes[n][i].assigned != True:
                                self.Nodes[n][i].serverId = snew
                                pass
                        else:
                                break

                        i = (i-1)%self.E
                        pass

        # Run add() x times, with serverIds [nextS, nextS+1, .. x-1]
        def addX(self, x):
                for i in range(self.nextS, x):
                        self.addToNodes(i)
                        pass


                if self.nextS == 0:
                        for i in range(self.nextS, 3):
                                self.addToNodes(i)
                                pass
                        pass
                self.nextS += x

                pass

        # Kill server with id sid from the nodes, and handle the rest of the extents
        def killServer(self, sid):
                pass




dhash = DHash()
dhash.addX(10)
print "<0, 1, 2, 3, 4, 5, 6, 7, 8, 9>"
print dhash.update()
i = 0
for Node in dhash.Nodes:
        print "N"+str(i)+":"
        x = 0
        printstr = ""
        for s in Node:
                printstr += str(s.serverId)+" "+str(s.assigned)+", "
                x += 1
        print "["+printstr[0:-2]+"]"
        i += 1
