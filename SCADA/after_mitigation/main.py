import tkinter as tk
from tkinter import font
import time
from datetime import datetime
import hashlib
import os

# Initial system values
ph_level = 7.0
water_level = 50
valve_status = "Closed"
pump_status = "Off"
last_update_time = None

# Authentication credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # SHA256 hash of "password"

# Create the main Tkinter window
root = tk.Tk()
root.title("CPS - Water System Control")
root.geometry("400x300")
root.configure(bg="#2e3d49")

# Define a custom font
custom_font = font.Font(family="Helvetica", size=12, weight="bold")

# Labels to display system status
status_label = tk.Label(root, text="System Status", font=font.Font(family="Helvetica", size=16, weight="bold"), bg="#2e3d49", fg="white")
status_label.grid(row=0, column=0, columnspan=2, pady=10)

ph_label = tk.Label(root, text=f"Current pH Level: {ph_level}", font=custom_font, bg="#2e3d49", fg="white")
ph_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)

water_level_label = tk.Label(root, text=f"Current Water Level: {water_level}%", font=custom_font, bg="#2e3d49", fg="white")
water_level_label.grid(row=2, column=0, sticky="w", padx=20, pady=5)

valve_label = tk.Label(root, text=f"Valve Status: {valve_status}", font=custom_font, bg="#2e3d49", fg="white")
valve_label.grid(row=3, column=0, sticky="w", padx=20, pady=5)

pump_label = tk.Label(root, text=f"Pump Status: {pump_status}", font=custom_font, bg="#2e3d49", fg="white")
pump_label.grid(row=4, column=0, sticky="w", padx=20, pady=5)

def authenticate(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return username == ADMIN_USERNAME and hashed_password == ADMIN_PASSWORD

def read_status_from_file():
    global ph_level, water_level, valve_status, pump_status, last_update_time
    try:
        with open('status.txt', 'r') as file:
            lines = file.readlines()
            ph_level = float(lines[0].strip())
            water_level = float(lines[1].strip())
            valve_status = lines[2].strip()
            pump_status = lines[3].strip()
            last_update_time = datetime.strptime(lines[4].strip(), "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error reading status file: {e}")

def update_system_status():
    read_status_from_file()
    ph_label.config(text=f"Current pH Level: {ph_level}")
    water_level_label.config(text=f"Current Water Level: {water_level}%")
    valve_label.config(text=f"Valve Status: {valve_status}")
    pump_label.config(text=f"Pump Status: {pump_status}")
    root.after(1000, update_system_status)

def initialize_status_file():
    with open('status.txt', 'w') as file:
        file.write(f"{ph_level}\n")
        file.write(f"{water_level}\n")
        file.write(f"{valve_status}\n")
        file.write(f"{pump_status}\n")
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def check_auth_attempts():
    try:
        with open('auth_attempt.txt', 'r') as file:
            username = file.readline().strip()
            password = file.readline().strip()
        
        auth_result = "FAIL"
        if authenticate(username, password):
            auth_result = "SUCCESS"
        
        with open('auth_result.txt', 'w') as file:
            file.write(auth_result)
        
        os.remove('auth_attempt.txt')
    except FileNotFoundError:
        pass
    
    root.after(500, check_auth_attempts)

# Initialize and start the GUI
initialize_status_file()
update_system_status()
check_auth_attempts()  # Start checking for authentication attempts
root.mainloop()