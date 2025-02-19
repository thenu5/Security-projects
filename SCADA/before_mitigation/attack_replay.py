import random
import time

# Simulate a more complex relay attack
def relay_attack():
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

            time.sleep(3)  # Attack continues every 3 seconds
    except KeyboardInterrupt:
        print("Attack stopped.")

# Run the relay attack
if __name__ == "__main__":
    relay_attack()
