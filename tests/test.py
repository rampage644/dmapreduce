#!

import os, sys
import unittest
import zmapreduce

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
		for i in xrange(1, 5):
			r = buffer.append()
			r.key = ('word%d' % i) * i
			r.value = '1'	
		
		for i in xrange(2, 6):
			self.assertEqual(buffer[i].key, ('word%d' % (i-1)) * (i-1))
			self.assertEqual(len(buffer[i].key), 5*(i-1))


		
if __name__ == "__main__":
    unittest.main()
    
