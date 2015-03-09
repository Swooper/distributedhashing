Haukur Jónasson
Tryggvi Þór Guðmundsson


DHash class:
	Holds all the variables and functions of the project

	Class variables:
		S: number of servers
		E: number extents of each replica, 10000
		N: number of replicas
		Replicas: the replicas themselves as a list of lists

	Class functions:
		fillReplicas(N):
			Fill N Replicas with empty values and return them as a list of lists

		assignNewServer(sid):
			Add a new server with the server id sid to all the replicas with a 
			randomly assigned starting point and a size of (E/S), this is used 
			after initialisation

		update(using):
			Run a simulated update on the system with a million (using) read 
			operations to measure the distribution of the servers in the system

		addToReplicas(snew):
			Add a new server with the server id snew to all the replicas with a 
			randomly assigned starting point, this is part of the initialisation

		add(x, initialize):
			Add x number of servers to the system, the first call to this function 
			must have the value of initialize set to True, the system is then initialized 
			using addToReplicas. Subsequent calls to this function must have the 
			value of initialize set to False, as the system has already been 
			initialized

		killServer(sid):
			Kills the server with the id sid and substitutes the cleared values 
			with values from other replicas

		printReplicas():
			Prints out all the replicas with their values in a readable form