#! cisco_versions.py

##################################################
## Fetches Curent Running Version on Cisco Network
## Devices.
##################################################
## Author: Fizgriz(Jefffrey Meigs)
## Version: 1.0.0
## Maintainer: Fizgriz(Jeffrey Meigs)
##################################################

# Built-in/Generic Imports
import time
import sys
import socket
import argparse # Accept runtime switches

# Libs
import paramiko # SSH
from paramiko.ssh_exception import (BadHostKeyException,
    AuthenticationException,
    SSHException)
import getpass # Fetch secure password
import os.path # Local file paths
from dotenv import load_dotenv # Use .env Resource
# [Requries install 'pip install -U <package name']

# Load .env resource
load_dotenv()

# Declare and Set Variables
sys.tracebacklimit = 0 # Default Traceback to none.
ips = os.getenv("IP_LIST").split(',') # Grab and store IP's in list
save_path = os.getenv("SAVE_PATH") # Grab and store output file save path
file_name = os.getenv("FILE_NAME") # Grab and store output file name
complete_path = os.path.join(save_path, file_name+".txt") # Combine paths

# Initiate used objects
parser = argparse.ArgumentParser(description='enable flags at run time.')
parser.add_argument('--debug', action='store_true',
                    help='print traceback on crashes')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Check for --debug flag and debug setting
if(parser.parse_args().debug) or (os.getenv('DEBUG')=='1'):
    sys.tracebacklimit = 1000         #default it back to normal, debug is set
    print("!-----------------DEBUG MODE----------------!")

# Display Script purpose.
print("""
      ##################################################
      ## Fetches Curent Running Version on Cisco Network
      ## Devices.
      ##################################################
      ## Author: Fizgriz(Jefffrey Meigs)
      ## Version: 1.0.0
      ## Maintainer: Fizgriz(Jeffrey Meigs)
      ##################################################
      """)
time.sleep(2)


def create_output():
    """Create or clear out output log file.

    Validates the save path and file name were declared.
    Attempts to create or clear the output file based on
    declared values. Lets the user know if successfull or
    an error occured.

    :return: None
    """
    if (save_path == '') or (file_name == ''):
        print("""save path or file name was not set before runtime.
              Please see README.""")
        quit()
    try:
        print("Creating output file if file does not exist.")
        file = open(complete_path, 'w')
        file.close()
        print("Created " + complete_path + "\n")
    except Exception as e:
        print("""Error creating Log file. You may not have proper local file
              permissions in directory specified.""")
        quit()
    return

def write_to_output (data):
    """Write data to output log file.

    Opens output log file declared earlier and inserts
    data given into file. Closes the file.

    :param data: Data to be appended to the output log.

    :return: None
    """
    file = open(complete_path, 'a')
    file.write(data)
    file.close()
    return

# Main run

create_output()

if ips == []:
    print('IP list was not populated. Please see TODO')
    quit()

try:
    print("Cisco Admin Credentials are required.")
    username = input("Username: ")
    password = getpass.getpass()
    print("------------------------------------------------")
except Exception as e:
    print("Failed to get credentials. Closing script.")
    quit()

for ip in ips:
    try:
        try:
            ssh.connect(ip, username=username, password=password,
                        look_for_keys=False, allow_agent=False)
            print("\nSSH connection established to " + ip)
            print("Performing Version Check for results...")
            stdin, stdout, stderr = ssh.exec_command("show version")
            time.sleep(4)
            stdout = stdout.readlines()
            for line in stdout:
                if 'Cisco IOS Software' in line:
                    output = line
                    break
            write_to_output(ip + ": " + ''.join(output))
            print(ip + " Version appended to file.")
        finally:
            ssh.close()
            print("Session Closed with: " + ip)
            print("------------------------------------------------")
    except (BadHostKeyException, AuthenticationException,
        SSHException, socket.error) as e:
            """Something went wrong during the ssh connection.
            Close the current SSH connection just to be safe.
            Send Error to user.
            """
            ssh.close()
            print("""
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                An Error occured. closing Connection.
                Exception Thrown.
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """)
            print(e)

print("""
    ##################################################
    SCRIPT COMPLETE. PLEASE SEE VERSIONS IN
    """ + complete_path + """ File.
    ##################################################
""")
