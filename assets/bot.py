from .utils import *
from .constants import voyage, guests
from .hook import hook
from selenium import webdriver
import re
import sys

clean()

profile = profile()
driver = webdriver.Firefox(firefox_profile=profile)

voyage_link = voyage
driver.get(voyage_link) #Visits the landing page
message('Made a request [Voyage Landing Page] -> {}'.format(voyage_link))

voyage_info = driver.find_element_by_class_name('md-hidden') #Finds the Select Room button
voyage_info.click()

session_link = driver.current_url

message('New session link created -> {}'.format(session_link))

guests_validator = re.match('^[-+]?[0-4]+$', guests)

if not guests_validator:
	error('Guests is not [1-4]')
	sys.exit()
else:
	stateroom_xpath = '//button[@data-num-pax="{}"]'.format(guests)

driver.find_element_by_xpath(stateroom_xpath).click()
time.sleep(5)

element = driver.find_element_by_xpath('//section[@id="stateroom-meta"]').get_attribute('innerHTML')
stateroom_element = htmlmin.minify(element, remove_empty_space=True)
message('Analyzing State Room data.')

if stateroom_element.count('Sold Out') == 5:
	message('Analyzing Data Finished -> All Rooms Sold Out')
else:
	message('Analyzing Data Finished -> A Room is Available')
	hook()

message('Running again -> -10 mins.')
time.sleep(600)
os.system('python3 launcher.py')
