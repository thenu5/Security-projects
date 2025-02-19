import time
import threading
import random
import tkinter as tk
import sys
import os
import ctypes
import socket
from datetime import datetime
from collections import defaultdict

# Global variables for rate limiting
request_tracker = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})
MAX_REQUESTS = 100
TIME_FRAME = 60  # 60 seconds

# Authentication credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # SHA256 hash of "password"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Unable to determine IP"

def log_auth_failure(username, ip_address):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('auth_failures.log', 'a') as log_file:
        log_file.write(f"{timestamp} - Authentication failed for user: {username} from IP: {ip_address}\n")

def attempt_authentication():
    print("Authentication required to access the system.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    ip_address = get_local_ip()
    
    with open('auth_attempt.txt', 'w') as file:
        file.write(f"{username}\n{password}\n{ip_address}\n")
    
    print("Authenticating...")
    time.sleep(2)  # Wait for main.py to process the authentication
    
    try:
        with open('auth_result.txt', 'r') as file:
            auth_result = file.read().strip()
        
        if auth_result == "SUCCESS":
            print(f"Authentication successful from IP: {ip_address}. Starting DOS attack...")
            return True
        else:
            print(f"Authentication failed from IP: {ip_address}. Access denied.")
            log_auth_failure(username, ip_address)
            return False
    except FileNotFoundError:
        print(f"Authentication process failed from IP: {ip_address}.")
        log_auth_failure(username, ip_address)
        return False

def is_rate_limited(ip_address):
    current_time = time.time()
    if current_time - request_tracker[ip_address]['last_reset'] > TIME_FRAME:
        request_tracker[ip_address] = {'count': 0, 'last_reset': current_time}
    
    request_tracker[ip_address]['count'] += 1
    
    if request_tracker[ip_address]['count'] > MAX_REQUESTS:
        print(f"Rate limit exceeded for IP: {ip_address}")
        return True
    return False

# Function to simulate an attack by updating values in status.txt
def update_status():
    ip_address = get_local_ip()
    try:
        # Infinite loop to continuously update the values (Denial of Service simulation)
        while True:
            if is_rate_limited(ip_address):
                print("Attack paused due to rate limiting.")
                time.sleep(5)  # Wait for 5 seconds before retrying
                continue

            # Simulate attack: Randomly change pH level and water level
            ph_level = random.uniform(3.0, 14.0)  # Simulate pH level between 3.0 and 14.0
            water_level = random.uniform(0.0, 100.0)  # Simulate water level between 0.0 and 100.0
            valve_status = random.choice(['open', 'closed'])
            pump_status = random.choice(['on', 'off'])

            # Update the status.txt file
            with open('status.txt', 'r+') as file:
                lines = file.readlines()

                # Ensure that the file has at least 4 lines (for each value)
                if len(lines) < 4:
                    raise ValueError("The status file is not in the expected format.")

                # Read and convert the first two lines as floats (ensure no integer conversion happens)
                try:
                    current_ph_level = float(lines[0].strip())  # Convert to float
                    current_water_level = float(lines[1].strip())  # Convert to float
                except ValueError:
                    print("Error reading status file. Ensure the pH level and water level are valid floats.")
                    sys.exit(1)

                # Update lines with new values, ensuring ph_level and water_level are floats
                lines[0] = f"{ph_level:.2f}\n"  # Ensure 2 decimal places for ph_level
                lines[1] = f"{water_level:.2f}\n"  # Ensure 2 decimal places for water_level
                lines[2] = f"{valve_status}\n"
                lines[3] = f"{pump_status}\n"

                # Go back to the beginning of the file to overwrite it with updated data
                file.seek(0)
                file.writelines(lines)
                file.truncate()  # Ensure no extra data is left in the file

            print(f"Attack executed from IP {ip_address}: pH={ph_level:.2f}, Water={water_level:.2f}%, Valve={valve_status}, Pump={pump_status}")
            time.sleep(0.1)  # Update every 0.1 seconds to simulate continuous attack

    except Exception as e:
        print(f"Error updating status file: {e}")
        sys.exit(1)

# Function to terminate the Tkinter window (simulating the DoS attack closing the window)
def close_window():
    root.quit()  # This will close the Tkinter window running 'main.py'

# Set up the Tkinter window for DoS attack (simulated attack)
def create_attack_window():
    global root
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window initially

    # Run the update_status in a separate thread
    threading.Thread(target=update_status, daemon=True).start()

    # Simulate the closing of the window by forcing it after a short time (e.g., 3 seconds)
    time.sleep(3)  # Wait for 3 seconds to simulate the DoS attack
    close_window()

# Start the DoS attack (start the Tkinter window and attack thread)
if __name__ == "__main__":
    if attempt_authentication():
        print("Starting DoS attack simulation...")

        # Start the attack by opening the Tkinter window (invisible) and starting the update loop
        create_attack_window()

        # Allow the DoS attack to run for a while before forcibly closing the GUI window
        print("Simulating continuous pH and water level changes...")

        # Prevent the main program from exiting immediately
        root.mainloop()

        print("DoS attack complete.")
    else:
        print("Access denied due to authentication failure.")