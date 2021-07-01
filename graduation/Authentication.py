import subprocess
import os
import json
import jsbeautifier

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

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
        

@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('search'))

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

@app.route('/email',methods=["GET","POST"])
def email():
    if request.method == "POST":
        input = request.form["email"]
        print(input)
 
        # select = '-s' 
        # arg = "python3 checkpwnedemails.py -a key.txt " +select + inp
        # hbpwd = subprocess.run(arg, stdout=subprocess.PIPE ,text=True ,shell=True)
        # print(hbpwd.stdout)   
        arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(input)

        dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")
        res = jsbeautifier.beautify(dehashed.stdout)
        return render_template("result.html" , out = res)
    else:
        return render_template("email.html")

@app.route('/Facebook',methods=["GET","POST"])
def Facebook():
    if request.method == "POST":
        mob = request.form["mobile"]
        number = mob
        number = str(number)
        arg  = "curl -X GET 'http://localhost:9200/eg/_search?q=\"{fname}\"'".format(fname = number) 
        print(arg)
        p2 = subprocess.run(arg, stdout=subprocess.PIPE ,text=True ,shell=True)
        #print(p2.stdout) 
        data= json.loads(p2.stdout)
        state = data["hits"]["total"]['value']
        if str(state) == '1' :
            name = data['hits']['hits'][0]['_source']['name']
            fb_id = data['hits']['hits'][0]['_source']['id']  
            phone = data['hits']['hits'][0]['_source']['phone']  
            res = "Name: " +str(name)+  "\nID : " +fb_id+ "\nphone number : "+phone
            res = res.replace('\n', '<br>')
        return render_template("result.html",out=res)
    else:
        return render_template("Facebook.html")

@app.route('/org',methods=["GET","POST"])
def org():
    if request.method == "POST":
        uname = request.form["org"]
        inp = uname
        arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(inp)
        dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")        
        res = jsbeautifier.beautify(dehashed.stdout)
        return render_template("result.html" , out = res)
    else:
        return render_template("org.html")




#selecting mail or mobile number 
# if s1 =='mail' :
#     #selecting single or muliple mail
    
#     inp = uname
#     select == '-s' 
#     arg = "python3 checkpwnedemails.py -a key.txt " +select + inp
#     # elif select == '-a' :
#     #     filepath = ''
#     #     arg = "python3 checkpwnedemails.py -a key.txt " +select + filepath
        
#     hbpwd = subprocess.run(arg, stdout=subprocess.PIPE ,text=True ,shell=True)
#     print(hbpwd.stdout)   

#     arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(inp)
#     dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")

# elif s1 =='org' :
    inp = uname
    arg2 = "curl 'https://api.dehashed.com/search?query={}' -u zeifoa5@gmail.com:i0xtde61tvcrmm4skwvx8atdrbv1zmed -H 'Accept: application/json'".format(inp)
    dehashed = subprocess.run(arg2, capture_output=True, shell=True, encoding="utf8")

# elif s1 == 'num' :
# number = uname
# number = str(number)
# arg  = "curl -X GET 'http://localhost:9200/eg/_search?q=\"{fname}\"'".format(fname = number) 
# #print(arg)
# p2 = subprocess.run(arg, stdout=subprocess.PIPE ,text=True ,shell=True)
# #print(p2.stdout) 

# data= json.loads(p2.stdout)
# state = data["hits"]["total"]['value']
# if str(state) == '1' :
#     name = data['hits']['hits'][0]['_source']['name']
#     fb_id = data['hits']['hits'][0]['_source']['id']  
#     phone = data['hits']['hits'][0]['_source']['phone']  
#     print(f"Name : {name} \nID : {fb_id} \nphone number : {phone}")

#     else : 
#         print(f"The number {number} , doesn't seem to have a fb breach")



if __name__ == "__main__":
    app.run(debug=True, port=9000)