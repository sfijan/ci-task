#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description='Get some football players.')
parser.add_argument('-m', '--method', metavar='METHOD', nargs=1, type=str, default='GET', help='sets the HTTP method to be used (defaults to GET)')
parser.add_argument('url', metavar='address', nargs=1, type=str, help='url to which to send the request')
parser.add_argument('-id', metavar='id', nargs='+', type=int, help='select the id or ids of records to get (gets all by default)')

args = parser.parse_args()
