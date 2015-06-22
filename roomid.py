import requests
import sys
import time
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def last_page(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	arr = []
	for li in soup.find('div', attrs={'class':'pagination pagination-responsive'}).find_all('li'):
		a = li.find('a')
		if a != None :
			try:
				num = int(a.string)
				arr.append(num)
			except:
				pass
	arr.sort()
	return arr[-1]

def get_roomId_pasePage(url):	
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	arr = []
	for div in soup.find_all('div', attrs={'class':'col-sm-12 row-space-2 col-md-6'}):
		tmp = div.find('div')['data-url']
		arr.append(tmp)
	return arr
	

def roomId_list(criteria, maximum):
	page = "";
	searhPage_url="https://www.airbnb.com/s/" + criteria + "?ss_id=i4wdsv9i"
	
	last = last_page(searhPage_url)
	if last > maximum:
		last = maximum
	res = [];
	for i in range(1, last + 1):
		Page_url="https://www.airbnb.com/s/" + criteria + "?ss_id=i4wdsv9i&page=" + str(i)
		for j in get_roomId_pasePage(Page_url):
			res.append(j)
	return res

		










