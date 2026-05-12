import customtkinter as ctk
import threading
import os
import time
from datetime import datetime
from tkinter import messagebox

from engine import AuditEngine
from database import init_db, get_session_history
from report_generator import generate_pdf_report

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        init_db()
        self.engine = AuditEngine()
        
        self.title("ProTracker | Activity Auditor")
        self.geometry("1100x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.brand_lbl = ctk.CTkLabel(self.sidebar, text="PROTRACKER", font=ctk.CTkFont(size=24, weight="bold"))
        self.brand_lbl.pack(pady=(40, 40))

        self.btn_start = ctk.CTkButton(self.sidebar, text="Start Tracking", height=40,
                                       fg_color="#10b981", hover_color="#059669",
                                       font=ctk.CTkFont(weight="bold"), command=self.start_session)
        self.btn_start.pack(pady=10, padx=20, fill="x")

        self.btn_stop = ctk.CTkButton(self.sidebar, text="Stop & Export PDF", height=40,
                                      fg_color="#ef4444", hover_color="#dc2626",
                                      font=ctk.CTkFont(weight="bold"), command=self.stop_session, state="disabled")
        self.btn_stop.pack(pady=10, padx=20, fill="x")

        self.btn_folder = ctk.CTkButton(self.sidebar, text="View All Sessions", height=40,
                                        fg_color="#374151", command=self.open_proof_folder)
        self.btn_folder.pack(pady=(100, 10), padx=20, fill="x")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        self.header_lbl = ctk.CTkLabel(self.main_container, text="System Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        self.header_lbl.pack(anchor="w", pady=(0, 20))

        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)

        self.timer_card = self.create_card(self.stats_frame, "ELAPSED TIME", "00:00:00", 0)
        self.status_card = self.create_card(self.stats_frame, "CURRENT STATUS", "Idle", 1)
        self.capture_card = self.create_card(self.stats_frame, "TOTAL CAPTURES", "0", 2)

        self.app_info_lbl = ctk.CTkLabel(self.main_container, text="Active Window: Standing By...", font=ctk.CTkFont(size=14))
        self.app_info_lbl.pack(anchor="w", pady=(20, 5))

        self.log_box = ctk.CTkTextbox(self.main_container, corner_radius=15, border_width=2, 
                                      border_color="#1f2937", font=("Consolas", 13))
        self.log_box.pack(fill="both", expand=True, pady=10)

    def create_card(self, master, label, value, col):
        card = ctk.CTkFrame(master, corner_radius=15, fg_color="#1f2937", height=120)
        card.grid(row=0, column=col, padx=(0, 20), sticky="nsew")
        master.grid_columnconfigure(col, weight=1)
        
        lbl = ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color="#9ca3af")
        lbl.pack(pady=(15, 0))
        
        val_lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        val_lbl.pack(pady=(5, 15))
        return val_lbl

    def start_session(self):
        self.engine.start_session()
        self.start_time = time.time()
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status_card.configure(text="TRACKING", text_color="#10b981")
        
        threading.Thread(target=self.engine.monitor_loop, args=(self.update_ui_callback,), daemon=True).start()
        self.update_timer()
        self.log_event("Audit Session Initiated")

    def update_timer(self):
        if self.engine.is_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_card.configure(text=time.strftime('%H:%M:%S', time.gmtime(elapsed)))
            self.capture_card.configure(text=str(self.engine.capture_count))
            self.after(1000, self.update_timer)

    def update_ui_callback(self, app_title, event_type):
        self.app_info_lbl.configure(text=f"Active Window: {app_title[:80]}")
        self.log_event(f"{event_type} -> {app_title[:45]}...")

    def log_event(self, message):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {message}\n")
        self.log_box.see("end")

    def stop_session(self):
        self.engine.stop_session()
        self.status_card.configure(text="PROCESSING", text_color="#f59e0b")
        self.update_idletasks()

        history = get_session_history(self.engine.session_id)
        if history:
            try:
                generate_pdf_report(self.engine.session_id, history, self.engine.session_path)
                messagebox.showinfo("Audit Saved", "A professional PDF report has been generated.")
                os.startfile(os.path.abspath(self.engine.session_path))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {e}")
        
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.status_card.configure(text="Idle", text_color="white")
        self.timer_card.configure(text="00:00:00")

    def open_proof_folder(self):
        folder = os.path.abspath("Proof_Folder")
        if not os.path.exists(folder): os.makedirs(folder)
        os.startfile(folder)

if __name__ == "__main__":
    app = ModernTrackerApp()
    app.mainloop()