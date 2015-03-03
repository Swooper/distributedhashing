# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

n1 = []
n2 = []
n3 = []

extent = 0
serverIds = []
servers = []
serverCount = 0

class Server(object):

        def __init__(self, serverId, first, last):
                self.serverId = serverId
                self.first = first
                self.last = last
                
def start(s, e):
        extent = e
        populateN()
        addServer(s)
        
def populateN():
        int i = 0
        for i in range(extent):
                n1.append("")
                n2.append("")
                n3.append("")
                
def addServer(s):
        partitionSize = extent / s
        serverCount += s
        while s>0:
                i = 0
                while i in serverIds:
                        i+=1
                first = (serverCount-s)*partitionSize
                last = first+partitionSize-1
                servers.append(new Server(i, first, last))
                serverIds.append(i)
                s-=1

def killServer(serverId):
        pass

start(10, 10000)
