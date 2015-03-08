# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import random


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
                self.E = 500
                self.N = 0

                self.Replicas = []
                pass

        # Fill the Replicas with None values,
        # "Empty", non-assigned values in every replica
        def fillReplicas(self, N):
                Replicas = [[] for n in range(N)]

                for n in range(self.N):
                        for j in range(self.E):
                                Replicas[n].append(None)
                                pass
                        pass

                return Replicas

        def assignNewServer(self, sid):
                # N0
                portion = int(self.E/self.S)
                first = random.randint(0, self.E-1)
                last = first+portion

                # Handle the case where the assigned chunk needs to wrap around
                if last > self.E-1:
                        last -= (self.E-1)
                        for n in self.Replicas[0][first:]:
                                n = sid
                                pass
                        for n in self.Replicas[0][:last]:
                                n = sid
                                pass
                        pass
                # Handle the regular case, where no wrap is needed
                else:
                        for n in self.Replicas[0][first:last]:
                                n = sid
                                pass
                        pass
                #N1
                if self.N >=2:
                        if last < first:
                                newFirst = random.randint(last, first-last)
                                newLast = newFirst+portion
                                for n in self.Replicas[1][newFirst:newLast]:
                                        n = sid
                                        pass
                                pass
                        else:
                                newFirst = random.randint(0, self.E-1)
                                if (newFirst > first and newFirst < last):
                                        newFirst = last+1
                                        pass
                                newLast = newFirst+portion
                                if newLast > self.E-1:
                                        newLast -= (self.E-1)
                                        for n in self.Replicas[1][newFirst:]:
                                                n = sid
                                                pass
                                        for n in self.Replicas[1][:newLast]:
                                                n = sid
                                                pass
                                        pass
                                else:
                                        for n in self.Replicas[1][newFirst:newLast]:
                                                n = sid
                                                pass
                                pass
                        pass

                #N2
                if self.N == 3:
                        pass
                pass
                

        # Update simulation function that reads the serverId of
        # the index in every Replica for a million (using) simulated writes
        def update(self):
                counts = [0 for s in range(self.S)]
                using = self.tenperc

                for i in range(using):
                        randi =  random.randint(0, self.E-1)
                        counts[self.Replicas[0][randi]] += 1
                        for Replica in self.Replicas:
                                counts[self.Replicas[0][randi]] += 1
                                pass
                        pass

                # Change the format to percentages
                for c in range(self.S):
                        counts[c] = round((float(counts[c])/(using*(self.N+1)))*100, 2)
                        pass
                
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

                                # Check if snew is already in other replicas
                                ids = []
                                for r in range(self.N):
                                        if r != n:
                                                ids.append(self.Replicas[r][nextIndex])
                                                pass
                                        pass
                                # And change it to the next snew that's not already in other replicas
                                while snew in ids:
                                        snew = (snew+1)%self.S
                                        pass

                                        
                                # Add the serverId snew to replica n, at the nextIndex
                                self.Replicas[n][nextIndex] = snew
                        pass
                pass

        # Run addToReplicas() x times, with serverIds [nextS, nextS+1, .. x-1]
        def add(self, x, initialize):
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
                if initialize:
                        for i in range(nextS, nextS+x):
                                self.addToReplicas(i)
                                pass
                        pass
                else:
                        for i in range(nextS, nextS+x):
                                self.assignNewServer(i)
                                pass
                pass

        # Kill server with id sid from the Replicas, and handle the rest of the extents
        def killServer(self, sid):
                for x in range(self.E):
                        # Clear out sid from N0
                        if self.Replicas[0][x] == sid:
                                self.Replicas[0][x] = self.Replicas[1][x]
                                self.Replicas[1][x] += 1
                                if self.N > 2:
                                        if self.Replicas[1][x] == self.Replicas[2][x]:
                                                self.Replicas[1][x] += 1
                                                pass
                                        pass
                                pass
                        if self.N >= 2:
                                # Clear out sid from N1
                                if self.Replicas[1][x] == sid:
                                        self.Replicas[1][x] += 1
                                        if self.Replicas[1][x] == self.Replicas[0][x]:
                                                self.Replicas[1][x] += 1
                                                pass
                                        pass
                                pass
                        if self.N == 3:
                                # Clear out sid from N2
                                while self.Replicas[2][x] == sid:
                                        self.Replicas[2][x] += 1
                                        while( self.Replicas[2][x] == self.Replicas[1][x] ) or (self.Replicas[2][x] == self.Replicas[0][x] ):
                                                self.Replicas[2][x] += 1
                                                pass
                                        pass
                                pass
                        pass
                pass

        # Print the contents of all the replicas in order
        def printReplicas(self):
                i = 0
                for Replica in self.Replicas:
                        print "N"+str(i)+":"
                        print Replica
                        i += 1
                        pass
                pass

# End of class DHash

# Run part
dhash = DHash()
dhash.add(3, True)
print dhash.update()
dhash.printReplicas()

#dhash.add(1, False)
print dhash.update()
dhash.printReplicas()
