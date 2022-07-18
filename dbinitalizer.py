import sqlite3

conn = sqlite3.connect('todolist.db')
print("Opened database todolist successfully");

conn.execute("CREATE TABLE user (user_id INTEGER PRIMARY KEY AUTOINCREMENT,user_name TEXT NOT NULL,password TEXT NOT NULL,email TEXT NOT NULL UNIQUE)")
print("Table user created successfully");

conn.execute("CREATE TABLE todolist (todo_item_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,todo_item TEXT NOT NULL,status TEXT NOT NULL)")
print("Table todolist created successfully");

conn.close()