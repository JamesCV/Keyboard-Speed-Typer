import sqlite3
from datetime import datetime

#database handling
db = sqlite3.connect('db/app.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, coins INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, difficulty TEXT, time REAL, wpm REAL, mistakes INTEGER, map TEXT, date TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, name TEXT, status TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, difficulty TEXT, dimensions TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))''')
db.commit()

def launchDBconnection():
    db = sqlite3.connect('db/app.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, coins INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, difficulty TEXT, time REAL, wpm REAL, mistakes INTEGER, map TEXT, date TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, name TEXT, status TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, difficulty TEXT, dimensions TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))''')
    db.commit()

def getLeaderboardRows():
    cursor.execute("SELECT * FROM games ORDER BY wpm DESC LIMIT 10")
    return cursor.fetchall()

def getPerformance():
    cursor.execute("SELECT * FROM games ORDER BY id DESC LIMIT 50")
    return cursor.fetchall()

def getCoins():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

def updateCoins(coins):
    cursor.execute("UPDATE users SET coins=? WHERE id=1", (coins,))
    db.commit()

def createUserProfile():
    cursor.execute("INSERT INTO users (coins) VALUES (?)", (0,))
    db.commit()

def getHistoryRows():
    cursor.execute("SELECT * FROM games ORDER BY date DESC LIMIT 10")
    return cursor.fetchall()

def getInventory():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

def unlockCar(name, selected):
    cursor.execute("INSERT INTO inventory (name, status, user_id) VALUES (?, ?, ?)", (name, "selected", 1))
    db.commit()

def changeSelectedCarInDB(oldcar, newcar):
    cursor.execute("UPDATE inventory SET status='unselected' WHERE name=?", (oldcar,))
    db.commit()
    cursor.execute("UPDATE inventory SET status='selected' WHERE name=?", (newcar,))
    db.commit()

def insertRecord(difficulty, time, wpm, mistakes, map):
    date = str(datetime.now().strftime("%m-%d"))
    cursor.execute("INSERT INTO games (difficulty, time, wpm, mistakes, map, date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (difficulty, time, wpm, mistakes, map, date, 1))
    db.commit()

def setSettings(dimensions, difficulty):
    cursor.execute("INSERT OR REPLACE INTO settings (id, dimensions, difficulty, user_id) VALUES (?, ?, ?, ?)",(0, dimensions, difficulty, 1))
    db.commit()

def getSettings():
    cursor.execute("SELECT * FROM settings WHERE id = 0")
    return cursor.fetchone()
