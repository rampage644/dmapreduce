#!/usr/bin/python

with open('report.txt') as f:
	input = f.read()

lines = input.splitlines()
for index, pos in enumerate((3,9)):
	sys, user = input.splitlines()[pos].split()[:2]
	print "%d: node time is %.2f (%s, %s)" % (index+1, float(sys) + float(user), sys, user)