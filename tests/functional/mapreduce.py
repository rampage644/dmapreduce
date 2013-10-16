#!
import zmapreduce

def ComparatorHash(h1, h2):
	return h1 > h2

def Reduce(buffer):
	import os, sys
	# buffered write, buf size is 100K
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0x10000)
	write = sys.stdout.write
	for record in buffer:
		write("%s%s" % (record.key, record.value))
	return 0

def Map(data, size, last_chunk, buffer):
	position = 0
	tr_size =  100
	h_size = 10
	for position in xrange(0, size, tr_size):
		buffer.append_record(
			data[position:position+h_size],
			data[position+h_size:position+tr_size],
			data[position:position+h_size])
	return size