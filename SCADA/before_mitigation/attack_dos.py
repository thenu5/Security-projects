import time
import threading
import random
import tkinter as tk
import sys
import os
import ctypes

# Function to simulate an attack by updating values in status.txt
def update_status():
    try:
        # Infinite loop to continuously update the values (Denial of Service simulation)
        while True:
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
    print("Starting DoS attack simulation...")

    # Start the attack by opening the Tkinter window (invisible) and starting the update loop
    create_attack_window()

    # Allow the DoS attack to run for a while before forcibly closing the GUI window
    print("Simulating continuous pH and water level changes...")

    # Prevent the main program from exiting immediately
    root.mainloop()

    print("DoS attack complete.")
