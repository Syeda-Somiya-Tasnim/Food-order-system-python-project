import os

import mysql.connector
from flask import Flask, redirect, render_template, request, session

app=Flask(__name__)
app.secret_key=os.urandom(25)

conn=mysql.connector.connect(host="localhost",user="root",password="",database="login")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('signin.html')

@app.route('/choos')
def home():
    if 'user_id' in session:
       return render_template('menu.html')
    else:
       return redirect('/') 

@app.route('/back')
def back():
    if 'user_id' in session:
           return render_template('menu.html')
    else:
       return redirect('login.html') 

@app.route('/loginvalidation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/choose')
    else:
        return redirect('/')

@app.route('/adduser', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES 
    (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' """.format(email))
    myusers=cursor.fetchall()
    session['user_id']=myusers[0][0]
    return redirect('/choos')
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


    
if __name__=="__main__":
    app.run(debug=True)


