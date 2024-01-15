import requests
import time
import random as rd

nbEnvoyees = 0
nbFailed = 0
nbSuccess = 0

while True:
    url = "http://10.0.0.252:5000"
    response = requests.get(url)
    nbEnvoyees += 1

    if response.status_code == 200:
        print("Success : "+response.text)
        nbSuccess += 1
    else:
        nbFailed += 1
        print("Failed with code "+str(response.status_code))
    time.sleep(rd.randrange(0, 5))

print(nbSuccess+" out of "+nbEnvoyees+" ("+nbFailed+" failed attempts)")
