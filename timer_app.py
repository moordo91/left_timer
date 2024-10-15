import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from utils import format_time

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("남은 시간 계산기")
        self.root.resizable(False, False)
        
        self.after_id = None
        self.timer_expired = False
        self.target_time = None
        
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)
        
        for i in range(3):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        
        # 날짜 입력
        self.date_entry = ttk.Entry(frame, font=("Jetbrains mono", 16))
        self.date_entry.grid(row=0, column=0, columnspan=3, padx=0, pady=5, sticky="EW")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # 시간 입력
        now = datetime.now()
        self.hour_spinbox = self.create_spinbox(frame, 0, 23, now.hour, 1, 0)
        self.minute_spinbox = self.create_spinbox(frame, 0, 59, now.minute, 1, 1)
        self.second_spinbox = self.create_spinbox(frame, 0, 59, 0, 1, 2)
        
        # 버튼 프레임
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        sb_style = ttk.Style()
        sb_style.configure("TButton", font=("Jetbrains Mono", 16))
        
        start_button = ttk.Button(
            buttons_frame, text="Start", command=self.start_timer, style="TButton"
        )
        start_button.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="E")
        
        reset_button = ttk.Button(
            buttons_frame, text="Reset", command=self.reset_timer, style="TButton"
        )
        reset_button.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="W")
        
        # 타이머 표시
        self.timer_label = tk.Label(self.root, text="+00:00:00", font=("Jetbrains mono", 40))
        self.timer_label.pack(padx=5, pady=(0, 20))
    
    def create_spinbox(self, parent, from_, to, value, row, column):
        spinbox = ttk.Spinbox(
            parent, from_=from_, to=to, width=4, format="%02.0f", font=("Jetbrains mono", 16)
        )
        spinbox.set(value)
        spinbox.grid(row=row, column=column, pady=5)
        return spinbox
    
    def start_timer(self):
        self.reset_timer()
        date_str = self.date_entry.get()
        hour = self.hour_spinbox.get()
        minute = self.minute_spinbox.get()
        second = self.second_spinbox.get()
        
        target_time_str = f"{date_str} {hour}:{minute}:{second}"
        try:
            self.target_time = datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            if self.target_time <= now:
                self.root.bell()
                messagebox.showerror("Error", "현재 시간 이후의 시간을 입력해주세요.")
                return
            self.timer_expired = False
            self.update_timer()
        except ValueError as e:
            self.root.bell()
            messagebox.showerror("Invalid format", f"잘못된 형식입니다.\n{e}")
    
    def update_timer(self):
        now = datetime.now()
        delta = self.target_time - now
        total_seconds = int(delta.total_seconds())
        time_str = format_time(total_seconds)
        self.timer_label.config(text=time_str)
        
        if total_seconds < 0 and not self.timer_expired:
            self.timer_expired = True
            self.times_up()
        
        self.after_id = self.root.after(1000, self.update_timer)
    
    def times_up(self):
        self.root.bell()
        messagebox.showinfo("Timer", "Time's up!")
    
    def reset_timer(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.timer_label.config(text="+00:00:00")
        self.timer_expired = False
    
    def run(self):
        self.root.mainloop()