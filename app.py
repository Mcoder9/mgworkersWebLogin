from flask import Flask, json, redirect, request, url_for
from oauth2client.service_account import ServiceAccountCredentials
from flask import render_template
from datetime import datetime
import requests
import gspread

# initiate app
app = Flask(__name__)
app.debug = True

# googl sheet setup
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Mgworkers-User-Managment").sheet1  # Open the spreadhseet



@app.route("/")
def home():
    return render_template('login.html')

@app.route("/signin", methods=['POST'])
def signin():
    global username
    username = request.form['username']
    password = request.form['password']
    if username and password:
        return validateUser(username, password)
    return redirect("/")


@app.route("/welcome/<info>")
def welcome(info):
    return render_template('welcome.html')

@app.route("/continue")
def continue_():
    return "continue ..."

@app.route("/dangerzone")
def dangerzone():
    return render_template('dangerzone.html')

@app.route("/expired")
def expired():
    return render_template('expired.html')

def userSubscription(expiryDate):
    today = requests.get(r"https://just-the-time.appspot.com/?f=%d-%m-%Y", timeout=10).text
    d1 = datetime.strptime(today, "%d-%m-%Y")
    d2 = datetime.strptime(expiryDate, "%d-%m-%Y")
    if d1<=d2:
        return True
    else:
        return False

@app.route("/resubscribe")
def renewSubscription():
    try:
        userData = query[0]
        print(userData)
        if userData['Manager'] == 'adminMgcoder':
            return render_template('jazzcash.html')
        if userData['Manager'] == 'Shams':
            
            return """
            <h2>Contact us:</h2>
            <p>Email:  ronisham39@gmail.com</p>
            <p>WhatsAPP:  +880-1998-561257</p>
            <p>Telegram:  @shams1739</p>"""
    except:
        return redirect('/')

    
def gettingUserData(username):
    global query
    for _ in range(5): # try 5 times if fail.
        try:
            query = [info for info in sheet.get_all_records() if info['Username'] == username]
            return query[0]
        except:
            pass
    return None


def validateUser(username, password):
    UserData = gettingUserData(username)
    if UserData:
        User_status,expiryDate,Id=UserData['Status'],UserData['ExpireDate'],UserData['Email']
        if User_status ==1:
            if userSubscription(expiryDate):
                return redirect(url_for('welcome', info={Id:password}))
            else:
                return redirect(url_for('expired'))
        else:
            return "<h3>You are temprary paused due to some reason. Contact to the service provider</h3>"
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)





