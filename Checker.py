import ctypes
import requests
import json
import time
import sys
import random
import subprocess
from colorama import init, Fore, Style

init()  # Initialize colorama

# Function to set the transparency of the terminal background
def set_terminal_transparency(transparency):
    try:
        # Using the Windows API to get the terminal window
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()

        # Setting the transparency using the Windows API
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, int(transparency * 255), 2)
    except Exception as e:
        print(f"Error setting transparency: {e}")

def animate_cover():
    sys.stdout.write("""
████████╗███████╗███╗   ███╗██████╗ ███████╗██╗   ██╗
╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██╔════╝╚██╗ ██╔╝
   ██║   █████╗  ██╔████╔██║██████╔╝█████╗   ╚████╔╝
   ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██╔══╝    ╚██╔╝
   ██║   ███████╗██║ ╚═╝ ██║██║     ██║        ██║
   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝        ╚═╝
    """)
    sys.stdout.write("\n")
    sys.stdout.write("Loading")
    start_time = time.time()
    stop_time = start_time + random.uniform(5, 10)

    while time.time() < stop_time:
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\b \b" * 3)
        sys.stdout.flush()
        time.sleep(0.5)

    sys.stdout.write("\r")
    sys.stdout.write(" " * 13)
    sys.stdout.write("\r")
    sys.stdout.flush()
    time.sleep(3)  # 3 seconds pause

# Desired transparency value (between 0 and 1, 0 = fully transparent, 1 = opaque)
transparency = 0.8

# Set terminal transparency
set_terminal_transparency(transparency)

def send_webhook(url, content):
    data = {
        "content": content
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

def check_nitro_code(code, webhook_url, valid_file, invalid_file):
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"

    response = requests.get(url)

    if response.status_code == 200:
        result = f"{Fore.GREEN}[VALID]{Style.RESET_ALL} {code}"
        send_webhook(webhook_url, result)
        valid_file.write(f"{code}\n")
    else:
        result = f"{Fore.RED}[INVALID]{Style.RESET_ALL} {code}"
        send_webhook(webhook_url, result)
        invalid_file.write(f"{code}\n")
        print(result)

def check_nitro_codes_from_file(file_path):
    with open(file_path, "r") as file:
        nitro_codes = file.read().splitlines()

    num_codes = len(nitro_codes)

    valid_count = 0
    invalid_count = 0

    webhook_url = input("Enter the Discord webhook URL: ")

    add_codes_input = input("Have you added your codes to the 'Nitro Codes.txt' file? (y/n): ")

    if add_codes_input.lower() == "y":
        print("Press Enter to perform the check...")
        input()
    elif add_codes_input.lower() == "n":
        print("Please add your codes to the 'Nitro Codes.txt' file and restart the program.")
        return
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return

    with open("Valid_Codes.txt", "w") as valid_file, \
            open("Invalid_Codes.txt", "w") as invalid_file:

        for code in nitro_codes:
            check_nitro_code(code, webhook_url, valid_file, invalid_file)

            if "VALID" in code:
                valid_count += 1
            else:
                invalid_count += 1

    print(f"Valid Codes: {valid_count}")
    print(f"Invalid Codes: {invalid_count}")

# Show cover
animate_cover()

# Example call
file_path = "Nitro Codes.txt"
check_nitro_codes_from_file(file_path)

# End the program when Enter is pressed
input("Press Enter to exit the program...")
subprocess.call("taskkill /F /PID %s" % subprocess.getpid(), shell=True)
