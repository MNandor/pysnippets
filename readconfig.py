#!/bin/python3

import os

def readconfig(file):
	config = {}
	with open(file, 'rt') as ifs:
		lines = ifs.readlines()
	for line in lines:
		line = line.strip()
		# Comments
		if line.startswith('#') or line =='':
			continue

		if line.count('=') != 1:
			print('Wrongly formatted line:')
			print(line)

		line = line.split('=')

		config[line[0]] = line[1]
	
	return config

	

readConfig=readconfig

