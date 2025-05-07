import websocket
import json
import time
import uuid
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ITSMESATYAVIR 
def logo():
    print(f"{Fore.GREEN}{Style.BRIGHT}[FORESTARMY]{Style.RESET_ALL} WebSocket Client Initialized\n")

# File paths
user_file = "user.txt"
device_file = "device.txt"

# Get or prompt for user_id
def get_user_id():
    if not os.path.exists(user_file) or os.path.getsize(user_file) == 0:
        user_id = input(f"{Fore.CYAN}[FORESTARMY] Enter your User ID: ").strip()
        with open(user_file, "w") as f:
            f.write(user_id)
        print(f"{Fore.YELLOW}[FORESTARMY] User ID saved to {user_file}")
    else:
        with open(user_file, "r") as f:
            user_id = f.read().strip()
    return user_id

# Get or generate device_id for the user
def get_device_id(user_id):
    if os.path.exists(device_file):
        with open(device_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(f"{user_id}:"):
                    return line.strip().split(":")[1]

    # If not found, generate new device_id
    device_id = str(uuid.uuid4())
    with open(device_file, "a") as f:
        f.write(f"{user_id}:{device_id}\n")
    print(f"{Fore.YELLOW}[FORESTARMY] Device ID generated and saved for user {user_id}")
    return device_id

# WebSocket event handlers
def on_open(ws):
    print(f"{Fore.GREEN}{Style.BRIGHT}[FORESTARMY] Connection Opened")
    payload = {
        "device_id": device_id,
        "user_id": user_id
    }
    ws.send(json.dumps(payload))
    print(f"{Fore.YELLOW}[FORESTARMY] Payload sent to server")

def on_message(ws, message):
    print(f"{Fore.CYAN}{Style.BRIGHT}[FORESTARMY] Message Received: {Style.RESET_ALL}{message}")

def on_error(ws, error):
    print(f"{Fore.RED}{Style.BRIGHT}[FORESTARMY] Error: {Style.RESET_ALL}{error}")

def on_close(ws, close_status_code, close_msg):
    print(f"{Fore.MAGENTA}{Style.BRIGHT}[FORESTARMY] Connection Closed | Code: {close_status_code} | Reason: {close_msg}")

# Auto reconnect loop
def connect_ws():
    logo()
    while True:
        try:
            ws = websocket.WebSocketApp(ws_url,
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.run_forever()
        except Exception as e:
            print(f"{Fore.RED}[FORESTARMY] Exception: {e}")
        print(f"{Fore.BLUE}[FORESTARMY] Reconnecting in 5 seconds...\n")
        time.sleep(5)

# Main Execution
user_id = get_user_id()
device_id = get_device_id(user_id)
ws_url = f"wss://ws.pingvpn.xyz/pingvpn/v1/clients/{user_id}/events"

connect_ws()
