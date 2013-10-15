#!
import os
import sys
import _zmapreduce

import hashlib

def hashf(s):
	return hashlib.md5(s).hexdigest()

def ComparatorHash(h1, h2):
	return h1 > h2

def Reduce(buffer):
	for record in buffer:
		print "[%s] %s = %s" % (
			record.hash, record.key, record.value)
	return 0

def Map(data, size, last_chunk, buffer):
	string = data.tobytes()
	for word in string.split():
		r = buffer.append()
		r.key = word
		r.value = "1"
		r.hash = hashf(word)
	return len(string)

# def Combine(input, output):
# 	for record in input:
# 		r = output.append()
# 		r.key = record.key
# 		r.value = record.value
# 		r.hash = record.hash

def Combine(input, output):
	pr = input[0]
	count = 1
	for i in xrange(1, len(input)):
		r = input[i]
		if r.hash != pr.hash:
			nr = output.append()
			nr.key = pr.key
			nr.value = str(count)
			nr.hash = pr.hash
			count = 1
			pr = r
		else:
			count += int(r.value)
	# append last
	nr = output.append()
	nr.key = r.key
	nr.hash = r.hash
	nr.value = str(count)