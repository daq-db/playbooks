#!/usr/bin/python3

print('Version 1.0')
print('Author: adam.abed.abud@cern.ch')
print('Last modified: March 6, 2020\n\n')

# USAGE: time python rados_test.py
import os
import time
import argparse
import subprocess
import re

def parse_args():
    parser = argparse.ArgumentParser(description='Python script for checking the health of PMEM devices ')
    return parser.parse_args()


# Checking if PMEM tools are installed on the machine
def check_yum_packages():
    pkgs = "ipmctl  ndctl" 
    command = "yum list installed " + pkgs 
    print("Checking if PMEM packages installed.")
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")


# Checking memory devices topology
def check_memory_topology():
    command = "ipmctl show -topology" 
    print("Checking memory topology.")
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    output = process.stdout
    print(output)
    print("\n")
    total_size = 0
    unit = ''
    output = process.stdout.split('\n')
    sockets = ["CPU1", "CPU2"]
    for sock in sockets:
        for line in output:
            if re.search(sock, line) and re.search("Logical Non-Volatile Device", line):
                 fields = line.strip().split()
                 unit = fields[7]
                 total_size += float(fields[6])

        print("Total size socket ", sock, " ", total_size, unit)
        total_size = 0
    print("\n\n")    

           


# Checking health of the PMEM devices 
def check_health_PMEM():
    command = "ipmctl show -dimm" 
    print("Checking PMEM health status.")
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")



# Checking health of the PMEM devices 
def check_available_namespaces():
    command = "ndctl list -u " 
    print("Checking available namespaces.")
    print("Executing: ", command)
    process = subprocess.run(command, stdin=True, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    print(output)
    print("\n")    




def main():
    args=parse_args()
    check_yum_packages()
    check_memory_topology()
    check_health_PMEM()
    check_available_namespaces()

    print("\n\nPMEM health check ended at ", time.ctime())


if __name__ == "__main__":
    main()

