from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), default="username")
    email = db.Column(db.String(200), default="abc@gmail.com")
    password = db.Column(db.String(200), default = "password")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.id

class Chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(200), default="author")
    content = db.Column(db.String(200), default="content")

    def __init__(self, author, content):
        self.author = author
        self.content = content


def getByUsername(username):
    user_list = User.query.all()
    for user in user_list:
        if user.username == username:
            return user
    return None
    
@app.route("/")
def default():
    #db.drop_all()
    db.create_all()
    return render_template('loginPage.html')


@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "" or password == "":
            return render_template('loginPage.html')

        temp = getByUsername(username)

        if temp == None or temp.password != password:
            print('Error: username or password incorrect!')
            return render_template('loginPage.html')
        
        try:
            return redirect('/profile/'+username)
        except:
            return 'Error: username or password incorrect'
    else:      
        return render_template('loginPage.html')


@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if username == "" or password == "":
            print("Error: fill out all entries!")
            return render_template('register.html')

        if password != password2:
            print("Error: passwords do not match")
            return render_template('register.html')

        new_user = User(username, email, password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/profile/'+username)
        except:
            return 'There was an issue'
    else:      
        return render_template('register.html')

@app.route("/profile/<username>")
def profile(username):
    try:
        user = getByUsername(username)       
        return render_template('chat_page.html', username = user.username)
    except:
        return 'There was an issue'

@app.route("/logout/")
def unlogger():
    return render_template('logoutPage.html')

@app.route("/new_message/", methods=["POST"])
def new_message():
    if request.method == 'POST':
        username = request.form['username']
        msg = request.form['new_message']

        new_chat = Chat(username, msg)
        
        try:
            db.session.add(new_chat)
            db.session.commit()
            return redirect('/profile/'+username)
        except:
            return 'There was an issue'
    
    return redirect('/profile/'+username)

@app.route("/messages/")
def messages():
    lst = []
    chats = Chat.query.all()
    
    for chat in chats:
        temp = { "author":str(chat.author), "content":str(chat.content) }
        lst.append(temp)

    s = {"chats": lst}
    s = json.dumps(s)

    return s


if __name__ == "__main__":
    app.run(debug=True)