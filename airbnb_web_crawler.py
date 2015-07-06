import os
import requests
import sys
import time
from bs4 import BeautifulSoup
import requests
import csv
import unicodedata
from datetime import datetime
from roomid import *


# this scipt is to extract the information about the list on airbnb given by search criteria
if len(sys.argv) == 1:
	print "Usage: " +  sys.argv[0] + " search_criteria page_limits"
	sys.exit(1) 
#search criteria
criteria = sys.argv[1]
searh_page_url="https://www.airbnb.com/s/" + criteria 
base_url="https://www.airbnb.com"
try:
	page_number = int(last_page(searh_page_url))
except:
	print "fail to get last page number"
	sys.exit(1)

page_limits = page_number
if len(sys.argv) > 2:
	try:
		threshold = int(sys.argv[2])
		if page_limits > threshold:
			page_limits = threshold
	except:
		print "invalid page limits"
		sys.exit(1) 


last_page = last_page(searh_page_url)

price_pattern = {
    'day_l': 'price_amount',
    'day_h': 'price_amount',
    'week_l': 'weekly_price_string',
    'week_h': 'weekly_price_string',
    'month_l': 'monthly_price_string',
    'month_h': 'monthly_price_string',
}
 
address_pattern = {
    'address': 'display-address',
    'zip-code': None,
    }
 
def get_price_from_airbnb(pattern, html):
    price={}    
    for name, id in pattern.iteritems():
        try:
            price[name]=html.find(id=id).get_text(strip=True)
        except:
            price[name]=None
    return price

def get_userId_from_airbnb(html):
	r = None
	try:
		url = html.find('li', attrs={'class':'user-image'}).find('a')['href']
		r = url.split('/')[3]
	except:
		pass
	return r

def get_name_from_airbnb(html):
    r = None
    try:
		r = html.find(id='listing_name').get_text(strip=True)
		#if isinstance(r, unicode):
		#	unicodedata.normalize('NFKD', r).encode('ascii','ignore')
    except:
        pass
    return r
 
def get_address_from_airbnb(html):
    address = {
               'address': None,
               'zip-code': None
               }
    try:
        a = html.find(id='display-address')['data-location']
        if a[-13:]=='United States':
			address['address']=a
    except:
        pass
    return address
 
def get_rating_from_airbnb(html):
    rating={'reviews': None,
            'rating': None}
	
    try:
		spans = html.find_all('span', attrs={'itemprop':'reviewCount'})
		for span in spans:
			try:
				num = int(span.string)
				rating['reviews'] = num
				break
			except:
				pass
    except:
        pass
		
    try:
        if rating['reviews']>0:
			rating['rating']= float(html.find('meta', attrs={'property':'airbedandbreakfast:rating'})['content'])
    except:
        pass
    return rating

#only a code sample; not applicable
def get_accommodates_from_airbnb(html):
    r = None
    try:
        for td in html.find(id='description_details').find_all('td'):
            if td.string == 'Accommodates:':
                r = int(td.parent.find_all('td')[1].string)
    except:
        pass
    return r
 
def get_bedrooms_from_airbnb(html):
    r = None
    try:
		divs = html.find_all('div', attrs={'class':'col-md-6'})
		for div in divs:
			for sub_div in div.find_all('div'):
				if sub_div.contents[0] == "Bedrooms: ":
					r = sub_div.strong.string
					break
    except:
        pass
    return r
 
def get_bathrooms_from_airbnb(html):
    r = None
    try:
        for td in html.find(id='description_details').find_all('td'):
            if td.string == 'Bathrooms:':
                r = int(td.parent.find_all('td')[1].string)
    except:
        pass
    return r

class Room:
	def __init__(self, roomId):
		self.id=roomId.split('/')[2].split('?')[0]
		room_url = base_url + roomId
		r = requests.get(room_url)
		soup = BeautifulSoup(r.text)
		self.userId = get_userId_from_airbnb(soup)
		#self.name=get_name_from_airbnb(soup)
		#self.rating=get_rating_from_airbnb(soup)
		#self.price=get_price_from_airbnb(price_pattern, soup)
		#self.address=get_address_from_airbnb(soup)
		#self.rooms=get_bedrooms_from_airbnb(soup)
		#self.updated=datetime.now()

		
def convertToCSV(room):
	f = open(filename, 'a')
	try:
		f.write(str(room.id))
		f.write(',')
		f.write(str(room.userId))
		#f.write(str(room.rating.get('rating')))
		#f.write(',')
		#f.write(str(room.rating.get('reviews')))
		#f.write(',')
		#f.write(str(room.price.get('day_l')))
		#f.write(',')
		#f.write(str(room.rooms))
		#f.write(',')
		#f.write(str(room.updated))
		#f.write(',')
		#f.write(str(room.name.encode('utf-8')))
		f.write('\n')
	except:
		attrs = vars(room)
		f = open(errorlog, 'a')
		stream = ', '.join("%s: %s" % item for item in attrs.items()).encode('utf8')
		f.write(stream)
		f.write('\n')
		f.close
		pass
	f.close()
	
filename = criteria + '.csv'
errorlog=  criteria + '.err'
f = open(filename, 'wb')
#f.write("id,rating,reviews,daily_price,bedrooms,update_time,name,address\n")
f.close()
f = open(errorlog, 'wb')
f.close()
for roomId in roomId_list(searh_page_url, page_limits):
	r = Room(roomId)
	attrs = vars(r)
	print ', '.join("%s: %s" % item for item in attrs.items())
	convertToCSV(r)

if len(open(errorlog).readlines()) == 0:
	os.system("rm " + errorlog)

	
	

