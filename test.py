from os import stat_result
import time
import subprocess
import json

def request () : 
    input = "hti.edu.eg"
    arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(input)
    dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")
    data = json.loads(dehashed.stdout)
    state = data['total']
    a = 0 
    if state != a : 
        # here to put your notification coede
    a = state
    # print(state)



starttime = time.time()
while True:
    request()
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
