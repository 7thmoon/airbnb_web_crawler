import os
import sys
import re

# this script is to get the total list on airbnb given by a city list
# the city list includes city name and state, which is separated by '\t'
# we can choose the number of cities to search from the top of the list 
if len(sys.argv) == 1:
	print "Usage: " +  sys.argv[0] + " city_list_file city_number"
	sys.exit(1)
	
city_cfg = sys.argv[1]
crawler_script = "airbnb_web_crawler.py"
if os.path.exists(crawler_script) == False or os.path.exists(city_cfg) == False:
	print "web_crawler script or city list config file doesn't exist in current dir"
	sys.exit(1)


city_number = len(open(city_cfg).readlines())
if city_number == 0 :
	print "city cfg file is empty"
	sys.exit(1)
	
if len(sys.argv) > 2:
	try:
		max = int(sys.argv[2])
		if max < city_number:
			city_number = max
	except:
		print "invalid city number"
		sys.exit(1) 
	

complete_file = city_cfg + ".complete"
error_log = city_cfg + ".err"

if os.path.exists(complete_file) == False :
	f = open(complete_file, 'wb')
	f.close()

if os.path.exists(error_log) == False :
	f = open(error_log, 'wb')
	f.close()
	
complete_number = len(open(complete_file).readlines())
if complete_number == city_number :
	print "task is completed for"  + city_cfg
	sys.exit(0)

lines = [line.rstrip('\r\n') for line in open(city_cfg)]
for l in lines[0:city_number]:
	city = l.split('\t')[0]
	try:
		state = l.split('\t')[1]
	except:
		state = ""
	s = city + '--' + state
	search_criteria = s.replace(' ', '-')
	print search_criteria
	found = False
	for line in open(complete_file, 'r'):
		if re.search(search_criteria ,line):
			found = True
			break
	if found == True:
		break
		
	try:	
		os.system("python " + crawler_script + " " + search_criteria)
		f = open(complete_file, 'a')
		f.write(search_criteria + '\n')
		f.close()
	except:
		f = open(error_log, 'a')
		f.write(search_criteria + '\n')
		f.close()
		
complete_number = len(open(complete_file).readlines())
if complete_number == city_number :
	print "Task is completed for "  + city_cfg
	os.system("rm " + complete_file)
	os.system("rm " + error_log)
	sys.exit(0)
else:
	print "Task uncompleted for"  + city_cfg + ". Please check " + error_log
	sys.exit(1)