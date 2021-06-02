import os 
import time
import subprocess
import json

a = 0 

def rep ():
        save_path = "/home/dld/timer/report/"
        filename = time.strftime("%Y%m%d%H%M%S.txt")
        fullname = os.path.join(save_path, filename)
        msg = json.dumps(data)
        new = "-"* 50
        f = open(fullname, "+a")
        f.write("\n new breaches found : \n"+new+"\n"+msg+"\n"+new*2)
        f.close 
        link = "http://52.151.252.60:9090/"+filename
        send_req  = " curl --data chat_id='1348121058' --data 'text=THIS IS A TEST MSG: {}' 'https://api.telegram.org/bot1859447166:AAFczzEAR4lxmfX7cit83IWYPTUZ1uWbq70/sendMessage'".format(link)
        p2 = subprocess.run(send_req ,shell=True)


starttime = time.time()

while True:
    
    input = "hti.edu.eg"
    arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(input)
    dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")
    data = json.loads(dehashed.stdout)
    state = data['total']
 
    if state != a : 
        rep ()

    a = state
 

    time.sleep(30.0 - ((time.time() - starttime) % 30.0))
