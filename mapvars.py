#!/usr/bin/python
"""UMN Mapserver mapfiles parser with trivial variables support.

Usage mapvars.py mapfile.map.templ > mapfile.map
"""

import sys
import re

vars = {}

def variables(line):
	varname = line.split('=')[0].strip()
	varvalue = line.split('=')[1].strip()
	vars[varname] = varvalue

def parse_line(line):
	return (line % vars).rstrip()



if __name__ == '__main__':
	try:
		filename = sys.argv[1]
	except IndexError:
		print __doc__
		sys.exit(1)

	readvars = False

	file = open(filename, 'r')
	line = file.readline()
	while line:
		varline = False
		if re.match('STARTVAR', line.upper().strip()):
			readvars = True
			varline = True
		elif re.match('ENDVAR', line.upper().strip()):
			readvars = False
			varline = True

		#print readvars, varline, line
		if readvars == True and varline == False:
			if not line.strip().startswith('#'):
				variables(line)

		if readvars == False and varline == False:
			print parse_line(line)
		line = file.readline()
