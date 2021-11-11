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

parser = argparse.ArgumentParser(description='Get some football players.')
parser.add_argument('-m', '--method', metavar='METHOD', nargs=1, type=str, default='GET', help='sets the HTTP method to be used (defaults to GET)')
parser.add_argument('-a', '--address', metavar='url', type=str, help='url address to which to send the request')
parser.add_argument('-id', metavar='id', nargs='+', type=int, help='select the id or ids of records to get (gets all by default)')

args = parser.parse_args()
print(args)

#TODO   add previous records
if args.method.upper() == 'GET':
    if args.id and len(args.id) == 1:   #get a single record
        r = requests.get(args.address + '/' + str(args.id[0]))
        if os.path.exists('single'):    #if a record exists,
            with open('single', 'r') as file:
                saved_id = json.load(file)['player_id'] #and has the same id
            if (saved_id == args.id[0] and
                os.path.getmtime('single') > date_to_unix(r.json()['modified'])):   #and is recent enough
                print('Data is already up to date') #only then is there no need to update
                exit(0)

        with open('single', 'w') as f:              #otherwise update
            s = json.dumps(r.json(), indent=4, sort_keys=True, default=str)
            f.write(s)

    else:       #get multiple records
        update = False
        if args.id:     #specified records
            s = '['
            for i in args.id:
                r = requests.get(args.address + '/' + str(i))
                if not os.path.exists('more') or os.path.getmtime('more') < date_to_unix(r.json()['modified']):
                    update = True
                s += json.dumps(r.json(), indent=4, sort_keys=True, default=str) + ','
            s = s[:-1] + ']'
        else:           #all the records
            r = requests.get(args.address)
            s = '['
            for i in r.json():
                s += json.dumps(i, indent=4, sort_keys=True, default=str) + ','
                if not os.path.exists('more') or os.path.getmtime('more') < date_to_unix(i['modified']):
                    update = True
            s = s[:-1] + ']'

        if update:      #update if needed
            with open('more', 'w') as f:
                f.write(s)
        else:
            print('Data is already up to date')

