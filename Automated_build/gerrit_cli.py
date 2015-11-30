#! /usr/bin/python

import os
import json
import time

time_since_epoch = int(time.time())

def run_gerrit_cli(gerrit_cli):
    global time_since_epoch
    f = os.popen(gerrit_cli)
    output = f.read()
    output = output.splitlines()
    for i in output:
        d = json.loads(i)
        if 'owner' in d:
            if time_since_epoch - d['createdOn'] > (86400 + 28800):
                continue
            sub = d['subject']
            if len(sub) > 60:
               index = sub.rfind(' ', 0, 60)
               second_part = sub[index+1:]
               if len(second_part) > 60:
                   ind = second_part.rfind(' ', 0, 60)
                   second_part = second_part[:ind] + "\n                     " + second_part[ind+1:]
               sub = sub[:index] + "\n                     " + second_part
            print "%-20s %s" % ( d['owner']['email'], sub)
            print ""

run_gerrit_cli("ssh -p 29418 vhosakot@cloud-review.cisco.com gerrit query --format=JSON status:new project:mercury/bootstrap")
run_gerrit_cli("ssh -p 29418 vhosakot@cloud-review.cisco.com gerrit query --format=JSON status:new project:mercury/installer")
run_gerrit_cli("ssh -p 29418 vhosakot@cloud-review.cisco.com gerrit query --format=JSON status:new project:mercury/kolla")
