import json
import pprint

data = json.load(open('jsontest.txt'))
p = pprint.pformat(data , indent = 3)

print(p)
