import sqlite3
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from db import DB_PATH
from notifier import send_notification

def check_reminders(demo_mode=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM items WHERE status = "sorted" AND expired = 0 AND reminded = 0')
    items = cursor.fetchall()
    
    now = datetime.now()
    
    for item in items:
        should_remind = False
        
        category = item['category']
        item_date_str = item['date']
        
        if category == 'notice':
            continue
            
        if item_date_str:
            try:
                item_date = datetime.strptime(item_date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
                
            if demo_mode:
                if item_date >= now.date():
                    should_remind = True
            else:
                one_day_before = item_date - timedelta(days=1)
                
                if now.date() == one_day_before and now.hour >= 9:
                    should_remind = True
                elif now.date() == item_date and now.hour >= 8:
                    should_remind = True
        else:
            if category == 'to_buy':
                if not demo_mode:
                    days_ahead = 5 - now.weekday()
                    if days_ahead < 0: 
                        days_ahead += 7
                    next_saturday = now.date() + timedelta(days=days_ahead)
                    
                    if now.date() == next_saturday and now.hour >= 10:
                        should_remind = True

        if should_remind:
            title = item['title'] or "Resurface Reminder"
            message = item['action'] or "Time to check this item"
            print(f"Sending reminder: '{title}' - {message}")
            send_notification(title, message)
            
            cursor.execute('UPDATE items SET reminded = 1 WHERE id = ?', (item['id'],))
            conn.commit()

    conn.close()

def start_scheduler(demo_mode=False):
    scheduler = BackgroundScheduler()
    # Check every 10 seconds in demo mode to ensure it fires within 20s
    interval_seconds = 10 if demo_mode else 60
    scheduler.add_job(lambda: check_reminders(demo_mode), 'interval', seconds=interval_seconds)
    scheduler.start()
    return scheduler
