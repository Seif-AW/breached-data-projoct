from os import stat_result
import time
import subprocess
import json

a = 0 

starttime = time.time()
while True:
    
    input = "hti.edu.eg"
    arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(input)
    dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")
    data = json.loads(dehashed.stdout)
    state = data['total']
    print(a)
    if state != a : 
        pass # here to put your notification code instead of pass 
    a = state
    print(a)

    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
