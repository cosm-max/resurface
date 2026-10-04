import sqlite3
import os

DB_PATH = "resurface.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
            summary TEXT,
            date TEXT,
            time TEXT,
            location TEXT,
            action TEXT,
            expired BOOLEAN,
            status TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_item(item_data, image_path):
    category = item_data.get('category', 'none')
    status = "unsorted" if category == "none" else "sorted"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (
            category, title, summary, date, time, location, action, expired, status, image_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        category,
        item_data.get('title'),
        item_data.get('summary'),
        item_data.get('date'),
        item_data.get('time'),
        item_data.get('location'),
        item_data.get('action'),
        item_data.get('expired', False),
        status,
        image_path
    ))
    conn.commit()
    conn.close()
