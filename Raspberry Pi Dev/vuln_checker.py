import os
import time

flag = "False"

while flag != "True":
    if os.path.exists('vuln.txt'):
        os.system('python vuln_publish.py')
        flag == "True"
        print("Vulnerable: vuln scan results")
	exit()
    if os.path.exists('notvuln.txt'):
        os.system('python notvuln_publish.py')
        exit()
else:
    print("doesnt exist")
    time.sleep(3)

