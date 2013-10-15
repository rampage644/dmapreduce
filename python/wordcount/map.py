#!

import sys
import zmapreduce

import mapreduce


node_id = int(sys.argv[1].split('-')[1])
print sys.argv
print "map %d" % node_id

m = zmapreduce.Mapper(node_id)
m.map_fn = mapreduce.Map
m.reduce_fn = mapreduce.Reduce
m.combine_fn = mapreduce.Combine
m.comparator_fn = mapreduce.ComparatorHash
m.mritem_size = 24
m.hash_size = 8
m.start()