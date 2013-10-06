#!
import os
import sys
import ztest

def ComparatorHash(h1, h2):
	return h1 > h2

def Reduce(buffer):
	for record in buffer:
		sys.stdout.write(record.key)
		sys.stdout.write(record.value)
	return 0

TERASORT_RECORD_SIZE = 100
HASH_SIZE = 10

def Map(data, size, last_chunk, buffer):
	position = 0
	while position < size:
		record = buffer.append()
		record.key = data[position:position+HASH_SIZE]
		record.value = data[position+HASH_SIZE:position+TERASORT_RECORD_SIZE]
		position += TERASORT_RECORD_SIZE
	return position