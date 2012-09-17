#!/usr/bin/env python
"""UMN Mapserver mapfiles parser with trivial variables support.

Usage: mapvars.py mapfile.map '<key>=<value>;<key>=<value>; ...'

Example: ./mapvars.py test.map.in "USER=MyUser; PASSWORD=MyPassword; SRID=4326; OUTLINECOLOR=100 100 100"
"""

import sys
import re


kvlocal = {}	# variables from mapfile
kvcmd = {}	# variables from command line

def set_var(kvline, kvstore='local'):
	""" Set variable to 'local' or 'cmd' key-value store. """

	key = kvline.split('=')[0].strip()
	value = kvline.split('=')[1].strip()

	if kvstore == 'local':
		kvlocal[key] = value
	else:
		kvcmd[key] = value

def get_line(line):
	""" Return line with variables substituted by values from key-value
	store. Values from 'cmd' key-value store always overrides values
	from 'local' one.
	"""

	kvstore = dict(kvlocal.items() + kvcmd.items())
	return (line % kvstore).rstrip()


if __name__ == '__main__':

	# open mapfile
	try:
		filename = sys.argv[1]
		mapfile = open(filename, 'r')
	except IndexError:
		print __doc__
		sys.exit(1)

	# read variables from command line
	try:
		for kvline in sys.argv[2].split(';'):
			set_var(kvline, 'cmd')
	except IndexError:
		pass

	varblock = False
	comment = False
	line = mapfile.readline()
	while line:
		if line.strip() != '':	# remove empty lines

			keyword = False
			comment = False

			if re.match('^STARTVAR', line.upper().strip()):
				keyword = True		# line contains variables declaration keyword
				varblock = True		# and marks beginning of variables declaration
			elif re.match('^ENDVAR', line.upper().strip()):
				keyword = True		# line contains variables declaration keyword
				varblock = False	# and marks end of variables declaration
			elif re.match('#', line.strip()):
				comment = True		# line is comment

			#print '>>>', line.strip(), keyword, varblock, comment

			# set variable if we are in variables declaration block or line is not comment
			if varblock and not keyword and not comment:
				set_var(line)

			# print line if we are not in variables declaration block or line is not comment
			elif not varblock and not keyword and not comment:
				print get_line(line)

		line = mapfile.readline()
