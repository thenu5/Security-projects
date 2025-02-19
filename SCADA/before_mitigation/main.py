import tkinter as tk
from tkinter import font

# Initial system values (to be overwritten by the attack)
ph_level = 7.0  # Normal pH level
water_level = 50  # Normal water level
valve_status = "Closed"
pump_status = "Off"

# Create the main Tkinter window
root = tk.Tk()
root.title("CPS - Water System Control")

# Set the window size and background color
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

# Function to read the system status from the file
def read_status_from_file():
    global ph_level, water_level, valve_status, pump_status
    try:
        with open('status.txt', 'r') as file:
            lines = file.readlines()
            ph_level = float(lines[0].strip())
            water_level = float(lines[1].strip())
            valve_status = lines[2].strip()
            pump_status = lines[3].strip()
    except Exception as e:
        print(f"Error reading status file: {e}")

# Function to update the displayed system status
def update_system_status():
    read_status_from_file()  # Read the updated values from the file

    # Update the GUI labels with the latest data
    ph_label.config(text=f"Current pH Level: {ph_level}")
    water_level_label.config(text=f"Current Water Level: {water_level}%")
    valve_label.config(text=f"Valve Status: {valve_status}")
    pump_label.config(text=f"Pump Status: {pump_status}")

    # Continuously update the status (every 1 second)
    root.after(1000, update_system_status)

# Function to initialize status.txt with default values if it doesn't exist
def initialize_status_file():
    try:
        with open('status.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) < 4:  # Check if there are less than 4 lines in the file
                raise ValueError("File contents are incomplete.")
    except (FileNotFoundError, ValueError):
        # If the file is not found or incomplete, write the default values
        with open('status.txt', 'w') as file:
            file.write(f"{ph_level}\n")
            file.write(f"{water_level}\n")
            file.write(f"{valve_status}\n")
            file.write(f"{pump_status}\n")

# Initialize the status file (if necessary)
initialize_status_file()

# Start the status update
update_system_status()

# Run the Tkinter main loop
root.mainloop()
