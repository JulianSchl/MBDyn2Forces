#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen
from mbc_py_interface import mbcNodal
import numpy as np
import time

number_of_forces = 2
nodal = []

input_file_name = 'membrane.mbd'
log_file = open('log.mbdyn', 'w')
process = Popen(['mbdyn', '-f', input_file_name],stdout=log_file,stderr=log_file)
process.stdin = ''

#path = 'case.sock'
host = ''
port = 0
timeout = -1
verbose = 1
data_and_next = 1
refnode = 0
nodes = 1
labels = 0 # 16
rot = 256 # for rotvec 256, rotmat 512, euler 1024; see mbc.h enum MBCType
accels = 0
#import ipdb; ipdb.set_trace()
#time.sleep(10)
for i in range(number_of_forces):
	path = 'case{}.sock'.format(i)
	print(path)
	nodal.append(mbcNodal(path, host, port, timeout, verbose, data_and_next, refnode, nodes, labels, rot, accels))
	
for i in range(number_of_forces):
	nodal[i].negotiate()
for i in range(number_of_forces):
	print(nodal[i].recv())
print("initialized")
#time.sleep(0.001)

while(True):
	force_tensor = np.random.uniform(low=0.4*10**-3,high=0.7*10**-6,size=(1,3))*0.
	for i in range(number_of_forces):
		nodal[i].n_f[:] = np.ravel(force_tensor)
		if nodal[i].send(False):
			exit('Something went wrong on send!')
			break
	for i in range(number_of_forces):
		if nodal[i].recv():
			exit('Something went wrong on recv!')
			break
	
	#print(np.reshape(nodal.n_x, (-1, 3)))
	
	for i in range(number_of_forces):
		if nodal[i].send(True):
			exit('Something went wrong on send!')
			break
	for i in range(number_of_forces):
		if nodal[i].recv():
			exit('Something went wrong on recv!')
			break

###Finalize
try:
	nodal.destroy()
	log_file.close()
except AttributeError:
	print('Warning: Could not close log file or destroy mbc.')
