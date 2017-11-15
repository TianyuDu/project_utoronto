import selenium
import time
import datetime
import numpy as np
import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
from typing import List

from constants import *
from basic import *
from utoronto_web import *
from google_map_web import *

def initialize() -> None:
	print('=======Initializing=======')
	print('Fetching Essential Information...')
	opt = str(input('Update local building list file from internet?[y/n] >> '))
	if opt.lower() == 'y':
		print('Now fetching building list from {0:s}'.format(ut_building_list_URL))
		generate_building_list(building_list_DIR)
		print('Done')
		web = selenium.webdriver.Chrome()
		subject_area_list = generate_subject_areas(web, ut_subject_area_URL, subject_area_url_DIR)
		generate_course_lis(web, subject_area_list, course_list_DIR)


	elif opt.lower() == 'n':
		print('Skipped.')

	print('Creating Global Variables...')
	print('Done.')
	global abbr2full, full2abbr
	global abbr2postal, postal2abbr
	global source_collection
	abbr2full = generate_abbr2full(building_list_DIR)
	abbr2postal = generate_abbr2postal(building_list_DIR)
	full2abbr = dict((v, k) for k, v in abbr2full.items())
	postal2abbr = dict((v, k) for k, v in abbr2postal.items())
	source_collection = [abbr2full, full2abbr, abbr2postal, postal2abbr]
	print('Loading Essential Information...')
	print('Done.')

if __name__ == '__main__':
	result = parallel_walk_info(0, 3, source_collection, Nthread=4)
	print(result)
