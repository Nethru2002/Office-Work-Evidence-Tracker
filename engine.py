import time
import os
import pyautogui
import pygetwindow as gw
from PIL import Image, ImageDraw
from datetime import datetime
from database import log_event

class AuditEngine:
    def __init__(self):
        self.is_running = False
        self.session_id = ""
        self.last_window = ""
        self.session_path = ""
        self.periodic_interval = 300 
        self.last_periodic_time = 0
        self.capture_count = 0

    def start_session(self):
        self.is_running = True
        self.capture_count = 0
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = os.path.abspath("Proof_Folder")
        self.session_path = os.path.join(base_folder, f"Session_{self.session_id}")
        
        if not os.path.exists(self.session_path):
            os.makedirs(self.session_path, exist_ok=True)
            
        self.last_window = ""
        self.last_periodic_time = time.time()

    def capture_proof(self, app_title, event_type):
        ts_now = datetime.now()
        ts_str = ts_now.strftime("%Y-%m-%d %H:%M:%S")
        file_name = f"SS_{ts_now.strftime('%H%M%S')}.png"
        path = os.path.join(self.session_path, file_name)
        
        try:
            ss = pyautogui.screenshot()
            draw = ImageDraw.Draw(ss)
            draw.rectangle([0, ss.height - 60, ss.width, ss.height], fill="black")
            stamp_text = f"OFFICIAL PROOF | TIME: {ts_str} | APP: {app_title[:70]} | EVENT: {event_type}"
            draw.text((20, ss.height - 40), stamp_text, fill="white")
            
            ss.save(path)
            log_event(self.session_id, app_title, event_type, path)
            self.capture_count += 1
            return path
        except Exception as e:
            print(f"Capture Error: {e}")
            return None

    def monitor_loop(self, ui_update_callback):
        while self.is_running:
            try:
                active_window = gw.getActiveWindow()
                current_title = active_window.title if active_window else "Desktop"
            except:
                current_title = "Transitioning..."

            if current_title != self.last_window:
                event = "WINDOW_SWITCH" if self.last_window != "" else "SESSION_START"
                self.capture_proof(current_title, event)
                self.last_window = current_title
                self.last_periodic_time = time.time()
                ui_update_callback(current_title, "App Switch")

            if time.time() - self.last_periodic_time >= self.periodic_interval:
                self.capture_proof(current_title, "PERIODIC_AUDIT")
                self.last_periodic_time = time.time()
                ui_update_callback(current_title, "Timer Audit")

            time.sleep(1)

    def stop_session(self):
        self.is_running = False