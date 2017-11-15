import numpy as np
import time
import multiprocessing
import itertools

def testfunction(arg1: int, arg2: str, threadID: int):
	result = arg1 + arg2 + np.random.rand()
	print('Thread Number:{0:d}, result: {1:f}'.format(threadID, result))
	return result

if __name__ == '__main__':
	RUN_PERIOD = 100
	with multiprocessing.Pool(processes=16) as p:
		start = time.clock()
		input_list = [(1,2,000)] * RUN_PERIOD
		result = p.starmap(testfunction, input_list)
		print('Multi Processing: Time taken: {0:f} seconds'.format(time.clock() - start))
		print(input_list)
