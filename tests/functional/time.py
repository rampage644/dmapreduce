#!/usr/bin/python

with open('report.txt') as f:
	input = f.read()

lines = input.splitlines()
for index in (0,1):
	sys, user = lines[3+6*index].split()[2:4]
	program = lines[5+6*index].split('/')[-1].split('.')[0]
	print "%s: node time is %.2f (%s, %s)" % (program, float(sys) + float(user), sys, user)