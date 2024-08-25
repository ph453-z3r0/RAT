import socket
import threading
from termcolor import colored

def is_server_running(ip, port=26050):
    try:
        with socket.create_connection((ip, port), timeout=1) as sock:
            return True
    except (ConnectionRefusedError, OSError):
        return False

def scan_ip_range(start_ip, end_ip, results):
    current_ip = start_ip
    while current_ip <= end_ip:
        ip_str = socket.inet_ntoa(current_ip.to_bytes(4, 'big'))
        if is_server_running(ip_str):
            try:
                hostname = socket.gethostbyaddr(ip_str)[0]
            except socket.herror:
                hostname = "Unknown"
            results[ip_str] = hostname
        current_ip += 1

def generate_ip_range(start_ip, end_ip):
    start_ip_int = int.from_bytes(socket.inet_aton(start_ip), 'big')
    end_ip_int = int.from_bytes(socket.inet_aton(end_ip), 'big')
    return start_ip_int, end_ip_int

def scan_lan(start_ip, end_ip):
    start_ip_int, end_ip_int = generate_ip_range(start_ip, end_ip)
    num_threads = 50
    ip_range = (end_ip_int - start_ip_int) // num_threads
    results = {}
    threads = []

    for i in range(num_threads):
        thread_start_ip = start_ip_int + i * ip_range
        thread_end_ip = start_ip_int + (i + 1) * ip_range - 1 if i < num_threads - 1 else end_ip_int
        thread = threading.Thread(target=scan_ip_range, args=(thread_start_ip, thread_end_ip, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

def broadcast_message(results, message):
    for ip in results:
        send_message(ip, message)

def receive_full_message(sock):
    buffer_size = 1024
    data = b""
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data.decode()

def send_message(ip, message, port=26050):
    try:
        with socket.create_connection((ip, port), timeout=1) as sock:
            sock.sendall(message.encode())
            if message.startswith("get: "):
                file_name = message.split("get: ")[1]
                with open(file_name, 'wb') as f:
                    while True:
                        data = sock.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(colored(f"File '{file_name}' received successfully", 'green'))
                return f"File '{file_name}' received successfully"
            else:
                response = receive_full_message(sock)
                return response
    except (ConnectionRefusedError, OSError) as e:
        return f"Failed to connect to {ip}: {str(e)}"

def send_file(ip, file_name, port=26050):
    try:
        with socket.create_connection((ip, port), timeout=1) as sock:
            sock.sendall(f"send: {file_name}".encode())
            with open(file_name, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    sock.sendall(data)
            sock.sendall(b"")
            response = receive_full_message(sock)
            print(colored(f"Response from {ip}: {response}", 'green'))
    except (ConnectionRefusedError, OSError):
        print(colored(f"Failed to connect to {ip}", 'red'))

def display_results(results):
    for idx, (ip, hostname) in enumerate(results.items()):
        print(colored(f"{idx}. IP: {ip}, Hostname: {hostname}", 'yellow'))

def print_ascii_art():
    print(colored("""
██╗      █████╗ ███╗   ██╗ ██████╗ ███████╗███████╗██╗
██║     ██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔════╝██║
██║     ███████║██╔██╗ ██║██║  ███╗█████╗  ███████╗██║
██║     ██╔══██║██║╚██╗██║██║   ██║██╔══╝  ╚════██║██║
███████╗██║  ██║██║ ╚████║╚██████╔╝███████╗███████║███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
""", 'green', attrs=['bold']))

if __name__ == "__main__":
    results = {}
    print_ascii_art()
    while True:
        print(colored("\n[+] Options:", 'magenta', attrs=['bold']))
        print(colored("[1] Scan the LAN", 'green'))
        print(colored("[2] Broadcast a message to all found IPs", 'green'))
        print(colored("[3] Send a message to a specific IP by index", 'green'))
        print(colored("[4] Send a file to a specific IP (OPTIONAL)", 'green'))
        print(colored("[5] File Transfer", 'green'))
        print(colored("[6] Exit", 'green'))
        print()
        choice = input(colored("[?] Enter your choice: ", 'cyan'))
        print()

        if choice == "1":
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip_parts = local_ip.split('.')
            start_ip = '.'.join(ip_parts[:-1] + ['1'])
            end_ip = '.'.join(ip_parts[:-1] + ['255'])
            print(colored(f"[*] Scanning LAN for servers running [{start_ip} - {end_ip}] on port 26050...", 'blue'))
            results = scan_lan(start_ip, end_ip)
            if results:
                print()
                print(colored("[+] :::Found servers:::", 'green', attrs=['bold']))
                display_results(results)
            else:
                print()
                print(colored("[-] No servers found.", 'red', attrs=['bold']))
                print()
        
        elif choice == "2":
            if not results:
                print()
                print(colored("[-] No servers to broadcast to. Please scan the LAN first.", 'red'))
                print()
            else:
                print()
                message = input(colored("[?] Enter the message to broadcast: ", 'cyan'))
                broadcast_message(results, message)
                print()
        
        elif choice == "3":
            if not results:
                print()
                print(colored("[-] No servers to send a message to. Please scan the LAN first.", 'red'))
                print()
            else:
                print()
                display_results(results)
                print()
                try:
                    index = int(input(colored("[?] Enter the index of the IP to send a message to: ", 'cyan')))
                    print()
                    ip = list(results.keys())[index]
                    while True:
                        message = input(colored("[?] Enter the message to send: ", 'cyan'))
                        print()
                        response = send_message(ip, message)
                        print(colored(f"[*] Response from {ip}: {response}", 'green'))
                        if message == 'quit':
                            break   
                except IndexError:
                    print(colored("[-] Invalid index.", 'red'))
        
        elif choice == "4":
            if not results:
                print()
                print(colored("[-] No servers to send a message to. Please scan the LAN first.", 'red'))
                print()
            else:
                try:
                    ipad = input("[?] Enter the IP of the system : ", 'cyan')
                    while True:
                        message = input(colored("[?] Enter the message to send: ", 'cyan'))
                        print()
                        response = send_message(ipad, message)
                        print(colored(f"[*] Response from {ipad}: {response}", 'green'))
                        if message == 'quit':
                            break
                except IndexError:
                    print(colored("[-] Invalid index.", 'red'))

        elif choice == "5":
            if not results:
                print()
                print(colored("[-] No servers to send a message to. Please scan the LAN first.", 'red'))
                print()
            else:
                print()
                display_results(results)
                print()
                try:
                    print()
                    index = int(input(colored("[?] Enter the index of the IP to transfer files to: ", 'cyan')))
                    print()
                    ip = list(results.keys())[index]
                    while True:
                        print()
                        message = input(colored("[?] Enter the command to send: ", 'cyan'))
                        if message.startswith("get: "):
                            response = send_message(ip, message)
                            print(colored(f"[*] Response from {ip}: {response}", 'green'))
                        elif message == "ls":
                            response = send_message(ip, message="ls")
                            print(colored(f"[*] Response from {ip}: {response}", 'green'))
                        elif message.startswith("cd"):
                            response = send_message(ip, message)
                            print(colored(f"[*] Response from {ip}: {response}", 'green'))
                        else:
                            print()
                            print(colored('''[!] You can only use: 
                                
                                send: filename - to upload a file
                                get: filename - to download a file
                                ls - show the files in the current directory
                                cd - change directory''', 'yellow'))
                            print()
                        if message == "quit":
                            break    
                except IndexError:
                    print(colored("[-] Invalid index.", 'red'))

        elif choice == "6":
            print()
            print(colored("[*] Exiting...", 'red'))
            print()
            break
        else:
            print()
            print(colored("[!] Invalid choice. Please enter a valid option (1-5).", 'red'))
            print()
