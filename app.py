#CHALLENGE URL: once you figure out the solution, try breaking into here -> https://crackme2-gdsc.mitb.tech 
the_super_secret = open("the_real_secret.txt", "r").read()

version = "0064-EXAMPLE" 

from flask import Flask, request, render_template, make_response
app = Flask(__name__)

import random
import time
import jwt


# Stores all accounts
# TODO: Make this a database (Task scheduled for the year 3024! (average dev timeline))

accounts = {
    "0" : {
        "username" : "admin",
        "password" : hash(the_super_secret)
    }
}

# Handle logins and registrations
# Moved here for better readability
# Only called AFTER validation is already done, so no internal validation needed

def login(userID):
    res = make_response(render_template('login_success.html'))
    token = jwt.encode({"id" : userID}, jwt_secret, algorithm="HS256")
    res.set_cookie("account", value=token)
    return res


def register(username, password):
    userID = int(time.time())
    accounts[userID] = {
        "username" : username,
        "password" : hash(password)
    }
    
    return render_template('register_success.html')



# generate a random seed

random_seed_string = time.strftime("%Y %H:%M:%S +0000", time.gmtime(random.random())) + version
seed = int.from_bytes(bytes(random_seed_string, 'utf-8'), byteorder='little', signed=False)
random.seed(seed)

# generate a JWT secret to sign all tokens. HMAC (HS256) verification used.

jwt_secret = ""
for i in range(1,50):
    jwt_secret += str(random.randint(0,9))



# Flask: Routes /register, /logout, /login and /

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

        if username is None or password is None:
            return render_template('register.html',  invalidacc = "Username/Password cannot be empty")

        if len(username) == 0 or len(password) == 0:
            return render_template('register.html',  invalidacc = "Username/Password cannot be empty")

        for userID in accounts.keys():
            if accounts[userID]['username'] == username:
                return render_template('register.html',  invalidacc = "Account already exists")
    
        return register(username, password)
    
    if request.method == 'GET':
        return render_template('register.html',invalidacc = "")
        


    if request.method == 'GET':
        return render_template('register.html',invalidacc = "")


# It just invalidates the account cookie, it doesn't care to check if it exists or not beforehand. Doesn't matter anyway.
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    res = make_response(render_template("logout_success.html"))
    res.set_cookie('account', '', expires=0)
    return res



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Form Submit
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

        for userID in accounts.keys():
            if accounts[userID]['username'] == username and accounts[userID]['password'] == hash(password):
                return login(userID)
    
        return render_template('login.html', invalidcreds = "Invalid Credentials")

    # Page load
    if request.method == 'GET':
        return render_template('login.html',invalidcreds = "")



@app.route('/')
def home_page():
    if 'account' in request.cookies:
            account_token = request.cookies.get('account')
            try:
                user_obj = jwt.decode(account_token, jwt_secret, algorithms=["HS256"])
                
                if(user_obj['id'] == "0"):
                    return render_template('home.html', showlogin = "hidden" , showregister = "hidden", morecontent = f"Here you go: {the_super_secret}", version = version)
                return render_template('home.html', showlogin = "hidden" , showregister = "hidden" , morecontent = "Regular users may not see the secret", version = version)

            except:
                res = make_response(render_template("home.html", showlogout = "hidden", morecontent = "Login invalidated", version = version))
                res.set_cookie('account', '', expires=0)
                return res
    else:
        return render_template('home.html', morecontent = "You are not logged in" , showlogout = "hidden", version = version)

