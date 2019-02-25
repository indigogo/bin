#!/usr/local/bin/python

import argparse
from argparse import ArgumentParser
import sys
import os
import re
from selenium import webdriver

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument( '-file', type = str, default = 'file', required = True, help = 'input file' )
#	parser.add_argument( '-option', type = str, default = 'a', choices = [ 'a', 'b', 'c' ], help = 'option' )
#	parser.add_argument( '-options', type = str, nargs = '+', help = 'options list' )
	args = parser.parse_args()

	filename = args.file

chromedriver = '/Users/indigo/git/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('https://members.wework.com/login')

email = driver.find_element_by_css_selector('#email_input')
email.send_keys('indigo@cyrusbio.com')
password = driver.find_element_by_css_selector('#password_input')                             
password.send_keys('1qweqweqwe')
password.submit()

driver.find_element_by_link_text('Book a Room').click()

#unfortunately the below DNE
 driver.find_element_by_css_selector('#results-section > div.results-list.rows > div.result-rows.ng-scope > div > div > div:nth-child(13) > div > div.ng-scope > div > div.bd > ul.slots.unstyled > li:nth-child(19) > div')
