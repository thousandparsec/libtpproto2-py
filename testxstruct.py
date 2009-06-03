#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from tp.netlib.xstruct import *

def fails(function, *args):
	try:
		function(*args)
		return False
	except (TypeError, ValueError):
		return True

def test_pack_unpack():
	#these are all tuples of (structure, values, string representation)
	tests = [
		#characters
		('c', ['a'], 'a'),
		('c', ['\x00'], '\x00'),
		
		('s', ['a'], 'a'),
		('s', ['\x00'], '\x00'),
		
		#8-bit integers
		('b', [127], '\x7f'),
		('b', [-128], '\x80'),
		
		('B', [0], '\x00'),
		('B', [255], '\xff'),
		
		#16-bit integers
		('h', [-32768], '\x80\x00'),
		('h', [32767], '\x7f\xff'),
		
		('H', [0], '\x00\x00'),
		('H', [65535], '\xff\xff'),
		
		('n', [-1], '\xff\xff'),
		('n', [0], '\x00\x00'),
		('n', [65534], '\xff\xfe'),
		
		#32-bit integers
		('i', [-2**31], '\x80\x00\x00\x00'),
		('i', [2**31-1], '\x7f\xff\xff\xff'),
		
		('I', [0], '\x00\x00\x00\x00'),
		('I', [2**32-1], '\xff\xff\xff\xff'),
		
		('j', [-1], '\xff\xff\xff\xff'),
		('j', [2**32-2], '\xff\xff\xff\xfe'),
		
		#64-bit integers
		('q', [-2**63], '\x80\x00\x00\x00\x00\x00\x00\x00'),
		('q', [2**63-1], '\x7f\xff\xff\xff\xff\xff\xff\xff'),
		
		('Q', [0], '\x00\x00\x00\x00\x00\x00\x00\x00'),
		('Q', [2**64-1], '\xff\xff\xff\xff\xff\xff\xff\xff'),
		
		('p', [-1], '\xff\xff\xff\xff\xff\xff\xff\xff'),
		('p', [2**64-2], '\xff\xff\xff\xff\xff\xff\xff\xfe'),
		
		#floats
		('f', [-2.**127], '\xff\x00\x00\x00'),
		('f', [-2.**-149], '\x80\x00\x00\x01'),
		('f', [2.**-149], '\x00\x00\x00\x01'),
		('f', [2.**127], '\x7f\x00\x00\x00'),
		
		('d', [-2.**1023], '\xff\xe0\x00\x00\x00\x00\x00\x00'),
		('d', [-2.**-1074], '\x80\x00\x00\x00\x00\x00\x00\x01'),
		('d', [2.**-1074], '\x00\x00\x00\x00\x00\x00\x00\x01'),
		('d', [2.**1023], '\x7f\xe0\x00\x00\x00\x00\x00\x00'),

		#timestamps
		('t', [datetime.fromtimestamp(0)], '\x00\x00\x00\x00'),
		('T', [datetime.fromtimestamp(0)], '\x00\x00\x00\x00\x00\x00\x00\x00'),
		
		#lists
		('[]', [[]], '\x00\x00\x00\x00'),
		('[b]', [[0]], '\x00\x00\x00\x01\x00'),
		('[bb]', [[(0, 0), (0, 0)]], '\x00\x00\x00\x02\x00\x00\x00\x00'),
		
		#strings
		('S', [''], '\x00\x00\x00\x00'),
		('S', ['ab'], '\x00\x00\x00\x02ab'),
		('S', [u'Ж'], '\x00\x00\x00\x02\xd0\x96'), #CYRILLIC CAPITAL LETTER ZHE
		('S', [u'中'], '\x00\x00\x00\x03\xe4\xb8\xad'), #HAN IDEOGRAPH
		('S', [u'\U00010346'], '\x00\x00\x00\x04\xf0\x90\x8d\x86') #GOTHIC LETTER FAIHU
		
		
		]
	
	for structure, values, string in tests:
		assert pack(structure, *values) == string,\
			"Packing %s with %s should have given %r, but instead gave %r" % (values, structure, string, pack(structure, *values))
		assert unpack(structure, string)[0] == tuple(values),\
			"Unpacking %r with %s should have given %s, but instead gave %s" % (string, structure, tuple(values), unpack(structure, *values)[0])
		assert unpack(structure, pack(structure, *values))[0] == tuple(values),\
			"Packing and unpacking %s with %s, but got %s" % (tuple(values), structure, unpack(structure, pack(structure, *values))[0])
		#we need to store this in a variable to use the unpack operator
		t = unpack(structure, string)[0]
		assert pack(structure, *t) == string,\
			"Unpacking and packing %s with %s, but got %s" % (string, structure, pack(structure, *t))
	
	
	#tuples of (structure, values) which should cause an exception to be thrown when passed to pack
	failureTests = [
		#characters
		('c', []),
		('c', [392]),
		('c', [u'中']),
		
		('s', [392]),
		('s', [u'中']),
		
		#8-bit ints
		('b', ['']),
		('b', [1024.]),
		('b', [-129]),
		('b', [128]),
		
		('B', ['']),
		('B', [1024.]),
		('B', [-1]),
		('B', [256]),
		
		#16-bit ints
		('h', ['']),
		('h', [1024.]),
		('h', [-32769]),
		('h', [32768]),
		
		('H', ['']),
		('H', [1024.]),
		('H', [-1]),
		('H', [65536]),
		
		('n', ['']),
		('n', [1024.]),
		('n', [-2]),
		('n', [65535]),
		
		#32-bit ints
		('i', ['']),
		('i', [1024.]),
		('i', [-2**31-1]),
		('i', [2**31]),
		
		('I', ['']),
		('I', [1024.]),
		('I', [-1]),
		('I', [2**32]),
		
		('j', ['']),
		('j', [1024.]),
		('j', [-2]),
		('j', [2**32-1]),
		
		#64-bit ints
		('q', ['']),
		('q', [1024.]),
		('q', [-2**63-1]),
		('q', [2**63]),
		
		('Q', ['']),
		('Q', [1024.]),
		('Q', [-1]),
		('Q', [2**64]),
		
		('p', ['']),
		('p', [1024.]),
		('p', [-2]),
		('p', [2**64-1]),
		
		#floats
		('f', ['']),
		
		('d', ['']),
		
		#timestamps
		('t', ['']),
		
		('T', ['']),
		
		#lists
		('[]', [1]),
		
		#strings
		('S', [1]),
		('S', [.5]),
		('S', []),
		]
		
	for structure, values in failureTests:
		assert fails(pack, structure, *values), "Packing %s into %s should raise an exception, but it did not." % (values, structure)

if __name__ == '__main__':
	test_pack_unpack()