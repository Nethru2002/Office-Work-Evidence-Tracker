---

# 📋 ProTracker: Professional Office Audit & Evidence System

**ProTracker** is a high-precision, automated task monitoring tool developed to provide undeniable visual and chronological proof of work activity. Designed for professionals who need to verify their productivity to office authorities, it combines real-time window tracking, automated watermarked screenshots, and professional PDF report generation.

---

## ✨ Key Features

*   **Instant Switch Detection:** Captures a screenshot and logs the event the millisecond you switch between applications or websites.
*   **Visual Watermarking:** Every screenshot is automatically stamped with a "Proof Bar" containing the exact Timestamp, Application Name, and Event Type.
*   **Professional PDF Reporting:** Compiles an entire work session into a single, clean PDF document with embedded images, ready to be sent to management.
*   **Work Intensity Metrics:** Tracks total session duration and the number of evidence captures made.
*   **Periodic Audits:** Even if you stay on one screen for a long time, the tool takes a "heartbeat" screenshot every 5 minutes to prove you are still active.
*   **Privacy-First:** All data, logs, and images are stored locally on your machine. No data is sent to the cloud.

---

## 🛠️ Project Structure

The tool consists of four modular Python files:

1.  **`main.py`**: The Modern Dashboard UI (built with CustomTkinter).
2.  **`engine.py`**: The background "brain" that monitors windows and captures screenshots.
3.  **`database.py`**: The storage layer that manages the SQLite audit logs.
4.  **`report_generator.py`**: The document engine that compiles logs and images into a PDF.

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10 or higher** installed on your system.

### 2. Install Dependencies
Run the following command in your terminal to install the required professional libraries:

```bash
pip install customtkinter pyautogui pygetwindow reportlab Pillow psutil
```

### 3. File Preparation
Place all four project files (`main.py`, `engine.py`, `database.py`, `report_generator.py`) in a single folder.

---

## 📖 How to Use

1.  **Launch the App:** Run the command:
    ```bash
    python main.py
    ```
2.  **Start a Session:** Click the **"Start Tracking"** button. The dashboard will glow green, and the timer will begin.
3.  **Perform Your Tasks:** Work as you normally would. The tool will silently capture every window change (e.g., switching from Chrome to Excel).
4.  **Stop & Export:** Once finished, click **"Stop & Export PDF"**. 
5.  **View Proof:** The tool will automatically open the session folder containing your watermarked screenshots and the final **Professional PDF Report**.

---

## 🛡️ Proving Your Work to Authorities

This tool is designed to make your work "Audit-Proof":

1.  **The PDF Report:** Instead of sending 50 separate images, you provide one structured PDF document.
2.  **The Watermark:** Because the Timestamp and App Name are baked into the image pixels, it serves as high-integrity evidence that the work happened at that specific time.
3.  **The Audit Log:** The internal SQLite database (`office_audit.db`) maintains a secondary, uneditable record of your activities.

---

## 📂 Data Storage
*   **Logs:** Saved in `office_audit.db`.
*   **Screenshots & Reports:** Saved in `Proof_Folder/Session_YYYYMMDD_HHMMSS/`.

---

## ⚠️ Requirements for Accuracy
*   **Windows OS:** This tool is optimized for Windows window management APIs.
*   **Permissions:** Ensure the terminal/IDE has permission to capture the screen (standard on most Windows setups).

---

## ⚖️ Disclaimer
*This tool is intended for professional self-reporting and transparency between employees and employers. Always ensure you are compliant with your local company's privacy policies regarding screen recording.*

**Developed by Nethru Randev**