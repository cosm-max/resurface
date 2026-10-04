import tkinter as tk
from tkinter import messagebox
from plyer import notification

def send_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Resurface",
            timeout=10
        )
    except Exception as e:
        print(f"Notification error (plyer): {e}")
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            messagebox.showinfo(title, message)
            root.destroy()
        except Exception as e2:
            print(f"Notification error (tkinter): {e2}")
