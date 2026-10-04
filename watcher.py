import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        
    def on_created(self, event):
        if not event.is_directory:
            ext = os.path.splitext(event.src_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg']:
                # Wait a little for file to write completely
                time.sleep(0.5)
                self.callback(event.src_path)

def start_watching(folder_path, callback):
    event_handler = ScreenshotHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    return observer
