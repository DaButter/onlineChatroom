import sqlite3

def create_logins_table():
    conn = sqlite3.connect('chatroom_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)''')
    conn.commit()
    conn.close()

def create_chat_table():
    conn = sqlite3.connect('chatroom_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS chat (
                username TEXT,
                message TEXT,
                time TEXT)''')
    conn.commit()
    conn.close()
