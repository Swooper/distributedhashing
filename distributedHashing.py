# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import random


# A Server object, with a serverId and a boolean assigned value
class Server():
        def __init__(self, serverId, start, end):
                self.serverId = serverId
                self.start = start
                self.end = end
                pass

# Distributed hashing
class DHash():
        def __init__(self):

                # constants for the "update" function
                self.million = 1000000
                self.tenperc = int(self.million*0.1)
                self.oneperc = int(self.million*0.01)

                # S, Servers, systems
                # E, Extents
                # N, Reflections, duplicates, replicas
                # Start at zero, change this as we add more
                self.S = 0 
                self.E = 50
                self.N = 0

                self.Servers = []
                self.Replicas = []
                pass

        # Fill the Replicas with None and False values,
        # "Empty" objects in N
        def fillReplicas(self, N):
                Replicas = [[] for n in range(N)]

                for n in range(self.N):
                        for j in range(self.E):
                                Replicas[n].append(None)
                                pass
                        pass

                return Replicas

        # Update simulation function that reads the serverId of
        # the index in every Replica for a million (using) simulated writes
        def update(self):
                counts = [0 for s in range(self.S)]
                using = self.oneperc


                for i in range(using):
                        randi =  random.randint(0, self.E-1)

                        # for Replica in self.Replicas:
                        #         counts[Replica[randi].serverId] += 1
                        #         pass
                        
                        pass

                # Change the format to percentages
                #       round((float(counts[c])/(using*3))*100, 2)

                return counts

        # Add snew into Replicas
        #   for each Replica:
        def addToReplicas(self, snew):
                randis = [random.randint(0, self.E-1) for n in range(self.N)]

                # Randomed index can't be the same as the server that's already there
                for n in range(self.N):
                        for rep in self.Replicas:
                                while snew == rep[randis[n]]:
                                        randis[n] = random.randint(0, self.E-1)
                                        pass
                                pass
                        pass
                
                # Use the randomized index for add the server into the replicas
                # Going from randis[n] down (and wrap-around) to randis[n+1]
                for e in reversed(range(self.E)):
                        for n in range(self.N):
                                nextIndex = (e+randis[n]+1)%self.E

                                # Check if snew is already in others
                                ids = []
                                for r in range(self.N):
                                        if r != n:
                                                ids.append(self.Replicas[r][nextIndex])
                                                pass
                                        pass
                                while snew in ids:
                                        snew = (snew+1)%self.S
                                        pass

                                        
                                self.addToReplica(snew, n, nextIndex)
                        pass

                pass

        # Add the serverId snew to replica n, at point i
        #       If it clashes at point i in other replicas:
        #               Use the next snew (wrapped-around)
        def addToReplica(self, snew, n, i):

                self.Replicas[n][i] = snew
                pass

        # Run add() x times, with serverIds [nextS, nextS+1, .. x-1]
        def addX(self, x):
                # Readjust the number of servers
                nextS = self.S
                self.S += x

                # Readjust the number of replicas, and fill then accordingly,
                # with the new values
                self.N = self.S
                if self.N > 3:
                        self.N = 3
                        pass
                self.Replicas = self.fillReplicas(self.N)

                
                # Start adding to replicas
                for i in range(nextS, nextS+x):
                        self.addToReplicas(i)
                        pass

                pass

        # Kill server with id sid from the Replicas, and handle the rest of the extents
        def killServer(self, sid):
                pass



# 
dhash = DHash()
dhash.addX(2)
# dhash.addX(5)
# dhash.addX(5)
# dhash.addX(5)
# dhash.addX(5)
# print dhash.update()

i = 0
for Replica in dhash.Replicas:
        print "N"+str(i)+":"
        printstr = ""
        for s in Replica:
                printstr += str(s)+", "
        print "["+printstr[0:-2]+"]"
        i += 1
