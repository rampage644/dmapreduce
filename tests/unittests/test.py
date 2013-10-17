#!

import os, sys
import unittest
import hashlib
import gc

import zmapreduce
import _zmapreduce

def howmany(cls):
	return len([x for x in gc.get_objects() if isinstance(x,cls)])


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

class MapReduceFunctionsTestCase(unittest.TestCase):
	def testCombine(self):
		input_count = 0
		output_count = 0
		buffer.clear()
		obuffer.clear()
		_zmapreduce._module_set_callbacks(None,
                                  None,
                                  None,
                                  None,
                                  0,
                                  8)

		with open('/dev/input.txt') as input_file:
			for line in input_file:
				line = line.strip()
				r = buffer.append()
				r.key = line
				r.value = "1"
				r.hash = hashlib.md5(line).hexdigest()

		Combine(buffer, obuffer)

		self.assertNotEqual(len(buffer), 
			len(obuffer))

		for r in obuffer:
			output_count += int(r.value)

		for r in buffer:
			input_count += int(r.value)

		self.assertEqual(input_count, 
			output_count)

class ZMapReduceModuleTest(unittest.TestCase):
	def testNodeFailedStart(self):
		n = zmapreduce.Node(0)
		with self.assertRaises(NotImplementedError):
			n._do_init()
		with self.assertRaises(NotImplementedError):
			n._do_init()
		with self.assertRaises(NotImplementedError):
			n.start()


	def testMapNodeInit(self):
		m = zmapreduce.Mapper(1)
		m.map_fn = lambda x: x
		m.reduce_fn = lambda x: x
		m.comparator_fn = lambda : True
		m.mritem_size = 28
		m.hash_size = 8
	
	def testReduceNodeInit(self):
		r = zmapreduce.Reducer(1)
		r.map_fn = lambda x: x
		r.reduce_fn = lambda x: x
		r.comparator_fn = lambda : True
		r.mritem_size = 28
		r.hash_size = 8
		r._do_init()

