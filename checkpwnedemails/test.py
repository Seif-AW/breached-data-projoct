import subprocess
import os


select = '-s'
inp = "zeifoa5@gmail.com"

if select == '-s' :
	arg = "python3 checkpwnedemails.py -a key.txt " +select + inp

elif select == '-a' :
	filepath = ''
	arg = "python3 checkpwnedemails.py -a key.txt " +select + filepath


run = subprocess.call(arg,shell=True)

