import requests
import time
import csv
import random
import string

from Signature import getSignature
from JobTemplate import JobTemplate

class TestSuites:
    def __init__(self, host):
        self.host       = host
     
    def _addTestSuite(self, name, setting_str, description = ""):
        testsuite_dic = {}
        testsuite_dic["name"] = name
        testsuite_dic["description"] = description
        for s in setting_str.split("\n"):
            if s == '':
                continue
            setting = s.split("=")
            key = "settings[" + setting[0] + "]"
            testsuite_dic[key] = setting[1]
        
        self.total_num = self.total_num + 1
        
        #open the result file
        refile = open(self.result_file, 'a')

        resp = requests.post(self.add_case_host, headers=self.header, data=testsuite_dic, verify=False)
        if resp.status_code != 200:
            self.failed_num = self.failed_num + 1
            refile.write("[ERROR] add test suite " + name + " failed \n")
            err_msg = resp.json()
            refile.write(err_msg["error"] + "\n")
        else :
            refile.write("[SUCCESS] add test suite " + name + " successfully \n")
            self.success_num = self.success_num + 1
            add_case_result = resp.json()
            testsuite_id = add_case_result["id"]

            if self.flag_add_jobTemplate == 1:
                job_template = JobTemplate(self.host)
                error_message = job_template.addJobTemplate(self.api_key, self.api_secret, self.flavor, self.distri, self.version, self.arch, self.machine, self.group, name, self.priority)

                if error_message != '':
                    refile.write('[ERROR] add job template failed \n')
                    refile.write(error_message + "\n")
                    self.job_template_failed_num = self.job_template_failed_num + 1
        refile.close()

    def addTestSuite(self,csv_file, api_key, api_secret, flag_add_jobTemplate=0, flavor='', distri='', version='', group='', priority=50):
        self.csv_file   = csv_file
        self.api_key    = api_key
        self.api_secret = api_secret
        self.flavor     = flavor
        self.distri     = distri
        self.version    = version
        self.group      = group
        self.priority   = priority 
        self.flag_add_jobTemplate = flag_add_jobTemplate

        timestamp   = int(time.time())
        url         = '/api/v1/test_suites'

        # get signature
        signature = getSignature(url + str(timestamp), self.api_secret)

        header = {'X-API-KEY':self.api_key, 'X-API-HASH':signature, 'X-API-Microtime':str(timestamp)}
        
        result_file = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + ".txt"

        error_message = ''

        self.add_case_host           = self.host + url
        self.header         = header
        self.result_file    = result_file
        self.total_num      = 0
        self.success_num    = 0
        self.failed_num     = 0
        self.job_template_failed_num = 0;

        #read csv file and add test suites
        try:
            with open(self.csv_file, 'r') as testsuite_csv:
                content = csv.reader(testsuite_csv, delimiter=',')
                for row in content:
                    if row[0] == 'x86_64':
                        continue
                    name_x86_64     = row[0]
                    setting_x86_64  = row[1]
                    name_ppc64le    = row[2]
                    setting_ppc64le = row[3]
                    name_s390x      = row[4]
                    setting_s390x   = row[5]
                    name_aarch64    = row[6]
                    setting_aarch64 = row[7]
                    
                    if name_x86_64 != '':
                        self.arch       = 'x86_64'
                        self.machine    = '64bit' 
                        self._addTestSuite(name_x86_64, setting_x86_64)
                    if name_ppc64le != '':
                        self.arch       = 'ppc64le'
                        self.machine    = 'ppc64le'
                        self._addTestSuite(name_ppc64le, setting_ppc64le)
                    if name_s390x != '':
                        self.arch       = 's390x'
                        self.machine    = 's390x-kvm-sle12'
                        self._addTestSuite(name_s390x, setting_s390x)
                    if name_aarch64 != '':
                        self.arch       = 'aarch64'
                        self.machine    = 'aarch64'
                        self._addTestSuite(name_aarch64, setting_aarch64)

                rfile = open(self.result_file, 'a')
                rfile.write(str(self.total_num) + " testsuites are operated \n")
                rfile.write(str(self.success_num) + " testsuites success to add \n")
                rfile.write(str(self.failed_num) + " testsuites failed to add \n")
                rfile.write(str(self.job_template_failed_num) + " testsuites failed to add into job template")
                rfile.close()
        except OSError as err:
            error_message = err 

        return error_message, result_file

    def deleteTestSuite(self, api_key, api_secret, testsuite_id):
        timestamp   = int(time.time())
        url         = '/api/v1/test_suites/' + str(testsuite_id)

        # get signature
        signature = getSignature(url + str(timestamp), api_secret)

        delete_header = {'X-API-KEY':api_key, 'X-API-HASH':signature, 'X-API-Microtime':str(timestamp), 'Accept':'application/json'}
        
        delete_url = self.host + url
        resp = requests.delete(delete_url, headers=delete_header, verify=False)

        if resp.status_code != 200 :
            data = resp.json()
            print(data)
            return data["error_status"]
        return ''

    def getAllTestSuite(self):
        resp = requests.get(self.host + "/api/v1/test_suites", verify=False)
        data = resp.json()
        if resp.status_code != 200:
            return data["error"] , ()
        return '', data["TestSuites"]
        