class ZMapReduceCExtensionTest(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testDataPresense(self):
		self.assertIsNotNone(data)
	
	def testDataInput(self):
		# check first 10 bytes
		for i in xrange(10):
			self.assertEqual(data[i], chr(i + 48))

	def testBufferPresense(self):
		self.assertIsNotNone(buffer)

	def testBufferConstructionRejection(self):
		with self.assertRaises(Exception):
			b = ztest.Buffer()

	def testBufferAppending(self):
		buffer.clear()
		r =  buffer.append()
		self.assertIsNotNone(r)
		self.assertEqual(len(buffer), 1)
		r.key = data[:10]
		r.value = data[10:100]

		# now check
		self.assertEqual(buffer[0].key, data[:10])
		self.assertEqual(buffer[0].value, data[10:100])

	def testBufferAppendingWithString(self):
		buffer.clear()
		r = buffer.append()
		self.assertIsNotNone(r)
		KEY = b'abc'
		VALUE = b'abcdefghijklmnopqrstuvwxyz'
		r.key = KEY
		r.value = VALUE
		self.assertEqual(len(buffer), 1)
		self.assertEqual(buffer[0].key, KEY)
		self.assertEqual(buffer[0].value, VALUE)

	def testBufferAppendingWithWrongArg(self):
		buffer.clear()
		r = buffer.append()

		with self.assertRaises(TypeError):
			r.key = 1

		with self.assertRaises(TypeError):
			r.hash = 1

		with self.assertRaises(TypeError):
			r.value = 1

		with self.assertRaises(TypeError):
			buffer.append_record(None, None, None)

	def testBufferFailWrongIndex(self):
		with self.assertRaises(IndexError):
			r = buffer[100]

	def testStringKeyValues(self):
		buffer.clear()

		for i in xrange(5):
			r = buffer.append()
			r.key = ('word%d' % i) * i
			r.value = '1'	
		
		for i in xrange(5):
			self.assertEqual(buffer[i].key, ('word%d' % (i)) * (i))
			self.assertEqual(len(buffer[i].key), 5*(i))

	def testOutputBufferPresense(self):
		self.assertIsNotNone(obuffer)

	def testInputToOutputBuffer(self):
		buffer.clear()
		obuffer.clear()

		for i in xrange(1, 5):
			r = buffer.append()
			r.key = ('word%d' % i) * i
			r.value = '1'	


		for record in buffer:
			r = obuffer.append()
			r.key = record.key
			r.value = record.value

		for i in xrange(len(buffer)):
			self.assertEqual(buffer[i].key, obuffer[i].key)
			self.assertEqual(buffer[i].value, obuffer[i].value)

	def Combine(self, input, output):
		key = input[0].key
		count = 1
		for i in xrange(1, len(input)):
			r = input[i]
			if r.key != key:
				nr = output.append()
				nr.key = r.key
				nr.value = str(count)
				nr.hash = r.hash
				count = 0
				hash = r.hash
			count += int(r.value)

	def testBufferClear(self):
		self.assertGreater(len(buffer), 0)
		buffer.clear()
		self.assertEquals(len(buffer), 0)

	def testBufferMemoryViewAndStringsEquals(self):
		# create test memoryview, buffer is memoryview
		rdata = r'qwertyuiop[]asdfghjkl;zxcvbnm,./1234567890-='
		mv = memoryview(rdata)

		buffer.clear()
		r1 = buffer.append()
		r1.key = mv[:5]
		r1.value = mv[5:10]

		r2 = buffer.append()
		r2.key = r'qwert'
		r2.value = r'yuiop'

		self.assertEquals(r1.key, r2.key)
		self.assertEquals(r1.value, r2.value)

		self.assertIsNot(r1.key, r2.key)
		self.assertIsNot(r1.value, r2.value)

	def testHashValues(self):
		# setting size of hash to 4 bytes
		# a tricky hack to set hash size to 4 bytes
		_zmapreduce._module_set_callbacks(None,
                                  None,
                                  None,
                                  None,
                                  0,
                                  4)

		r = buffer.append()
		r.hash = r'qwer'

		self.assertEquals(r.hash, r'qwer')
		self.assertNotEquals(r.hash, r'qwe')

		r.hash = r'qwertyuiop[]'
		self.assertEquals(r.hash, r'qwer')
		self.assertNotEquals(r.hash, r'qwertyuiop[]')

		# bytes
		_zmapreduce._module_set_callbacks(None,
                                  None,
                                  None,
                                  None,
                                  0,
                                  10)
		r = buffer.append()
		r.hash = r'1234567890'

		self.assertEquals(r.hash, r'1234567890')
		self.assertNotEquals(r.hash, r'123')

		r.hash = r'1234567890qwertyuiop'
		self.assertEquals(r.hash, r'1234567890')
		self.assertNotEquals(r.hash, r'1234567890qwertyuiop')

		r.hash = r'123456'
		self.assertNotEquals(r.hash, r'123456')

	def testHashValuesFromMemoryView(self):
		rdata = r'qwertyuiop[]asdfghjkl;zxcvbnm,./1234567890-='
		mv = memoryview(rdata)
		_zmapreduce._module_set_callbacks(None,
                                  None,
                                  None,
                                  None,
                                  0,
                                  4)

		buffer.clear()
		r1 = buffer.append()
		r1.hash = mv[:4]

		self.assertEquals(r1.hash, r'qwer')

	def testIteratingOverEmptyBuffer(self):
		buffer.clear()

		for record in buffer:
			pass

		# reduce(lambda input_count, record: input_count += int(record.value), buffer)
		# self.assertEqual(input_count, 0)

	def testBufferAppendingRecordMemoryView(self):
		buffer.clear()
		self.assertEquals(len(buffer), 0)

		buffer.append_record(
			data[:10],
			data[10:100],
			data[:8])

		self.assertEquals(len(buffer), 1)

		# now check
		self.assertEqual(buffer[0].key, data[:10])
		self.assertEqual(buffer[0].value, data[10:100])
		self.assertEqual(buffer[0].hash, data[:8])

		r = buffer[0]
		self.assertEqual(r.key, data[:10])
		self.assertEqual(r.value, data[10:100])
		self.assertEqual(r.hash, data[:8])



	def testBufferAppendingRecordString(self):
		buffer.clear()
		self.assertEquals(len(buffer), 0)

		buffer.append_record(
			r'0123456789',
			r'qwertyuiop[]asdfghjkl;zxcvbnm',
			r'11111111')

		self.assertEquals(len(buffer), 1)

		# now check
		self.assertEqual(buffer[0].key, r'0123456789')
		self.assertEqual(buffer[0].value, r'qwertyuiop[]asdfghjkl;zxcvbnm',)
		self.assertEqual(buffer[0].hash, r'11111111')

		r = buffer[0]
		self.assertEqual(r.key, r'0123456789')
		self.assertEqual(r.value, r'qwertyuiop[]asdfghjkl;zxcvbnm',)
		self.assertEqual(r.hash, r'11111111')

class ZMapReduceRefCountTest(unittest.TestCase):
	def testInputsFromCcode(self):
		# refcount == 2 cause we're creating temporary object as getrefcount argument!
		self.assertEquals(sys.getrefcount(buffer), 2)
		self.assertEquals(sys.getrefcount(obuffer), 2)
		self.assertEquals(sys.getrefcount(data), 2)


	def testRecordCreation(self):
		r = buffer.append()
		r.hash = r'012345'
		r.key = r'09876'
		r.value = r'zxcvbnm'

		k,v,h = r.key, r.value, r.hash
		self.assertEquals(sys.getrefcount(r), 2)
		# only temp object should count
		self.assertEquals(sys.getrefcount(r.key), 1)
		self.assertEquals(sys.getrefcount(r.value), 1)
		self.assertEquals(sys.getrefcount(r.hash), 1)

		
if __name__ == "__main__":
	# have to do such thing, cause we're using pymain from custom c code
	# unittest.main() throws SystemExit exception, leaving source executable
	# with memory leaks and unfreed resources
	try:
		unittest.main()
	except BaseException as e:
		pass
 	  
