#!/usr/bin/python

import json
import requests
import argparse

def authenticate(username='admin', passwd='admin'):
    headers = {'content-type': 'application/json'}
    payload = json.dumps({'username': username, 'passwd': passwd})
    response = requests.post(args.target + '/auth', headers=headers, data=payload)
    if (response.status_code >= 200) and (response.status_code < 300):
        return response.json()['jwt']
    print response.status_code
    return None

def main():
    token = authenticate(args.username, args.password)
    get_headers = {'authorization': 'Bearer ' + token}
    headers = {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }

    response = requests.get(args.target + '/device', headers=get_headers)
    if response.status_code != 200:
        print "failed to read devices"

    devices = response.json()['devices']
    for d in devices:
        del d['updated']
        del d['created']
        d['freq'] = int(args.timeout)*333
        upd = requests.put("%s/device/%s" % (args.target, d['id']), headers=headers, data=json.dumps(d))
        if upd.status_code != 200:
            print "%s %s" % (upd, upd.json())


desc= """ """
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-t', '--target', help="", default="http://localhost:8000")
parser.add_argument('-u', '--username', help="", default="admin")
parser.add_argument('-p', '--password', help="", default="admin")
parser.add_argument('-w', '--timeout', help="", default="3")
args = parser.parse_args()
main()
