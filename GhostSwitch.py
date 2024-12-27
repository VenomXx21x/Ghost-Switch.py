import time
import requests
from stem import Signal
from stem.control import Controller
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

def banner():
    print(Fore.YELLOW + """
      █████╗  ██████╗ ███╗   ██╗██╗  ██╗ ██████╗ ███╗   ███╗ ██████╗ ███████╗
     ██╔══██╗██╔════╝ ████╗  ██║██║  ██║██╔═══██╗████╗ ████║██╔═══██╗██╔════╝
     ███████║██║  ███╗██╔██╗ ██║███████║██║   ██║██╔████╔██║██║   ██║█████╗  
     ██╔══██║██║   ██║██║╚██╗██║██╔══██║██║   ██║██║╚██╔╝██║██║   ██║██╔══╝  
     ██║  ██║╚██████╔╝██║ ╚████║██║  ██║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████╗
     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "            Coded by HacktifyDiaries | Stay Anonymous")
    print(Fore.YELLOW + "-----------------------------------------------------\n")

def get_current_ip():
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get("http://checkip.amazonaws.com/", proxies=proxies, timeout=10)
        return response.text.strip()
    except requests.RequestException as e:
        return f"{Fore.RED}[ERROR] Error fetching IP: {e}"

def change_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='blu3@##@Top=1234')  # Replace with your Tor password
            controller.signal(Signal.NEWNYM)
            print(Fore.GREEN + "[SUCCESS] IP address changed successfully!")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Unable to change IP: {e}")

def main(interval):
    banner()
    print(Fore.GREEN + "[INFO] Starting automatic IP changer...\n")
    last_ip = None

    while True:
        print(Fore.CYAN + "[INFO] Requesting new identity...")
        change_ip()

        for _ in range(10):  # Retry up to 10 times to get a new IP
            new_ip = get_current_ip()
            if new_ip != last_ip and "ERROR" not in new_ip:
                last_ip = new_ip
                print(Fore.GREEN + f"[INFO] New IP: {new_ip}\n")
                break
            else:
                print(Fore.YELLOW + "[WARNING] IP did not change. Retrying...")
                time.sleep(3)
        else:
            print(Fore.RED + "[ERROR] Failed to obtain a new IP after multiple attempts.")

        print(Fore.YELLOW + f"[WAITING] Waiting {interval} seconds before the next change...\n")
        time.sleep(interval)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="HacktifyDiaries: Powerful Tor-based IP changer.")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Interval (seconds) between IP changes")
    args = parser.parse_args()

    try:
        main(args.interval)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[INFO] Exiting...")
    except Exception as e:
        print(Fore.RED + f"[ERROR] An unexpected error occurred: {e}")
