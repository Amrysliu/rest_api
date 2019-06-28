import requests
import time
import csv
from Signature import getSignature

class JobTemplate:
    def __init__(self, host):
        self.host       = host

    def addJobTemplate(self, api_key, api_secret, flavor, distri, version, arch, machine, group_name, testsuite_name, priority=50):

        timestamp   = int(time.time())
        url         = '/api/v1/job_templates'

        # get signature
        signature = getSignature(url + str(timestamp), api_secret)

        header = {'X-API-KEY':api_key, 'X-API-HASH':signature, 'X-API-Microtime':str(timestamp), 'Accept':'application/json'}

        error_message = ''

        add_template_host = self.host + url

        params = {
                    "group_name":group_name,
                    "machine_name":machine,
                    "test_suite_name":testsuite_name,
                    "arch":arch,
                    "flavor":flavor,
                    "distri":distri,
                    "version":version,
                    "prio":priority
                }

        resp = requests.post(add_template_host, headers=header, data=params, verify=False)

        if resp.status_code != 200:
            result = resp.json()
            error_message = result['error']

        return error_message
