import tkinter as tk
from tkinter import messagebox
from mido import Message, MidiFile, MidiTrack
import os
import random
import math

sequence = ""

def update_display():
    sequence_label.config(text=f"현재 서열: {sequence}")

def add_base(base):
    global sequence
    sequence += base
    update_display()

def reset_sequence():
    global sequence
    sequence = ""
    update_display()
    status_label.config(text="")

def generate_midi():
    global sequence
    status_label.config(text="🎵 GENOMA MUSIC producir 🎵", foreground="blue")

    if not sequence:
        messagebox.showerror("❌ 오류", "먼저 A, T, C, G를 클릭해 DNA 서열을 만드세요!")
        status_label.config(text="")
        return

    # 음계 (C장조 한 옥타브 내)
    c_major = [60, 62, 64, 65, 67, 69, 71]  # C D E F G A B

    # 각 염기서열에 대응되는 음
    base_note_map = {
        'A': [60, 64],   # C, E
        'T': [62, 65],   # D, F
        'C': [67, 60],   # G, C
        'G': [69, 71]    # A, B
    }

    # 악기 설정
    instrument = 4  # Electric Piano 1

    ticks_per_beat = 480
    bpm = 80
    time_per_note = 0.6
    sequence_duration = len(sequence) * time_per_note
    repeat_count = math.ceil(20 / sequence_duration)

    mid = MidiFile()
    mid.ticks_per_beat = ticks_per_beat
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=instrument, time=0))

    for _ in range(repeat_count):
        for base in sequence:
            note = random.choice(base_note_map[base])
            duration = random.choice([240, 480])  # 8분음표 ~ 4분음표
            track.append(Message('note_on', note=note, velocity=70, time=0))
            track.append(Message('note_off', note=note, velocity=70, time=duration))

    filename = "dna_smooth.mid"
    mid.save(filename)
    full_path = os.path.abspath(filename)
    messagebox.showinfo("✅ Terminación", f"¡Generación de música terminada!\n\n📁 저장 위치:\n{full_path}")
    status_label.config(text="🎵 Generación de música terminada 🎵", foreground="green")

# GUI 구성
window = tk.Tk()
window.title("🧬 GENOMA MUSIC SIMULATION🧬")
window.geometry("500x400")
window.resizable(False, False)

tk.Label(window, text="GENOMA MUSIC SIMULATION", font=("Arial", 16, "bold")).pack(pady=10)

sequence_label = tk.Label(window, text="현재 서열: ", font=("Arial", 12))
sequence_label.pack()

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

btn_style = {'width': 5, 'height': 2, 'font': ("Arial", 14)}

tk.Button(button_frame, text="A", bg="#FFDAB9", command=lambda: add_base("A"), **btn_style).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="T", bg="#E6E6FA", command=lambda: add_base("T"), **btn_style).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="C", bg="#E0FFFF", command=lambda: add_base("C"), **btn_style).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="G", bg="#FFFACD", command=lambda: add_base("G"), **btn_style).grid(row=0, column=3, padx=5)

control_frame = tk.Frame(window)
control_frame.pack(pady=10)

tk.Button(control_frame, text="🔁 초기화", command=reset_sequence, font=("Arial", 11)).grid(row=0, column=0, padx=10)
tk.Button(control_frame, text="🎶 음악 생성하기", command=generate_midi, bg="#4682B4", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=10)

status_label = tk.Label(window, text="", font=("Arial", 10))
status_label.pack(pady=10)

tk.Label(window, text="🎧 HANKUK ACADEMY OF FOREIGN STUDIES 🎧", font=("Arial", 9), fg="gray").pack(side="bottom", pady=10)

update_display()
window.mainloop()