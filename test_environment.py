import google_map_web
import selenium
from constants import *
from selenium import webdriver

#driver = webdriver.Chrome()
#driver.get(google_map_URL)

start = ['BA', 'MS', 'MP', 'SS', 'WW']
end = start

result = google_map_web.parallel_walk_info(start, end, nthread=4)

end = start

#driver.close()
