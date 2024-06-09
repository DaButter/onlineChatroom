from flask import Flask, render_template, redirect, request, session
from datetime import datetime
import json
import sqlite3
import create_table_user_logins

# Flask app init
app = Flask('app')
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'your_secret_key'

# Landing page
@app.route('/')
def landing():
  return render_template('landing.html')


# Chatroom page
@app.route('/chats')
def chatroom():
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    return render_template("chatroom.html", username=username)


# Update chat messages
@app.route('/read_msg')
def read_msg():
  with open('data/messages.json', 'r', encoding="utf-8") as f:
    messages = f.read()
  return messages


# Send and save new message
@app.route('/send/<name>/<message>')
def send(name, message):
    timestamp = datetime.now().strftime("%d.%m.%Y. %H:%M:%S")

    new_msg = {
        "username": name,
        "message": message,
        "time": timestamp
    }
    print(new_msg)

    con = sqlite3.connect('chatroom_data.db')
    c = con.cursor()
    c.execute("INSERT INTO chat (username, message, time) VALUES (?, ?, ?)", (name, message, timestamp))
    con.commit()
    con.close()

    with open("data/messages.json", "r+", encoding="utf-8") as file:
        msgs = json.load(file)
        msgs.append(new_msg)
        file.seek(0)
        json.dump(msgs, file, indent=2, ensure_ascii=False)
        file.truncate()

    return "OK"


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        con = sqlite3.connect('chatroom_data.db')
        c = con.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        con.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect('/chats')
        else:
            return render_template('login.html', error='Invalid username or password!')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username'].lower()
    password = request.form['password']

    con = sqlite3.connect('chatroom_data.db')
    c = con.cursor()

    # Check if user already exists in table
    c.execute("SELECT * FROM users WHERE username=?", (username, ))
    user = c.fetchone()

    if user:
      # If user exists, print error message
      return render_template('register.html', error='Username already exists!')
    else:
      # If user does not exist, register it to DB
      c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
      con.commit()
      con.close()
      return redirect('/login')
  else:
    return render_template('register.html')


if __name__ == "__main__":
  create_table_user_logins.create_logins_table()
  create_table_user_logins.create_chat_table()

  app.run(host='0.0.0.0', port=8080, debug=True)
