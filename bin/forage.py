#!/usr/bin/python -O

import sys
from codecs import open

def extract(fname):
	print(fname)
	try: f = open(fname)
	except:
		print('Unable to open ' + fname)
		return
	for l in f:
		if not l: continue
		for x in l.split('href=')[1:]:
			if x[0] == '"': x = x[1:].split('"', 1)[0]
			else: x = x.split()[0]
			print(x)
	f.close()

def main(argv=None):
	for fname in sys.argv[1:]:
		extract(fname)

if __name__ == "__main__": main() 
