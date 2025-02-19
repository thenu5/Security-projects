import random
import time
from datetime import datetime
import socket

def get_local_ip():
    try:
        # This creates a UDP socket (doesn't actually connect)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connecting to a Google DNS server
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
            print(f"Authentication successful from IP: {ip_address}. Starting relay attack...")
            return True
        else:
            print(f"Authentication failed from IP: {ip_address}. Access denied.")
            log_auth_failure(username, ip_address)
            return False
    except FileNotFoundError:
        print(f"Authentication process failed from IP: {ip_address}.")
        log_auth_failure(username, ip_address)
        return False

# Simulate a more complex relay attack
def relay_attack():
    ip_address = get_local_ip()
    try:
        while True:
            with open('status.txt', 'r') as file:
                lines = file.readlines()

            # Randomly change pH level within a range
            ph_level = random.uniform(3.0, 7.5)  # Random pH level between 3.0 and 7.5
            lines[0] = f"{ph_level}\n"

            # Randomly change water level within a range
            water_level = random.randint(10, 100)  # Random water level between 10% and 100%
            lines[1] = f"{water_level}\n"

            # Randomly change valve status between "Open" and "Closed"
            valve_status = random.choice(["Open", "Closed"])
            lines[2] = f"{valve_status}\n"

            # Randomly change pump status between "On" and "Off"
            pump_status = random.choice(["On", "Off"])
            lines[3] = f"{pump_status}\n"

            # Write the manipulated values back to the file
            with open('status.txt', 'w') as file:
                file.writelines(lines)

            print(f"Attack executed from IP {ip_address}: pH={ph_level:.2f}, Water={water_level}%, Valve={valve_status}, Pump={pump_status}")
            time.sleep(3)  # Attack continues every 3 seconds
    except KeyboardInterrupt:
        print(f"Attack stopped from IP: {ip_address}")

# Run the relay attack with authentication
if __name__ == "__main__":
    if attempt_authentication():
        relay_attack()
    else:
        print("Access denied due to authentication failure.")