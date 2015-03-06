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
                # N, Reflections, duplicates, replicas
                self.S = 10
                self.E = 1000
                self.N = 3
                
                self.nextS = 0

                self.Replicas = self.fillReplicas(self.N)
                pass

        # Fill the Replicas with None and False values,
        # "Empty" objects in N
        def fillReplicas(self, N):
                Replicas = [[] for n in range(N)]

                for i in range(self.N):
                        for j in range(self.E):
                                Replicas[i].append(Server(None, False))
                                pass
                        pass

                return Replicas

        # Update simulation function that reads the serverId of
        # the index in every Replica for a million (using) simulated writes
        def update(self):
                counts = [0 for s in range(self.S)]
                
                conflicts = 0
                ccounts = [0 for s in range(self.S)]
                cplaces = []

                using = self.oneperc

                for i in range(using):
                        randi =  random.randint(0, self.E-1)

                        for Replica in self.Replicas:
                                counts[Replica[randi].serverId] += 1
                                pass

                        
                        pass

                # Change the format to percentages
                for c in range(self.S):
                        counts[c] = round((float(counts[c])/(using*3))*100, 2)
                        pass

                return str(counts)+", "+str(sum(counts))+"\nConflicts: "+str(conflicts)+", "+str(ccounts)+", "+str(cplaces)

        # Add snew into Replicas
        #   for each Replica:
        #               choose a random place, make that place "assigned"
        #               run down the Replica and add the server handle until it reaches the next server in that Replica 
        #                                                                                                          or the same server value is already at that place in other Replicas
        def addToReplicas(self, snew):
                randis = [random.randint(0, self.E-1) for ri in range(self.N)]

                # Randomed index can't be the same as the start of an already-there server
                # OR the new serverId can't be the same as the one already-there
                for ri in range(self.N):
                        for n in self.Replicas:
                                while snew == n[randis[ri]].serverId:
                                        randis[ri] = random.randint(0, self.E-1)
                                        pass
                                pass
                        pass
                
                
                # Use the randomized index for 
                for n in range(self.N):
                        ri = randis[n]
                        self.addToReplica(n, snew, ri)
                        pass

                pass

        # Add snew to a single Replica n, at point ri, start indicates whether we're coming from addToReplicas or not
        def addToReplica(self, n, snew, ri):

                # Place the starting points of the server in each Replica, "assigned" points
                self.Replicas[n][ri].serverId = snew
                self.Replicas[n][ri].assigned = True

                i = (ri-1)%self.E
                while snew != self.Replicas[n][i].serverId:

                        # Check other Replicas for the snew id, 
                        #       if it's already in other Replicas:
                        #       -       send it through addToReplica again, with a new sid
                        ids = []
                        for Replica in self.Replicas:
                                ids.append(Replica[i].serverId)
                                pass
                        if snew in ids:
                                self.addToReplica(n, (snew+1)%self.S, i)
                                break

                        # Check for the start of other servers
                        if self.Replicas[n][i].assigned != True:
                                self.Replicas[n][i].serverId = snew
                                pass
                        else:
                                break

                        i = (i-1)%self.E
                        pass

        # Run add() x times, with serverIds [nextS, nextS+1, .. x-1]
        def addX(self, x):
                for i in range(self.nextS, x):
                        self.addToReplicas(i)
                        pass


                if self.nextS == 0:
                        for i in range(self.nextS, 3):
                                self.addToReplicas(i)
                                pass
                        pass
                self.nextS += x

                pass

        # Kill server with id sid from the Replicas, and handle the rest of the extents
        def killServer(self, sid):
                pass




dhash = DHash()
dhash.addX(10)
print "<0, 1, 2, 3, 4, 5, 6, 7, 8, 9>"
print dhash.update()
i = 0
for Replica in dhash.Replicas:
        print "N"+str(i)+":"
        x = 0
        printstr = ""
        for s in Replica:
                printstr += str(s.serverId)+" "+str(s.assigned)+", "
                x += 1
        print "["+printstr[0:-2]+"]"
        i += 1
