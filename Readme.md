# Smile-Capture: Real-Time Smile-Triggered Photography Using OpenCV

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![OpenCV](https://img.shields.io/badge/OpenCV-4.10-green)](https://opencv.org/) [![Tkinter](https://img.shields.io/badge/Tkinter-8.6-orange)](https://docs.python.org/3/library/tkinter.html) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a PGDIT course assignment for Course PGDIT-114 (Artificial Intelligence and Neural Network). A real-time desktop application that captures photos using your webcam **only when you smile**. Built with Python, it combines computer vision for smile detection and a clean GUI for live preview. Perfect for hands-free selfies, demos, or emotion-aware tech prototypes.

## Features
- **Real-Time Smile Detection**: Uses OpenCV Haar Cascades to spot smiles in frontal faces.
- **Auto-Capture**: Snaps high-res JPEGs on smile detection (with debouncing to avoid duplicates).
- **Live Preview**: Mirror-flipped video feed with face outlines for instant feedback.
- **User-Friendly GUI**: Start/Stop buttons, status updates, and a subtle flash effect.
- **Easy Setup**: Runs locally on Windows/Mac/Linux; no cloud or extra hardware needed.
- **Customizable**: Tune detection sensitivity and add extensions like multi-face support.

## Tech Stack
- **Core**: Python 3.8+, OpenCV (image processing & detection)
- **GUI**: Tkinter + PIL (image conversion & display)
- **Utils**: NumPy (array handling), Threading (non-blocking video)

## Installation

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/amanullahradiant/assignment-smile-detection-and-capture.git
   cd assignment-smile-detection-and-capture
   ```

2. **Set Up Virtual Environment** (Recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(requirements.txt includes: opencv-python==4.10.0.84, numpy==2.1.2, Pillow==10.4.0)*

4. **Run the App**:
   ```bash
   python main.py
   ```
   - Click **Start Webcam** → Smile → Watch the magic! Photos save to `captured_photos/`.

## Usage
1. Launch the app – a window opens with a blank preview and controls.
2. Hit **Start Webcam** to begin live feed (face rectangles appear on detection).
3. Smile confidently – the app flashes white and saves a timestamped photo (e.g., `smile_20251116_105000.jpg`).
4. Use **Stop Webcam** to pause; close the window for clean exit.

**Pro Tip**: For stricter detection, edit `SMILE_CONFIDENCE = 55` in `main.py` (higher = fewer false positives).


## Contributors
This project was built collaboratively by our awesome team of PGDIT students from **Jahangirnagar University:**

- **Md Amanullah Parvez** (25102) 
- **Md. Mizanur Rahaman** (25109)
- **Md. Mamunur Rushid** (25110)
- **Foysal Hasib** (25111)
- **Md. Shahidul Alom Siddiki** (25114)


## Supervisor
- Dr. Shamim Al Mamun (Professor, Institute of Information Technology, Jahangirnagar University)


## Acknowledgments
- OpenCV team for Haar Cascades.
- Tkinter docs for seamless GUI.
- Inspired by real-time emotion AI demos.


Star ⭐ the repo if it brings a smile to your face! 😄

---
