import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import threading
import os
from datetime import datetime

# ------------------------------------------------------------
# 1. Haar cascades (global)
# ------------------------------------------------------------
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
SMILE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)

SMILE_CONFIDENCE = 55          # higher = stricter


def detect_smile(frame: np.ndarray) -> bool:
    """Return True if a confident smile is found."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
    )
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        smiles = SMILE_CASCADE.detectMultiScale(
            roi_gray,
            scaleFactor=1.7,
            minNeighbors=SMILE_CONFIDENCE,
            minSize=(25, 25),
        )
        if len(smiles) > 0:
            return True
    return False


# ------------------------------------------------------------
# 2. GUI + webcam thread
# ------------------------------------------------------------
class SmileCaptureApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smile-Capture")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # ---- UI elements ----
        self.lbl_video = ttk.Label(root)
        self.lbl_video.pack(padx=10, pady=10, expand=True, fill="both")

        # Buttons frame
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_start = ttk.Button(btn_frame, text="Start Webcam", command=self.start_webcam)
        self.btn_start.pack(side="left", padx=5)

        self.btn_stop = ttk.Button(btn_frame, text="Stop Webcam", command=self.stop_webcam, state="disabled")
        self.btn_stop.pack(side="left", padx=5)

        self.lbl_status = ttk.Label(root, text="Press 'Start Webcam' to begin", foreground="blue")
        self.lbl_status.pack(pady=5)

        # ---- State ----
        self.cap: cv2.VideoCapture | None = None
        self.running = False
        self.photo_dir = "captured_photos"
        os.makedirs(self.photo_dir, exist_ok=True)

    # --------------------------------------------------------
    def start_webcam(self):
        if self.running:
            return

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        self.running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.lbl_status.config(text="Webcam ON – smile to capture!", foreground="green")

        # start video loop in a background thread
        threading.Thread(target=self._video_loop, daemon=True).start()

    # --------------------------------------------------------
    def stop_webcam(self):
        self.running = False          # <-- this will break the while loop

    # --------------------------------------------------------
    def _video_loop(self):
        smile_detected = False
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            # mirror
            frame = cv2.flip(frame, 1)

            # draw face rectangles
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 215, 0), 2)

            # smile detection + capture
            if not smile_detected and detect_smile(frame):
                smile_detected = True
                self.root.after(0, self._capture_photo, frame.copy())
            elif smile_detected and not detect_smile(frame):
                smile_detected = False

            # show in GUI
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((720, 540), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_video.config(image=photo)
            self.lbl_video.image = photo   # keep reference

        self._cleanup()

    # --------------------------------------------------------
    def _capture_photo(self, frame: np.ndarray):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.photo_dir, f"smile_{timestamp}.jpg")
        cv2.imwrite(filename, frame)

        self.lbl_status.config(
            text=f"SMILE! Photo saved → {os.path.basename(filename)}",
            foreground="purple",
        )

        # ---- flash effect (optional) ----
        flash = tk.Toplevel(self.root)
        flash.configure(bg="white")
        flash.geometry("200x100")
        flash.overrideredirect(True)          # no title bar
        flash.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        x = (w - 200) // 2
        y = (h - 100) // 2
        flash.geometry(f"200x100+{x}+{y}")
        flash.after(200, flash.destroy)

    # --------------------------------------------------------
    def _cleanup(self):
        if self.cap:
            self.cap.release()
            self.cap = None

        self.running = False
        self.root.after(0, lambda: self.btn_start.config(state="normal"))
        self.root.after(0, lambda: self.btn_stop.config(state="disabled"))
        self.root.after(
            0,
            lambda: self.lbl_status.config(
                text="Webcam stopped. Press 'Start Webcam' again.", foreground="blue"
            ),
        )

    # --------------------------------------------------------
    def on_closing(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


# ------------------------------------------------------------
# 3. Run the app
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SmileCaptureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()