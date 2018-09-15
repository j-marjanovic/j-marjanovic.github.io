Title: Theremin Simulation
Date: 2014-11-06 22:00
Category: Projects
Tags: Theremin
Status: Draft

	:::python
	# -*- coding: utf-8 -*-
	"""
	Created on Sun Nov  2 14:54:35 2014

	@author: jan
	"""

	import numpy as np
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	import matplotlib.pyplot as plt
	import scipy.constants as const

	#   b, y
	# A
	# |
	# +----> a, x
	a = 0.3         # x dimension of space
	b = 1.0         # y dimension of space

	Na = 50         # number of nodes in x
	Nb = 100        # number of nodes in y

	x_ant = 0.1     # antenna x position
	y_ant = 0.5     # antenna y position
	l_ant = 0.5     # antenna length
	V_ant = 1.0     # antenna voltage (capacitance is Q/V, so we set V to 1)

	x_man = 0.2     # man x position
	y_man = 0.4     # man y position
	l_man = 0.8     # man length (height)
	V_man = 0.0     # man voltage

	l_hand = 0.06   # hand length   <--- VERY IMPORTANT PARAMETER
	x_hand = x_man-l_hand/2.0
	y_hand = 0.6    # hand y position
	V_hand = V_man  # hand voltage has same potential as man


	_err_ppm = 1000   # max diff from two consecutive iterations to stop the loop

	###############################################################################
	# Setup
	#   We create 2D grid of nodes with their voltage and save if they are set
	#   to fixed voltage (e.g. grounded) or is there a field which should be 
	#   caculated

	V = np.zeros((Na,Nb))
	fixed = [[False]*Nb for i in range(Na)]

	def placeObject(x,y,l,vert,V0):
	    global V
	    if vert: 
		Nx       = int(x/a*Na)
		Ny_start = int((y-l/2.0)/b*Nb) 
		Ny_stop  = int((y+l/2.0)/b*Nb) 
		
		for i in range(Ny_start, Ny_stop+1):
		    V[Nx][i] = V0
		    fixed[Nx][i] = True
	    else:
		Nx_start = int((x-l/2.0)/a*Na)
		Nx_stop  = int((x+l/2.0)/a*Na)
		Ny       = int(y/b*Nb) 
		
		for i in range(Nx_start, Nx_stop+1):
		    V[i][Ny] = V0            
		    fixed[i][Ny] = True
	    
	    
	placeObject(x_ant,  y_ant,  l_ant,  True,  V_ant)
	placeObject(x_man,  y_man,  l_man,  True,  V_man)
	placeObject(x_hand, y_hand, l_hand, False, V_hand)

	###############################################################################
	# Calculation
	#   We are solving 1st Maxwell equation:
	#      div D = ro -> div E = ro/eps --> div E = 0 
	#
	#   Combined with definiton of voltage potential:
	#      E = - grad V
	#
	#   Results in Laplace equation:
	#      div grad V = 0


	m, n = V.shape

	def iterate():
	    global V
	    for i in range(m):
		for j in range(n):
		    if i == 0 and j == 0:
		        V_T = (V[0][1] + V[1][0]) / 2.0
		    elif i == m-1 and j == 0:
		        V_T = (V[i-1][0] + V[i][1]) / 2.0
		    elif i == 0 and j == n-1:
		        V_T = (V[0][j-1] + V[1][j]) / 2.0        
		    elif i == m-1 and j == n-1:
		        V_T = (V[i][j-1] + V[i-1][j]) / 2.0   
		    elif i == 0:
		        V_T = (V[0][j-1] + V[0][j+1] + V[1][j]) / 3.0 
		    elif i == m-1:
		        V_T = (V[i][j-1] + V[i][j+1] + V[i-1][j]) / 3.0      
		    elif j == 0:
		        V_T = (V[i-1][0] + V[i+1][0] + V[i][1]) / 3.0 
		    elif j == n-1:
		        V_T = (V[i-1][j] + V[i+1][j] + V[i][j-1]) / 3.0    
		    else:
		        V_T = (V[i-1][j] + V[i+1][j] + V[i][j-1] + V[i][j+1]) / 4.0    
		      
		    if not fixed[i][j]:
		        V[i][j] = V_T
		        

	e = []
	for i in range(1000):
	    Vprev = V.copy()
	    iterate()
	    ei = np.sum(Vprev - V)
	    e.append(ei)
	    if(np.abs(ei/Na/Nb) < _err_ppm*1e-6):
		print "Done"
		break


	###############################################################################
	# Calc C
	#   Electric field is calculated as E = - grad V
	#   Charge is calculated from Gauss equation in integral form

	Ex = np.zeros((Na,Nb))
	Ey = np.zeros((Na,Nb))
	Eabs = np.zeros((Na,Nb)) 
	for i in range(m-1):
	    for j in range(n-1):
		Ex[i][j] = ( V[i+1][j] - V[i][j] ) / (a/Na)
		Ey[i][j] = ( V[i][j+1] - V[i][j] ) / (b/Nb)
		Eabs[i][j] = np.sqrt(Ex[i][j]*Ex[i][j]+Ey[i][j]*Ey[i][j])
		
	    

	Nx       = int(x_ant/a*Na)
	Ny_start = int((y_ant-l_ant/2.0)/b*Nb) 
	Ny_stop  = int((y_ant+l_ant/2.0)/b*Nb) 


	# Gauss 
	Q = 0

	for i in range(Ny_start, Ny_stop+1):
	    Q += Eabs[Nx+1][i]
	    Q += Eabs[Nx-1][i]
	    
	C = const.epsilon_0 * Q

	###############################################################################
	# Plot
	X,Y = np.meshgrid(np.linspace(0,b, Nb), np.linspace(0,a, Na))
	fig = plt.figure(figsize=(8,6))
	ax = fig.gca(projection='3d')

	ax.view_init(-90,0)
	ax.plot_surface(X, Y, V, rstride=1, cstride=1, cmap=cm.rainbow,
		linewidth=0, antialiased=False)
		
	ax.text(0.95, 2.5, 0, 'C = ' + str(round(C*1e9,4)) + " nF",
		verticalalignment='bottom', horizontalalignment='right',
		transform=ax.transAxes, fontsize=12)

	ax.set_title('Distance = ' + str((x_hand-l_hand/2.0) - x_ant ) + ' cm') 
