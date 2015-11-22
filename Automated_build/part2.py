#! /usr/bin/python

import os
from subprocess import Popen, PIPE


curr_dir = os.getcwd()


def append_to_logfile(data, header):
    with open(curr_dir + "/mediacloud_install.log", "a") as myfile:
        myfile.write("\n" + header + "\n========================\n")
        myfile.write("\n" + data + "\n")


print "======== Running \"runner/runner.py -i -s 6\" ========\n"
os.chdir("mercury/bootstrap/installer/")
proc = Popen(['runner/runner.py', '-i', '-s', '6'],stdout=PIPE, stdin=PIPE, stderr=PIPE,universal_newlines=True)
out,err = proc.communicate(input="{}\n".format("Y"))
print out, err
append_to_logfile(out, "Output of runner.py")
append_to_logfile(err, "Errors of runner.py")
os.chdir("../../..")
print "======== Ran \"runner/runner.py -i -s 6\" ========\n"
