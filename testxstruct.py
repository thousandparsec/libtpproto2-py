from datetime import datetime

from tp.netlib.xstruct import *

def now():
	"""\
	This function is needed because xstruct's representation is only accurate to the second
	"""
	time = datetime.now()
	return datetime(time.year, time.month, time.day, time.hour, time.minute, time.second)

def test_pack_upnack():
	"""\
	Tests whether packing then unpacking various data gives sane results
	"""
	tests = [
		#characters
		('c', ('a',)), ('cc', ('A', 'd')), ('c', ('\x00',)),
		('s', ('a',)), ('ss', ('A', 'd')), ('s', ('\x00',)),
		#8-bit integers
		('b', (1,)), ('bbbb', (0,-1,127,-128)),
		('B', (1,)), ('BBBB', (0,1,128,255)),
		#16-bit integers
		('h', (1,)), ('hhhh', (0,-1,32767,-32768)),
		('H', (1,)), ('HHHH', (0,1,32768,65535)),
		('n', (1,)), ('nnnn', (0,-1,32768,65534)),
		#32-bit integers
		('i', (1,)), ('iiii', (0,-1,2**31-1,-(2**31))),
		('I', (1,)), ('IIII', (0,1,2**16-1,2**32-1)),
		('j', (1,)), ('jjjj', (0,-1,2**16-1,2**32-2)),
		#64-bit integers
		('q', (1,)), ('qqqq', (0,-1,2**63-1,-(2**63))),
		('Q', (1,)), ('QQQQ', (0,1,2**16-1,2**64-1)),
		('p', (1,)), ('pppp', (0,-1,2**16-1,2**64-2)),
		#floats
		('f', (1.,)), ('ffff', (-2.**127, -2.**-149, 2.**-149, 2.**127)),
		('d', (1.,)), ('dddd', (-2.**1023, -2.**-1074, 2.**-1074, 2.**1023)),
		#timestamps
		('t', (now(),)), ('T', (now(),))
		]
	
	for i, j in tests:
		value = unpack(i, pack(i, *j))[0]
		assert value == j, "Packing and unpacking %s with %s, but got %s" % (j, i, value)

if __name__ == '__main__':
	test_pack_upnack()