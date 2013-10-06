#!
import os
import sys
import ztest

def ComparatorHash(h1, h2):
	return h1 > h2

def Reduce(buffer):
	for i in xrange(buffer.count()):
		sys.stdout.write(buffer.key(i))
		sys.stdout.write(buffer.value(i))
	return 0

TERASORT_RECORD_SIZE = 100

def Map(data, size, last_chunk, buffer):
	position = 0
	while position < size:
		buffer.append(data, position, TERASORT_RECORD_SIZE)
		position += TERASORT_RECORD_SIZE
	return position