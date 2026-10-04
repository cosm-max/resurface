import tkinter as tk
import queue

class AppUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() # Hide main window
        self.queue = queue.Queue()
        self.check_queue()
        
    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                self._show_popup(*task)
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)
        
    def request_popup(self, image_path, on_scan, on_ignore):
        self.queue.put((image_path, on_scan, on_ignore))
        
    def _show_popup(self, image_path, on_scan, on_ignore):
        popup = tk.Toplevel(self.root)
        popup.title("Resurface")
        popup.attributes("-topmost", True)
        popup.geometry("350x120")
        
        lbl = tk.Label(popup, text=f"Scan this screenshot?\n{image_path}", wraplength=330)
        lbl.pack(pady=10)
        
        def handle_scan():
            popup.destroy()
            on_scan(image_path)
            
        def handle_ignore():
            popup.destroy()
            on_ignore(image_path)
            
        btn_scan = tk.Button(popup, text="Scan it", command=handle_scan)
        btn_scan.pack(side=tk.LEFT, padx=30)
        
        btn_ignore = tk.Button(popup, text="Just a screenshot", command=handle_ignore)
        btn_ignore.pack(side=tk.RIGHT, padx=30)
        
        popup.protocol("WM_DELETE_WINDOW", handle_ignore)
        
    def run(self):
        self.root.mainloop()
