#!

import sys
import zmapreduce
import mapreduce

node_id = int(sys.argv[1].split('-')[1])

m = zmapreduce.Mapper(node_id)
m.map_fn = mapreduce.Map
m.reduce_fn = mapreduce.Reduce
m.comparator_fn = mapreduce.ComparatorHash
m.mritem_size = 28
m.hash_size = 10
m.start()