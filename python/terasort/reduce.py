#!

import sys
import zmapreduce

import mapreduce

node_id = int(sys.argv[1].split('-')[1])

r = zmapreduce.Reducer(node_id)
r.map_fn = mapreduce.Map
r.reduce_fn = mapreduce.Reduce
r.comparator_fn = mapreduce.ComparatorHash
r.mritem_size = 28
r.hash_size = 10
r.start()