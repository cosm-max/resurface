import os
import threading
from watcher import start_watching
from ui import AppUI
from gemma_client import analyze_image
from db import init_db, insert_item

WATCH_FOLDER = "screenshots"

def on_scan(image_path):
    print(f"Scanning {image_path}...")
    
    def task():
        data = analyze_image(image_path)
        if data:
            print(f"Result: {data}")
            insert_item(data, image_path)
        else:
            print("Failed to analyze image.")
            
    threading.Thread(target=task, daemon=True).start()

def on_ignore(image_path):
    print(f"Ignored {image_path}")

def main():
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)
        
    init_db()
    ui = AppUI()
    
    def new_screenshot_callback(image_path):
        ui.request_popup(image_path, on_scan, on_ignore)
        
    observer = start_watching(WATCH_FOLDER, new_screenshot_callback)
    print(f"Watching '{WATCH_FOLDER}' for new screenshots...")
    print("Press Ctrl+C to exit.")
    
    try:
        ui.run()
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
