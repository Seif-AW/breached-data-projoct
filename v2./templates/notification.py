
from os import stat_result


while True : 
    input = "hti.edu.eg"
    arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(input)
    dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")
    data = json.loads(dehashed.stdout)
    state = data['total']
    print(state)
    type(data['total'])

    new_value = state
    a = 0 

    if a != new_value  :
        pass 

    a = new_value 

    time.sleep(5.0 - ((time.time() - starttime) % 5.0))  



