import numpy
'''
Determine whether the conductance behaves like an expoential growth curve within the first transition period, or does it come second.
Do the same for exponential decay which is whatever the exponetial growth isnt. 
'''
def determineBehavior(g_Array):
	#convert conductance to float array 
	conductance = map(float,g_Array)
	length = len(conductance)

	#If phase1 = 1 then growth, else -1 which means decay
	phase1 = 0
	phase2 = 0

	#Check each quartile and see overall is the data decaying or growing
	#Check first quartile and Second Quartile
	if sum(conductance[:length/4]) > sum(conductance[length/4:length/2]):
		phase1 = -1
	else:
		phase1 = 1
	#Check Third Quartile against Forth Quartile
	if sum(conductance[length/2:3*length/4]) > sum(conductance[3*length/4:length]):
		phase2 = -1
	else:
		phase2 = 1

	return phase1, phase2

'''
Find Critical Points where exponential decay and growth start
'''
def FindCriticalPoints( phase1 , g_Array ):

	#convert conductance to float array 
	conductance = []
	for g in map(float,g_Array):
		if g not in conductance:
			conductance.append(g)

	#Initialize total length and transition point
	length = len(conductance)
	transition_point = length/2

	#Find the main transition point between growth and decay
	for g in conductance[3:length-4] :
		i = conductance.index(g)

		#If first phase is growth, find the first point to decrease
		if phase1 == 1 and g > conductance[i+1] and g > conductance[i+3] and g > conductance[i-3]:
			transition_point = i 
			break
			
		#If first phase is decay, fidn the first point to increase
		elif phase1 == -1 and g < conductance[i+1] and g < conductance[i+3] and g < conductance[i-3]:
			transition_point = i 
			break
	
	startpoint = 0
	endpoint = 0

	#If growth
	if phase1 == 1:
		startpoint = min(conductance[:transition_point-1])
		endpoint = min(conductance[transition_point+1:])
	else:
		startpoint = max(conductance[:transition_point-1])
		endpoint = max(conductance[transition_point+1:])

	return g_Array.index(startpoint), g_Array.index(conductance[transition_point]), g_Array.index(endpoint)

'''
Find mean lifetime constant for Decay or Growth
'''
def FindTau(phase, g_start):
	if phase == -1:
		return float((1/numpy.exp(1)) * g_start)
	else:
		return float((1-(1/numpy.exp(1))) * g_start)
'''
Find the Rate of Decay or Growth
'''
def FindRate(tau):
	return float(1/tau)

'''
Exponential Decay Function
'''
def DecayFunction(time,tau,Gstart,Gasymptote):
	return numpy.exp( (-1*time)/tau ) * (Gstart- Gasymptote) + Gasymptote
'''
Inverse Exponential Decay Function
'''
def InverseDecayFunction(time,tau,Gstart,Gasymptote):
	return (1 - numpy.exp( (-1*time)/tau )) * (Gstart- Gasymptote) + Gasymptote




	
