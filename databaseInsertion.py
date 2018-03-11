import urllib2
import json
import MySQLdb


#Connect to database
def dbConnect(sql):
    db = MySQLdb.connect(host="localhost",user="archana", passwd="archana",db="events",charset = 'utf8', use_unicode = True)
    cur = db.cursor()
    cur.execute(sql)
    db.commit()


#Insert the 311 data to event_data table
def dbinsert(case_id, opened, updated, closed, status, category, responsible_agency, request_type, request_details,
             address, latitude, longitude ):
    sql = "INSERT INTO event_data (case_id, opened, updated, closed, status, category, responsible_agency, request_type," \
          "request_details, address, latitude, longitude) VALUES " \
          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (case_id, opened, updated,closed, status, category, responsible_agency, request_type, request_details, address,
             latitude, longitude)
    dbConnect(sql)

#Get the data from 311
req = urllib2.Request('https://data.sfgov.org/resource/vw6y-z8j6.json')
opener = urllib2.build_opener()
f = opener.open(req)
data = json.loads(f.read())
actual_data = list()
for length in range(len(data)):
    if len(data[length]) == 0:
        continue
    else:
        actual_data.append(data[length])

#Retrieve the required data from json data fetched from the 311 and call the function dbInsert to insert the data into the table event_data
for line in actual_data:
    category = line['category']
    case_id = line['case_id']
    opened = line['opened']
    updated = line['updated']
    if line.get('closed'):
        closed = line['closed']
    else:
        closed = '0000-00-00 00:00:00'
    status = line['status']
    responsible_agency = line['responsible_agency']
    request_type = line['request_type']
    if line.get('request_details'):
        request_details = line['request_details']
    else:
        request_details = 'NA'
    latitude = line['point']['latitude']
    longitude = line['point']['longitude']
    address = line['address']
    dbinsert(case_id, opened, updated,closed, status, category, responsible_agency, request_type, request_details, address,
             latitude, longitude)


