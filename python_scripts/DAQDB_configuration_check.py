#!/usr/bin/python3

print('Version 1.0')
print('Author: adam.abed.abud@cern.ch')
print('Last modified: March 10, 2020\n\n')

# USAGE: python3 initial_checkups.py

import os
import time
import argparse
import subprocess
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parse_args():
    parser = argparse.ArgumentParser(description='Python script for checking DAQDB configuration setup ')
    return parser.parse_args()


# Checking kernel version.
def check_kernel_version():
    command = "uname -a " 
    print("Checking kernel version.")
    print("If NOT set to 4.15, please follow the README file and update\n")
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")
    output = process.stdout.split('\n')
    for line in output:
            if re.search("4.15.0", line):
                tests_dict['kernel'] = "Passed"



# Checking SELINUX is disabled.
def check_selinux():
    command = "getenforce " 
    print("Checking SELINUX is disabled.")
    print("If NOT disabled please modify the file here (/etc/selinux/config) with the following:")
    print("disabled instead of enforcing \n")    
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")
    output = process.stdout.split('\n')
    for line in output:
            if re.search("Disabled", line):
                tests_dict['selinux'] = "Passed"

# Checking firewall is disabled.
def check_firewalld():
    command = "systemctl status firewalld" 
    print("Checking firewall is disabled.")
    print("If NOT disabled please run the following command as root user: ")
    print("sudo systemctl stop firewalld \n")    
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")
    output = process.stdout.split('\n')
    for line in output:
            if re.search("inactive", line):
                tests_dict['firewalld'] = "Passed"



# Checking network IP is set.
def check_network():
    command = "ifconfig -a " 
    print("Checking network IP is set.")
    print("If NOT set please run the following command: ")
    print("sudo ifconfig enp24s0 192.168.1.4/24 up \n")    
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")    
    output = process.stdout.split('\n')
    for line in output:
            if re.search("192.168.1.4", line):
                tests_dict['network'] = "Passed"


# Checking memory devices mounted
def check_pmem_mount():
    command = "df -h " 
    print("Checking that PMEM devices are mounted.")
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True) 
    output = process.stdout
    print(output)
    print("\n")
    output = process.stdout.split('\n')
    for line in output:
            if re.search("/mnt/pmem", line):
                tests_dict['pmem_mount'] = "Passed"

def main():
    args=parse_args()
    global tests_dict
    tests_dict  = {"kernel" : "Failed", "selinux" : "Failed", "firewalld" : "Failed", "network" : "Failed", "pmem_mount" : "Failed"}
    check_kernel_version()
    check_selinux()
    check_firewalld() #NOT WORKING
    check_network()
    check_pmem_mount()

    print("\n\n=========== SUMMARY ============ ")
    print("Test \t\t\t  Result " )
    print("================================ ")
    for test in tests_dict:
         if tests_dict[test] == "Passed": 
              print(test, " \t\t ", bcolors.OKGREEN + tests_dict[test] + bcolors.ENDC)
         else: 
              print(test, " \t\t ", bcolors.FAIL + tests_dict[test], " \t\t", "ATTENTION!" + bcolors.ENDC )


    print("\n\nDAQDB configuration check ended at ", time.ctime())
    print("")


if __name__ == "__main__":
    main()

