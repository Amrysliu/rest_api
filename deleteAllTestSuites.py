import sys
from TestSuites import TestSuites

test_suite = TestSuites("http://10.161.8.44")
error_message, testsuites = test_suite.getAllTestSuite()

if error_message != '':
    print(error_message)
    sys.exit(1)

for one in testsuites :
    error_message = test_suite.deleteTestSuite("CE04082DA88CB4E3", "2ADD91EB3CB4D956", one["id"])
    
    if error_message != '':
        print("Failed to delete " + one["name"])
        print(error_message)
        sys.exit(2)
    print(one["name"] + " was deleted successfully")
