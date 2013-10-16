#!

import sys
import zmapreduce
import mapreduce
import gc

sys.setcheckinterval(1000)
node_id = int(sys.argv[1].split('-')[1])

m = zmapreduce.Mapper(node_id)
m.map_fn = mapreduce.Map
m.reduce_fn = mapreduce.Reduce
m.mritem_size = 28
m.hash_size = 10
m.start()