import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from threading import Thread, Lock
import os
import time
import random
from queue import Queue
from PIL import Image, ImageTk
import sys
import webbrowser
import re
from webdriver_manager.chrome import ChromeDriverManager

# Modern Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MinnoşCheckerFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Config
        self.title(f"Minnoş Checker Final")
        self.geometry("900x700")
        self.minsize(850, 650)
        
        # State
        self.running = False
        self.lock = Lock()
        self.valid_count = 0
        self.invalid_count = 0
        
        # UI
        self.setup_ui()
        
        # Auto config
        self.check_dependencies()
    
    def setup_ui(self):
        """Ultra modern UI design"""
        # Header
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        # Logo
        try:
            self.logo_img = ctk.CTkImage(light_image=Image.open("logo.png"), size=(180, 40))
            ctk.CTkLabel(self.header, image=self.logo_img, text="").pack(side="left", padx=20)
        except:
            ctk.CTkLabel(self.header, text="Minnoş Checker Final", font=("Arial", 18, "bold")).pack(side="left", padx=20)
        
        # Main content
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=(0,15))
        
        # Input section
        self.setup_input_section()
        
        # Results
        self.setup_results_section()
        
        # Status bar
        self.status = ctk.CTkLabel(self, text="Hazır", height=30, 
                                 fg_color=("#EEEEEE", "#333333"), 
                                 text_color=("#333333", "#EEEEEE"))
        self.status.pack(fill="x", side="bottom")
    
    def setup_input_section(self):
        """Compact input section"""
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=10, pady=10)
        
        # Tabs
        self.tabs = ctk.CTkTabview(frame, width=400, height=120)
        self.tabs.pack()
        
        # File tab
        tab1 = self.tabs.add("Dosya")
        self.file_entry = ctk.CTkEntry(tab1, placeholder_text="combo.txt")
        self.file_entry.pack(fill="x", pady=5)
        ctk.CTkButton(tab1, text="Gözat", width=80, command=self.browse_file).pack()
        
        # Manual tab
        tab2 = self.tabs.add("Manuel")
        self.manual_entry = ctk.CTkEntry(tab2, placeholder_text="kullanici:sifre")
        self.manual_entry.pack(fill="x", pady=5)
        
        # Proxy section
        proxy_frame = ctk.CTkFrame(frame)
        proxy_frame.pack(fill="x", pady=5)
        
        self.proxy_entry = ctk.CTkEntry(proxy_frame, placeholder_text="proxy.txt (opsiyonel)")
        self.proxy_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        ctk.CTkButton(proxy_frame, text="Gözat", width=80, command=self.browse_proxy).pack(side="right")
        
        # Controls
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=5)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="Başlat", 
                                     fg_color="#4CAF50", hover_color="#45a049",
                                     command=self.start_checking)
        self.start_btn.pack(side="left", expand=True, padx=2)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="Durdur", 
                                    fg_color="#f44336", hover_color="#d32f2f",
                                    state="disabled", command=self.stop_checking)
        self.stop_btn.pack(side="left", expand=True, padx=2)
        
        self.clear_btn = ctk.CTkButton(btn_frame, text="Logları Temizle", 
                                     fg_color="#FF9800", hover_color="#F57C00",
                                     command=self.clear_logs)
        self.clear_btn.pack(side="left", expand=True, padx=2)
        
        self.save_btn = ctk.CTkButton(btn_frame, text="Sonuçları Kaydet", 
                                   fg_color="#9C27B0", hover_color="#7B1FA2",
                                   command=self.save_results)
        self.save_btn.pack(side="left", expand=True, padx=2)
    
    def setup_results_section(self):
        """Modern results display"""
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        
        # Stats
        stats_frame = ctk.CTkFrame(frame, height=40)
        stats_frame.pack(fill="x", pady=(0,5))
        
        self.valid_label = ctk.CTkLabel(stats_frame, text="Geçerli: 0", width=100)
        self.valid_label.pack(side="left", padx=5)
        
        self.invalid_label = ctk.CTkLabel(stats_frame, text="Geçersiz: 0", width=100)
        self.invalid_label.pack(side="left", padx=5)
        
        # Results
        self.results = ctk.CTkTextbox(frame, wrap="none", font=("Consolas", 11))
        self.results.pack(fill="both", expand=True)
    
    def check_dependencies(self):
        """Check required components"""
        try:
            ChromeDriverManager().install()
        except Exception as e:
            self.log(f"HATA: {str(e)}", "error")
    
    def log(self, message, type="info"):
        """Advanced logging"""
        colors = {
            "info": "#FFFFFF",
            "success": "#4CAF50",
            "error": "#f44336",
            "warning": "#FFC107"
        }
        
        self.results.configure(state="normal")
        self.results.insert("end", message + "\n", type)
        self.results.tag_config(type, foreground=colors[type])
        self.results.see("end")
        self.results.configure(state="disabled")
    
    def browse_file(self):
        """File browser"""
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, filename)
    
    def browse_proxy(self):
        """Proxy browser"""
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.proxy_entry.delete(0, "end")
            self.proxy_entry.insert(0, filename)
    
    def validate_input(self, text):
        """Kullanıcı:şifre formatını kontrol et"""
        return re.match(r"^[^:]+:.+$", text) is not None
        
    def start_checking(self):
        """Thread-safe başlatma"""
        with self.lock:
            if not self.running:
                self.running = True
                Thread(target=self.check_accounts, daemon=True).start()
    
    def check_accounts(self):
        """Main checking logic"""
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        try:
            # Implementation here
            pass
        finally:
            self.stop_checking()
    
    def stop_checking(self):
        """Stop checking"""
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def clear_logs(self):
        """Clear log messages"""
        self.results.configure(state="normal")
        self.results.delete(1.0, "end")
        self.results.configure(state="disabled")
        
    def save_results(self):
        """Save only valid results to file"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                              filetypes=[("Text files", "*.txt")])
        if filename:
            all_text = self.results.get(1.0, "end")
            valid_accounts = [line for line in all_text.split('\n') 
                            if "Geçerli" in line or "VALID" in line]
            with open(filename, "w", encoding="utf-8") as f:
                f.write('\n'.join(valid_accounts))

if __name__ == "__main__":
    app = MinnoşCheckerFinal()
    app.mainloop()
