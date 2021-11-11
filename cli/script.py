#!/usr/bin/env python
import argparse
import requests
import json
import os
import datetime
import time

def unix_to_date(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
def date_to_unix(s):
    return time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f").timetuple())
def str_to_date(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

#write all of the records into a file with the given filename
def write_to_file(filename, records):
    if records == []:
        return
    if os.path.exists(filename):
        with open(filename, 'r+') as file:
            j = json.load(file)                         #get the data,
            j[str(datetime.datetime.now())] = records   #add the new records
            file.seek(0, 0)                             #reset and write
            file.write(json.dumps(j, indent=4, sort_keys=True, default=str))

    else:       #if there is no file, simply write the records
        with open(filename, 'w') as file:
            j = {str(datetime.datetime.now()): records}
            file.write(json.dumps(j, indent=4, sort_keys=True, default=str))
    return

#return a dictionary with all the player_ids and timestamp of last fetch
def get_records(filename):
    if not os.path.exists(filename):
        return {}
    ret = {}
    with open(filename, 'r') as file:
        j = json.load(file)
        for ts in j:                #for every fetch time
            for record in j[ts]:    #for every record
                ret[record['player_id']] = ts
    return ret



parser = argparse.ArgumentParser(description='Get some football players.')
parser.add_argument('-m', '--method', metavar='METHOD', nargs=1, type=str, default='GET', help='sets the HTTP method to be used (defaults to GET)')
parser.add_argument('-a', '--address', metavar='url', type=str, help='url address to which to send the request')
parser.add_argument('-id', metavar='id', nargs='+', type=int, help='select the id or ids of records to get (gets all by default)')


single = 'single'
more = 'more'
args = parser.parse_args()
#print(args)

if args.method.upper() == 'GET':
    #fetch records
    if not args.id:             #no specified ids -> get all
        filename = more
        fetched = requests.get(args.address).json()
    elif len(args.id) == 1:     #single specified id
        filename = single
        fetched = [requests.get(args.address + '/' + str(args.id[0])).json()]
    else:                       #multiple specified ids
        filename = more
        fetched = [requests.get(args.address + '/' + str(i)).json() for i in args.id]

    #make a selection and add records
    stored = get_records(filename)
    to_put = []
    for record in fetched:
        if (not record['player_id'] in stored.keys() or
                str_to_date(record['modified']) > str_to_date(stored[record['player_id']])):
            to_put.append(record)
    write_to_file(filename, to_put)

