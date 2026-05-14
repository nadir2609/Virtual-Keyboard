# Virtual Keyboard Using Computer Visiob

Python project that lets you type without touching a keyboard.
Your webcam tracks your hand, shows an on-screen keyboard, and presses keys when you:

- **Pinch** your thumb and index finger, or
- **Hover (dwell)** over a key for a short time.

It is built with **OpenCV**, **MediaPipe**, and **pynput**.

---

## Features

- Live hand tracking (single hand)
- On-screen full keyboard layout
- Two click modes:
  - **Pinch click**
  - **Dwell click** (with progress bar)
- `SHIFT` (one-shot) and `CAPS` support
- `BACK`, `TAB`, `SPACE`, `CLEAR` special keys
- `GOOGLE` key to search typed text in browser

---

## Project Structure

```text
Virtual-Keyboard/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── hand_tracking.py
│   ├── gesture.py
│   ├── dwell_click.py
│   ├── keyboard_ui.py
│   └── input_handler.py
├── models/
│   └── hand_landmarker.task
├── images/
│   └── google2.png
├── requirements.txt
└── README.md
```

---

## Requirements

- Python **3.10+** (project currently uses Python 3.12 in local venv)
- Webcam
- Windows/macOS/Linux

---

## Setup

### 1. Clone oproject

```powershell
git clone https://github.com/nadir2609/Virtual-Keyboard.git
```

### 2. Create virtual environment

```powershell
python -m venv env
```

### 3. Activate virtual environment

**Windows (PowerShell):**

```powershell
.\env\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
env\Scripts\activate.bat
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## How to Run

From the project root:

```powershell
python .\src\main.py
```

- Press **Q** to quit.
- A fullscreen window named **Virtual Keyboard** will open.

---

## Configuration (Optional)

Edit `src/config.py` to tune behavior:

- `INPUT_MODE = "pinch" | "dwell" | "pinch_or_dwell"`
- `CLICK_THRESHOLD` (pinch sensitivity)
- `DWELL_TIME_MS` (hover time before click)
- `DWELL_MOVE_TOLERANCE` (allowed finger movement during dwell)
- `CAMERA_ID` (change if webcam index is different)

---

## How It Works (Simple Flow)

1. Read frame from webcam.
2. Detect hand landmarks using MediaPipe model (`models/hand_landmarker.task`).
3. Smooth landmark points to reduce jitter.
4. Find which key your index finger is hovering.
5. Trigger key press from pinch and/or dwell logic.
6. Send real key events with `pynput` and update typed text UI.

---

## Troubleshooting

- **No hand detected**: improve lighting and keep your hand centered.
- **Wrong camera opens**: set `CAMERA_ID` in `src/config.py` (`0`, `1`, etc.).
- **Typing is too sensitive**: increase `CLICK_THRESHOLD` (pinch) or `DWELL_TIME_MS` (dwell).
- **Permissions issue on Linux/macOS**: allow accessibility/input-control permissions for Python.
