# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import random


# Distributed hashing
class DHash():
        def __init__(self, extent):

                # S, Servers, systems
                # E, Extents
                # N, Reflections, duplicates, replicas
                # Start at zero, change this as we add more
                self.S = 0 
                self.E = extent
                self.N = 0

                self.Replicas = []
                pass

        # Initialize the Replicas with None values,
        # "Empty", non-assigned values in every replica
        def fillReplicas(self, N):
                Replicas = [[] for n in range(N)]
                for n in range(self.N):
                        for j in range(self.E):
                                Replicas[n].append(None)
                                pass
                        pass

                return Replicas

        
        # Add a server, assign a part of the extent,
        # including the backup replicas, to that server
        def assignNewServer(self, sid):
                print "assignNewServer("+str(sid)+")"
                # N0
                portion = int(self.E/self.S)
                first = random.randint(0, self.E-1)
                last = first+portion

                if last > self.E-1: # N0 wraparound
                        last -= (self.E-1)
                        for n in range(first, len(self.Replicas[0])):
                                self.Replicas[0][n] = sid
                                pass
                        for n in range(0,last):
                                self.Replicas[0][n] = sid
                                pass
                        pass
                else: # No N0 wraparound
                        for n in range(first, last):
                                self.Replicas[0][n] = sid
                                pass
                        pass
                #N1
                if self.N >=2:
                        if last < first: #N0 wraps around
                                n1First = random.randint(last, first-last)
                                n1Last = n1First+portion
                                for n in range(self.Replicas[1][n1First:n1Last]):
                                        self.Replicas[1][n] = sid
                                        pass
                                pass
                        else: #N0 doesn't wrap around
                                n1First = random.randint(0, self.E-1)
                                if (n1First > first and n1First < last):
                                        n1First = last+1
                                        pass
                                n1Last = n1First+portion
                                if n1Last > self.E-1: #N1 wraparound
                                        n1Last -= (self.E-1)
                                        for n in range(n1First, len(self.Replicas[1])):
                                                self.Replicas[1][n] = sid
                                                pass
                                        for n in range(0,n1Last):
                                                self.Replicas[1][n] = sid
                                                pass
                                        pass
                                else: #No N1 wraparound
                                        for n in range(n1First, n1Last):
                                                self.Replicas[1][n] = sid
                                                pass
                                        pass
                                pass
                        pass

                #N2
                if self.N == 3:
                        if last < first: #N0 wraparound
                                n2First = random.randint(last, first-last)
                                if (n2First > n1First) and (n2First < n1Last):
                                        n2First = n1Last+1
                                        pass
                                n2Last = n2First+portion
                                if (n2Last > n1First) and (n2Last < n1Last):
                                        n2Last = n1First-1
                                        pass
                                pass
                        else: #No N0 wraparound
                                if n1First > n1Last: #N1 wraparound
                                        n2First = random.randint(n1Last, n1First-n1Last)
                                        if (n2First > first) and (n2First < last):
                                                n2First = last+1
                                                pass
                                        n2Last = n2First+portion
                                        if (n2Last > first) and (n2Last < last):
                                                n2Last = last-1
                                        if (n2Last > self.E-1):
                                                n2Last = self.E-1
                                                pass
                                        pass
                                else: #No N1 wraparound
                                        n2First = random.randint(0, self.E)
                                        if (n2First > first) and (n2First < last):
                                                n2First = last+1
                                                pass
                                        if (n2First > n1First) and (n2First < n1Last):
                                                n2First = n1Last+1
                                                pass
                                        n2Last = n2First+portion
                                        if (n2Last > first) and (n2Last < last):
                                                n2First = first-1
                                                pass
                                        if (n2Last > n1First) and (n2Last < n1Last):
                                                n2First = n1First-1
                                                pass
                                        if (n2Last > self.E-1):
                                                n2Last = self.E-1
                                                pass
                                        pass
                                pass
                        if n2Last > n2First: #No N2 wraparound
                                for n in range(n2First, n2Last):
                                        self.Replicas[2][n] = sid
                                        pass
                                pass
                        else: #N2 wraparound
                                for n in range(0, n2Last):
                                        self.Replicas[2][n] = sid
                                        pass
                                for n in range(n2First, len(self.Replicas[2])):
                                        self.Replicas[2][n] = sid
                                        pass
                                pass
                        pass   
                pass
                

        # Update simulation function that reads the serverId of
        # the index in every Replica for simulated writes
        def update(self, using):
                counts = [0 for s in range(self.S)]

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
                print "addToReplicas("+str(snew)+")"
                randis = [random.randint(0, self.E-1) for n in range(self.N)]

                # Randomed index can't be the same as the server that's already there
                for n in range(self.N):
                        for rep in self.Replicas:
                                while snew == rep[randis[n]]:
                                        randis[n] = random.randint(0, self.E-1)
                                        pass
                                pass
                        pass
                
                # Use the randomized index to add the server into the replicas
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
                print "add("+str(x)+", "+str(initialize)+")"
                # Readjust the number of servers
                nextS = self.S
                self.S += x

                # Readjust the number of replicas, and fill then accordingly,
                # with the new values
                self.N = self.S
                if self.N > 3:
                        self.N = 3
                        pass
                if initialize:
                        self.Replicas = self.fillReplicas(self.N)
                        pass
                
                # Start adding to replicas
                
                for i in range(nextS, nextS+x):
                        if initialize:
                                self.addToReplicas(i)
                                pass
                        else:
                                self.assignNewServer(i)
                                pass
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
dhash = DHash(500)
dhash.add(10, True)
print "Initialized with 10 servers, writing 1,000,000 times:"
print dhash.update(1000000)
#dhash.printReplicas()

dhash.add(3, False)
print "Added 3 servers, writing 1,000,000 times:"
print dhash.update(1000000)
#dhash.printReplicas()

dhash.killServer(5)
print "Killed sid=5, writing 1,000,000 times:"
print dhash.update(1000000)
#dhash.printReplicas()

dhash.add(1, False)
print "Added 1 server, writing 1,000,000 times, five times:"
print dhash.update(1000000)
#print dhash.update(1000000)
#print dhash.update(1000000)
#print dhash.update(1000000)
#print dhash.update(1000000)
dhash.printReplicas()
