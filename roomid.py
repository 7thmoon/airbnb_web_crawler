import requests
import sys
import time
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# get the last page of search result
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
	#arr.sort()
	return max(arr)

# get the room id on each page
def get_roomId_pasePage(url):	
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	arr = []
	for div in soup.find_all('div', attrs={'class':'col-sm-12 row-space-2 col-md-6'}):
		tmp = div.find('div')['data-url']
		arr.append(tmp)
	return arr
	
#get the room list based on search criteria and page limits
def roomId_list(searhPage_url, pages):
	page = "";
	res = [];
	for i in range(1, pages + 1):
		Page_url = searhPage_url + "&page=" + str(i)
		for j in get_roomId_pasePage(searhPage_url):
			res.append(j)
	return res

		










