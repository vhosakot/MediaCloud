#! /usr/bin/python

import os
import re
from subprocess import Popen, PIPE


new_repo = False
os.system("rm -rf mediacloud_install.log")
curr_dir = os.getcwd()


def append_to_logfile(data, header):
    with open(curr_dir + "/mediacloud_install.log", "a") as myfile:
        myfile.write("\n" + header + "\n========================\n")
        myfile.write("\n" + data + "\n")


if not os.path.isdir("mercury/bootstrap/"):
    print "======== No Mercury bootstrap repo found ========\n"
    print "======== Cloning Mercury bootstrap repo ========\n"
    os.chdir("mercury")
    os.system("git clone http://cloud-review.cisco.com/mercury/bootstrap")
    new_repo = True
    print "======== Cloned Mercury bootstrap repo ========\n"
    os.chdir("../")


if os.path.exists("mercury/bootstrap/openstack-configs/setup_data.yaml") and not new_repo:
    print "======== Backing up mercury/bootstrap/openstack-configs/setup_data.yaml ========\n"
    proc = Popen(['cp', 'mercury/bootstrap/openstack-configs/setup_data.yaml', '.'],stdout=PIPE, stdin=PIPE, stderr=PIPE,universal_newlines=True)
    out,err = proc.communicate(input="{}\n".format("yes"))
    print out, err
    print "======== mercury/bootstrap/openstack-configs/setup_data.yaml backed up ========\n"


if os.path.exists("mercury/bootstrap/installer/openstack/playbooks/openstack-uninstall.yaml") and not new_repo:
    print "======== Running openstack-uninstall.yaml ========\n"
    os.chdir("mercury/bootstrap/installer/openstack/playbooks/")
    proc = Popen(['./mercury_playbook', 'openstack-uninstall.yaml'],stdout=PIPE, stdin=PIPE, stderr=PIPE,universal_newlines=True)
    out,err = proc.communicate(input="{}\n".format("y"))
    # print out, err
    append_to_logfile(out, "Output of openstack-uninstall.yaml")
    append_to_logfile(err, "Errors of openstack-uninstall.yaml")
    out_list = out.splitlines() + err.splitlines()
    for line in out_list:
        line = line.lower()
        if "[os_uninstall | Systemctl daemon-reload to avoid access denied error.]".lower() in line:
            continue
        if "fail" in line or "err" in line:
            if "failed=0".lower() in line:
                continue
            print "========  ", line
    print "======== Ran openstack-uninstall.yaml ========\n"
    os.chdir("../../../../../")


if not new_repo:
    print "======== Running unbootstrap.sh ========\n"
    os.chdir("mercury/bootstrap/")
    proc = Popen(['./unbootstrap.sh'],stdout=PIPE, stdin=PIPE, stderr=PIPE,universal_newlines=True)
    out,err = proc.communicate(input="{}\n".format("Y"))
    # print out, err
    append_to_logfile(out, "Output of unbootstrap.sh")
    append_to_logfile(err, "Errors of unbootstrap.sh")
    out_list = out.splitlines() + err.splitlines()
    for line in out_list:
        line = line.lower()
        if "fail" in line or "err" in line:
            if "failed to stop docker-cobbler.service: unit docker-cobbler.service not loaded".lower() in line:
                continue
            print "========  ", line
    print "======== Ran unbootstrap.sh ========\n"
    os.chdir("../../")


if not new_repo:
    print "======== Deleting Mercury bootstrap repo ========\n"
    os.system("rm -rf mercury/bootstrap")
    print "======== Deleted Mercury bootstrap repo ========\n"
    print "======== Cloning Mercury bootstrap repo ========\n"
    os.chdir("mercury")
    os.system("git clone http://cloud-review.cisco.com/mercury/bootstrap")
    print "======== Cloned Mercury bootstrap repo ========\n"
    os.chdir("../")


print "======== Copying MediaCloud's setup_data.yaml to mercury/bootstrap/openstack-configs/ ========\n"
proc = Popen(['cp', 'setup_data.yaml', 'mercury/bootstrap/openstack-configs/'],stdout=PIPE, stdin=PIPE, stderr=PIPE,universal_newlines=True)
out,err = proc.communicate(input="{}\n".format("yes"))
print out, err
print "======== Copied MediaCloud's setup_data.yaml to mercury/bootstrap/openstack-configs/ ========\n"


print "======== Running \"./bootstrap.sh -i -t master\" ========\n"
os.chdir("mercury/bootstrap")
proc = Popen(['./bootstrap.sh', '-i', '-t', 'master'],stdout=PIPE, stdin=PIPE, stderr=PIPE,universal_newlines=True)
out,err = proc.communicate()
# print out, err
append_to_logfile(out, "Output of bootstrap.sh")
append_to_logfile(err, "Errors of bootstrap.sh")
out_list = out.splitlines() + err.splitlines()
bootstrap_passed = False
for line in out_list:
    line = line.lower()
    if "Generating openrc file for your setup".lower() in line:
        bootstrap_passed = True
    if "fail" in line or "err" in line:
        if re.search(r"byte-compiling .*pyc", line) is not None or\
           re.search(r"copying .*ucssdk", line) is not None or\
           re.search(r"failovermethod = priority", line) is not None or\
           re.search(r"rule[ ]*\|[ ]*status[ ]*\|[ ]*error[ ]*\|", line) is not None or\
           re.search(r"ignoring errors", line) is not None or\
           re.search(r"/usr/sbin/semodule:.*failed", line) is not None or\
           re.search(r"libsemanage.semanage_link_sandbox:.*no such file or directory", line) is not None:
             continue
        print "========  ", line
os.chdir("../..")
if not bootstrap_passed:
    print "======== Ran \"./bootstrap.sh -i -t master\". It failed ========\n"
else:
    print "======== Ran \"./bootstrap.sh -i -t master\". It passed! ========\n"
