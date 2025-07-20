import tkinter as tk
from tkinter import ttk
import threading, time, queue, os, tempfile, requests, sounddevice as sd, numpy as np, scipy.io.wavfile
import pyautogui, pyperclip
from pynput import mouse, keyboard

# ───────── THEME ───────── #
COL_BG        = "#0b0d17"   # deep navy background
COL_CARD      = "#111426"   # slightly lighter card / panel
COL_PRIMARY   = "#8f2bff"   # violet‑pink (idle button colour)
COL_PRIMARY_2 = "#4266ff"   # indigo‑blue (active/recording)
COL_ACCENT    = "#ff4dff"   # hot‑pink accent (macro button)

COL_TEXT      = "#ffffff"
COL_SUBTEXT   = "#c7c7d9"

FONT_MAIN  = ("Inter", 22)
FONT_BTN   = ("Inter", 13, "bold")
FONT_SMALL = ("Inter", 11)

# ───────── CONFIG ───────── #
SERVER_URL = "http://localhost:8000/transcribe"  # Replace with your server's IP and port
KILL_COMBO = {keyboard.Key.ctrl_l, keyboard.Key.shift_l, keyboard.KeyCode(char='q')}

# ───── GLOBAL STATE ───── #
macro            = []          # recorded steps
recording_flag   = [False]
audio_q          = queue.Queue()
_keys_held       = set()

# ───── EMERGENCY KILL ───── #

def _kill_press(key):
    if key in KILL_COMBO:
        _keys_held.add(key)
        if _keys_held >= KILL_COMBO:
            os._exit(1)

def _kill_release(key):
    _keys_held.discard(key)

keyboard.Listener(on_press=_kill_press, on_release=_kill_release).start()

# ───────── VOICE RECORDING ───────── #

def _audio_callback(indata, frames, t, status):
    if recording_flag[0]:
        audio_q.put(indata.copy())


def record_until_toggle(path, sr=16_000):
    frames = []
    with sd.InputStream(samplerate=sr, channels=1, dtype='int16', callback=_audio_callback):
        while recording_flag[0]:
            try:
                frames.append(audio_q.get(timeout=0.1))
            except queue.Empty:
                pass
    if not frames:
        return False
    audio = np.concatenate(frames, axis=0)
    scipy.io.wavfile.write(path, sr, audio)
    return True


def send_audio(path):
    with open(path, 'rb') as f:
        r = requests.post(SERVER_URL, files={'file': f})
    return r.json().get('text', '<err>') if r.ok else '<err>'

# ────────── MACRO RECORD / PLAY ────────── #

def record_macro():
    """Record mouse clicks and Ctrl+V presses until the user hits the S key."""
    macro.clear()
    status_lbl.config(text="⏺  Recording macro…  (press 's' to stop)")
    start = time.time()
    stop_record = {"flag": False}

    def on_click(x, y, btn, pressed):
        if stop_record["flag"]:
            return False
        if pressed:
            macro.append({"t": time.time() - start, "type": "mouse", "data": (x, y, btn)})

    def on_press(key):
        if isinstance(key, keyboard.KeyCode) and key.char == 's':
            stop_record["flag"] = True
            return False
        _keys_held.add(key)

    def on_release(key):
        V_VK = 0x56  # 'V'
        if isinstance(key, keyboard.KeyCode) and key.vk == V_VK and (keyboard.Key.ctrl_l in _keys_held or keyboard.Key.ctrl_r in _keys_held):
            macro.append({"t": time.time() - start, "type": "hotkey", "data": ("ctrl", "v")})
        _keys_held.discard(key)

    ml = mouse.Listener(on_click=on_click)
    kl = keyboard.Listener(on_press=on_press, on_release=on_release)
    ml.start(); kl.start(); ml.join(); kl.join()

    if macro:
        listen_btn.config(state=tk.NORMAL, bg=COL_PRIMARY)
        copy_btn.config(state=tk.NORMAL, bg=COL_CARD)
        status_lbl.config(text=f"✅ Macro captured ({len(macro)} steps).")
    else:
        status_lbl.config(text="⚠️  No steps captured – try again.")


