#!/usr/bin/python3

import sys, getopt
from MediumType import MediumType
from Machine import Machine
from TestSuites import TestSuites
from JobGroup import JobGroup

def printHelp():
    print("""
    USAGE:
        python3 openqa.py -h For help

        python3 openqa.py -c csv.file -a https://openqa.suse.de -k 123456 -s 123456 -T -f Flavor -d distri -v version -g group_name -p priority

    Options:
        -c, CSV file name with relative path
        -a, OpenQA server address, https://openqa.suse.de
        -k, api key
        -s, api secret
        -f, flavor
        -d, distri
        -v, version
        -g, job group name
        -p, priority [optional]
        -T, add testsuites.
    Note:
        -f, -d, -v -g -r and -p must be used at same time. If users give -f, -d, -v, -g script will add testsuit to jobgroup.
        -p, specify priority. if not priority is specified, using default value '50' 
    """)


csv_file    = ''
host        = ''
api_key     = ''
api_secret  = ''
flavor      = ''
distri      = ''
version     = ''
group       = ''
priority    = 50
operate     = 'addTestSuites'

mediumIds   = {}
machineIds  = {}
group_id    = ''

flag_add_jobTemplate = 0
    
try:
    options, remainder = getopt.getopt(
        sys.argv[1:], 
        "Thc:a:k:s:f:d:v:g:p:",
        [
            'help',
            'csv_file=',
            'host=',
            'api_key=',
            'api_secret=',
            'flavor='
            'distri='
            'version='
            'group='
            'priority='
            'TestSuites'
        ])
except getopt.GetoptError as err:
    print('ERROR:', err)
    sys.exit(1)

for opt, arg in options:
    if opt in ('-c', '--csvfile'):
        csv_file = arg
    elif opt in ('-a', '--host'):
        host = arg
    elif opt in ('-k', '--apikey'):
        api_key = arg
    elif opt in ('-s', '--apisecret'):
        api_secret = arg
    elif opt in ('-f', '--flavor'):
        flavor = arg
    elif opt in ('-d', '--distri'):
        distri = arg
    elif opt in ('-v', '--version'):
        version = arg
    elif opt in ('-g', '--group'):
        group = arg
    elif opt in ('-p', '--priority'):
        priority = arg
    elif opt in ('-T'):
        operate = 'addTestSuites'
    elif opt in ('-h', '--help'):
        printHelp()
        sys.exit(0)

#check the parameter integrity
if csv_file == '' or host == '' or api_key == '' or api_secret == '' :
    print("Parameter Missing")
    printHelp()
    sys.exit(1)
if flavor != '' and distri != '' and version != '' and group !='' :
    flag_add_jobTemplate = 1

if operate == 'addTestSuites':
    testsuite = TestSuites(host)
    error_message, result_file = testsuite.addTestSuite(csv_file, api_key, api_secret, flag_add_jobTemplate, flavor, distri, version, group, priority)
    if error_message != '':
        print(error_message)
        sys.exit(5)
    print('See the result file: ' + result_file)
    sys.exit(0)
