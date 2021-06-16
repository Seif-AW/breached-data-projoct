import subprocess
import os
import json
import jsbeautifier
import pprint
import time

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

def write() :

    save_path = "/mnt/d/Reports"
    filename = time.strftime("%Y%m%d%H%M%S.txt")
    fullname = os.path.join(save_path, filename)
    msg = session.get('res').replace( '<br','\n')
    new = "-"* 50
    f = open(fullname, "+a")
    f.write("breaches found :"+msg)
    f.write(msg)
    f.close  

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='yahia', password='123'))
users.append(User(id=2, username='seif', password='seif'))
users.append(User(id=3, username='youssef', password='aa12'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
    # else : 
    #     x = "the user is not assigned "
    #     return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        try :
            user = [x for x in users if x.username == username][0]
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('search'))
            else : 
                return redirect(url_for('error'))
        except :
          return redirect(url_for('error'))

    return render_template('loginyoussef.html')

@app.route('/search',methods=['GET', 'POST'])
def search():
    if not g.user:
        return redirect(url_for('error'))

    return redirect(url_for('email'))

@app.route('/error',methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        return render_template('error.html')
# _______________________________________________________________________________________________________________________________________________
@app.route('/email',methods=["GET","POST"])
def email():
    if not g.user:
        return redirect(url_for('error'))
    if request.method == "POST":
        try :
            input = request.form["email"]
            # print(input)

#have ibeenpwnd_tool_canceled
            # inp = input
            # arg = "python3 ~/graduation/checkpwnedemails/checkpwnedemails.py -a ~/graduation/checkpwnedemails/key.txt " +' -s'  + inp
            # hbpwd = subprocess.run(arg, stdout=subprocess.PIPE ,text=True ,shell=True)
            # print(hbpwd.stdout)  

#haveibeenpwnd

            arg_hbpd = "curl -H \"hibp-api-key:b5e16e09e2fe4360830a08907d62353d\" -H \"user-agent: Beyond the Frame\" -sS https://haveibeenpwned.com/api/v3/breachedaccount/\{fname}\?truncateResponse=false".format(fname = input)
            hbpwd = subprocess.run(arg_hbpd, stdout=subprocess.PIPE ,text=True ,shell=True)
            hbpwd = jsbeautifier.beautify(hbpwd.stdout)

# dehashed
            arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(input)
            dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")
            res = jsbeautifier.beautify(dehashed.stdout)
# combining             
            res = res+ '\n'+'\n'+hbpwd

            res = res.replace('\n', '<br>')
        except :
            res = 'Invalid Input'   

#genarating report
        session['res'] = res
        write()      
                  
        return render_template("result.html" , out = res)
        
    else:
        return render_template("email.html")
# ____________________________________________________________________________________________________________________________________________
@app.route('/Facebook',methods=["GET","POST"])
def Facebook():
    if not g.user:
        return redirect(url_for('error'))
    if request.method == "POST":
        
        try :
# Elastic    
            mob = request.form["mobile"]
            number = mob
            arg  = "curl -X GET 'http://localhost:9200/eg/_search?q=\"{fname}\"'".format(fname = number) 
            p2 = subprocess.run(arg, stdout=subprocess.PIPE ,text=True ,shell=True)
            #print(p2.stdout) 
            data= json.loads(p2.stdout)
            state = data["hits"]["total"]['value']

            if str(state) == '1' :
                name = data['hits']['hits'][0]['_source']['name']
                fb_id = data['hits']['hits'][0]['_source']['id']  
                phone = data['hits']['hits'][0]['_source']['phone']  
                res = "Name: " +str(name)+  "\nID : " +fb_id+ "\nphone number : "+phone
                res_elk = res.replace('\n', '<br>')
# dehashed
                arg_dehashed = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(phone)
                dehashed = subprocess.run(arg_dehashed, capture_output=True, shell=True, encoding="utf8")
                res_dehashed = jsbeautifier.beautify(dehashed.stdout)                                

            else : 
                res = number +" doesn't seem to be in Facebook breach"

#have ibeenpwnd

            arg_hbpd = "curl -H \"hibp-api-key:b5e16e09e2fe4360830a08907d62353d\" -H \"user-agent: Beyond the Frame\" -sS https://haveibeenpwned.com/api/v3/breachedaccount/\{fname}\?truncateResponse=false".format(fname = phone)
            hbpwd = subprocess.run(arg_hbpd, stdout=subprocess.PIPE ,text=True ,shell=True)
            hbpwd = jsbeautifier.beautify(hbpwd.stdout)
#combin
            # res = res_elk+ '\n'+'\n'+hbpwd+ '\n'+'\n'+res_dehashed
            res = res_elk+ '\n'+'\n'+hbpwd
            res = res.replace('\n', '<br>')
            

        except  : 
            res = "Invalid Input , please enter FB id or a mobile number beginning with the country id"
     
#genarating report
        session['res'] = res
        write()
                     

        return render_template("result.html", out = res)
        
    else:
        return render_template("Facebook.html")

# ____________________________________________________________________________________________________________________________________
@app.route('/org',methods=["GET","POST"])
def org():
    if not g.user:
        return redirect(url_for('error'))
    if request.method == "POST":
        try :
            uname = request.form["org"]
            inp = uname
            arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(inp)
            arg3 = "  | ~/go/bin/gron  | grep 'mail\|pass\|name' "
            total = arg2 + arg3
            filt = subprocess.run(total, stdout=subprocess.PIPE ,text=True ,shell=True)
            # dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")        
            # res = jsbeautifier.beautify(dehashed.stdout)
#            res = pprint.pformat(dehashed.stdout , indent = 3)
            
            res = filt.stdout.replace('\n', '<br>')
            # res = res.replace('\n', '<br>')

        except : 
            res = 'invalid input'

#genarating report
        session['res'] = res
        write()

        return render_template("result.html" , out = res) 
        

    else:
        return render_template("org.html")

if __name__ == "__main__":
    app.run(debug=True, port=2005 , host='0.0.0.0')