def play_macro(text):
    if not macro:
        return
    pyperclip.copy(text)
    t0 = time.time()
    for step in macro:
        while time.time() - t0 < step["t"]:
            time.sleep(0.002)
        if step["type"] == "mouse":
            x, y, btn = step["data"]
            pyautogui.moveTo(x, y)
            pyautogui.click()
        elif step["type"] == "hotkey":
            pyautogui.hotkey(*step["data"])

# ───────── GUI CALLBACKS ───────── #

def toggle_recording(_evt=None):
    if recording_flag[0]:
        recording_flag[0] = False
        listen_btn.config(text="🎤  Listen", bg=COL_PRIMARY)
        status_lbl.config(text="🎤 Idle")
    else:
        if not macro:
            status_lbl.config(text="⚠️  Record a macro first!")
            return
        recording_flag[0] = True
        listen_btn.config(text="🔴  Recording…", bg=COL_PRIMARY_2)
        status_lbl.config(text="🎙  Listening…  press Space to stop")
        threading.Thread(target=process_audio_flow, daemon=True).start()


def process_audio_flow():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name
    if not record_until_toggle(wav_path):
        listen_btn.config(text="🎤  Listen", bg=COL_PRIMARY)
        status_lbl.config(text="⚠️  Recording cancelled.")
        return
    txt = send_audio(wav_path)
    os.remove(wav_path)

    txtbox.config(state=tk.NORMAL)
    txtbox.delete("1.0", tk.END)
    txtbox.insert(tk.END, txt)
    txtbox.config(state=tk.DISABLED)

    play_macro(txt)
    listen_btn.config(text="🎤  Listen", bg=COL_PRIMARY)
    status_lbl.config(text="✅  Done. Ready.")


def copy_transcript():
    text = txtbox.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        status_lbl.config(text="📋  Transcript copied.")

# ───────── GUI BUILD ───────── #
root = tk.Tk()
root.title("The Golem")
root.geometry("560x500")
root.configure(bg=COL_BG)
root.bind('<space>', toggle_recording)

style = ttk.Style()
style.theme_use('clam')
style.configure("Horizontal.TScale", troughcolor=COL_CARD, background=COL_ACCENT)

macro_btn = tk.Button(root, text="🎬  Record Macro", font=FONT_BTN, bg=COL_ACCENT, fg=COL_TEXT,
                      command=lambda: threading.Thread(target=record_macro, daemon=True).start(),
                      relief="flat", bd=0, highlightthickness=0)
macro_btn.pack(pady=6)

listen_btn = tk.Button(root, text="🎤  Listen", font=FONT_MAIN, bg=COL_PRIMARY, fg=COL_TEXT,
                       activebackground=COL_PRIMARY_2, activeforeground=COL_TEXT,
                       command=toggle_recording, state=tk.DISABLED, relief="flat", bd=0, highlightthickness=0)
listen_btn.pack(pady=16)

copy_btn = tk.Button(root, text="📋  Copy Transcript", font=FONT_BTN, bg=COL_CARD, fg=COL_TEXT,
                     command=copy_transcript, state=tk.DISABLED, relief="flat", bd=0, highlightthickness=0)
copy_btn.pack(pady=4)

txtbox = tk.Text(root, height=11, width=60, font=("Inter", 12), wrap=tk.WORD,
                 bg=COL_CARD, fg=COL_TEXT, insertbackground=COL_TEXT, relief="flat", borderwidth=0)
txtbox.pack(pady=10)
txtbox.config(state=tk.DISABLED)

status_lbl = tk.Label(root, text="🎤 Idle", font=FONT_SMALL, bg=COL_BG, fg=COL_SUBTEXT)
status_lbl.pack(pady=4)

root.mainloop()
