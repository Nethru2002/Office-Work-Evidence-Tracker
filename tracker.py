import os
import time
import csv
import pyautogui
import pygetwindow as gw
from datetime import datetime

class TaskTracker:
    def __init__(self, output_dir="Work_Proof"):
        self.output_dir = output_dir
        self.logs_dir = os.path.join(self.output_dir, "Logs")
        self.screenshots_dir = os.path.join(self.output_dir, "Screenshots")
        self.is_running = False
        
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def get_active_window(self):
        try:
            window = gw.getActiveWindow()
            return window.title if window else "Idle/Desktop"
        except:
            return "Unknown"

    def log_activity(self, task_name, window_title):
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"Activity_Log_{date_str}.csv")
        
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Task Name", "Active Window"])
            writer.writerow([datetime.now().strftime("%H:%M:%S"), task_name, window_title])

    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join(self.screenshots_dir, f"Proof_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

    def start_monitoring(self, task_name, interval=60, screenshot_interval=300):
        self.is_running = True
        print(f"Monitoring started for: {task_name}")
        
        last_screenshot_time = 0
        
        while self.is_running:
            current_window = self.get_active_window()
            self.log_activity(task_name, current_window)
            
            if time.time() - last_screenshot_time >= screenshot_interval:
                self.take_screenshot()
                last_screenshot_time = time.time()
                
            time.sleep(interval)

    def stop_monitoring(self):
        self.is_running = False