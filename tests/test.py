#!

import os, sys
import unittest
import hashlib
import _zmapreduce

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
		_zmapreduce.hash(8)

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

class BasicTestCase(unittest.TestCase):
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
		r =  buffer.append()
		self.assertIsNotNone(r)
		self.assertEqual(len(buffer), 1)
		r.key = data[:10]
		r.value = data[10:100]

		# now check
		self.assertEqual(buffer[0].key, data[:10])
		self.assertEqual(buffer[0].value, data[10:100])

	def testBufferAppendingWithString(self):
		r = buffer.append()
		self.assertIsNotNone(r)
		KEY = b'abc'
		VALUE = b'abcdefghijklmnopqrstuvwxyz'
		r.key = KEY
		r.value = VALUE
		self.assertEqual(len(buffer), 2)
		self.assertEqual(buffer[1].key, KEY)
		self.assertEqual(buffer[1].value, VALUE)


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
		data = r'qwertyuiop[]asdfghjkl;zxcvbnm,./1234567890-='
		mv = memoryview(data)

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

	def testSettingHashSize(self):
		_zmapreduce.hash(10)
		_zmapreduce.hash(4)

	def testHashValues(self):
		# setting size of hash to 4 bytes
		_zmapreduce.hash(4)

		r = buffer.append()
		r.hash = r'qwer'

		self.assertEquals(r.hash, r'qwer')
		self.assertNotEquals(r.hash, r'qwe')

		r.hash = r'qwertyuiop[]'
		self.assertEquals(r.hash, r'qwer')
		self.assertNotEquals(r.hash, r'qwertyuiop[]')

		# bytes
		_zmapreduce.hash(10)
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
		data = r'qwertyuiop[]asdfghjkl;zxcvbnm,./1234567890-='
		mv = memoryview(data)
		_zmapreduce.hash(4)

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
	
		
if __name__ == "__main__":
    unittest.main()
    
