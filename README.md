# Remote Access Trojan (RAT)

## Overview
This RAT program is designed for educational and research purposes only. It demonstrates how a Remote Access Trojan can be structured, using Python scripts to simulate both the attacker and the victim. **Do not use this code for any malicious or illegal activities.**

The program consists of two main components:
1. **Victim Script**: `WindowsSecurity.py`
2. **Attacker Software**: `office365.py`

### Components

#### 1. `WindowsSecurity.py` - Victim Script
- **Purpose**: This script is designed to run on the victim's machine, disguising itself as a legitimate security process.
- **Functionality**: 
  - Operates as a server, waiting for commands from the attacker's client software.
  - Prevents security software from identifying it as a threat by mimicking Windows security processes.

#### 2. `office365.py` - Attacker Software
- **Purpose**: This script functions as the attacker’s client, controlling the victim’s machine through the `WindowsSecurity.py` script.
- **Functionality**:
  - Acts as a client that sends commands to the `WindowsSecurity.py` script.
  - Mimics legitimate Office 365 processes to avoid detection.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ph453-z3r0/RAT.git
    cd RAT
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configuration**:
   - No need to modify the IP address and port settings in both `WindowsSecurity.py` and `office365.py` to ensure proper communication between the client and server.
   - It uses the local ip to host (WORKS ONLY ON LAN)
  
## Usage

### Running the Victim Script
1. Deploy the `WindowsSecurity.py` script on the target machine.
2. Execute the script:
    ```bash
    python WindowsSecurity.py
    ```
3. The script will run in the background, awaiting commands from the attacker's client.
   The Scripts needs to be converted to exe for effective usage

### Running the Attacker Software
1. On the attacker's machine, execute the `office365.py` script:
    ```bash
    python office365.py
    ```
2. Use the client to send commands to the victim’s machine through the `WindowsSecurity.py` server.

## Disclaimer
This program is intended solely for educational purposes. The author is not responsible for any misuse of the code. Ensure that you have permission from the system owner before deploying or testing this software.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Releases
Releases will be uploaded soon ! [This is a PROTOTYPE]
