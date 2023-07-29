import datetime
import json


# global variables
motion_folder = '/home/_user_/motion/'
capture_folder = '/home/_user_/motion/capture/'
camera_localip = 'http://192.168.1.IP:WebControlPort/00000/' # Local IP + webcontrol port, 00000 - id all cameras
token_filename = motion_folder + 'telegram_token'
credential_filename = motion_folder + 'credential'
users_filename = motion_folder + 'users.json'
event_filename = motion_folder + 'event.json'

log = 'True' # For log output if needed
infinity = 'True' # To run a bot in a recursive loop
master_id = 0 # ID for chat master
page = 1 # Page for list images
buttons_list = [] # For list of all images


def log_print(text): # Log function
    if log == 'True':
        print("--- " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Print current time
        print(text) # Print log message


# Token
try:
    log_print("Trying to open a file: '" + token_filename + "'.")
    with open(token_filename, 'r', encoding='utf-8') as file:
        telegram_token = file.read()
    log_print("File: '" + token_filename + "' opened successfully.")
except FileNotFoundError:
    log_print("#Error - Missing token file: '" + token_filename + "', check step 11 in readme.")
    log_print("Close script.")
    quit()
except Exception as exc:
    log_print("#Error - Something wrong with token file: \n" + str(exc) + "\nCheck step 11 in readme.")
    log_print("Close script.")
    quit()


# JSON users data
try:
    log_print("Trying to open a file: '" + users_filename + "'.")
    with open(users_filename, 'r', encoding='utf-8') as file:
        users = json.load(file)
        master_id = list(users.keys())
        master_id = master_id[0]
    log_print("File: '" + users_filename + "' opened successfully.")
except FileNotFoundError:
    log_print("#Error - Missing json file: '" + users_filename + "', check step 7 in readme.")
    log_print("Close script.")
    quit()
except Exception as exc:
    log_print("#Error - Something wrong with json file: \n" + str(exc) + "\nCheck step 7 in readme.")
    log_print("Close script.")
    quit()


# Password
try:
    log_print("Trying to open a file: '" + credential_filename + "'.")
    with open(credential_filename, 'r') as file:
        password_master = file.read()
    log_print("File: '" + credential_filename + "' opened successfully.")
except FileNotFoundError:
    log_print("#Error - Missing password file: '" + credential_filename + "', check step 7 and 8 in readme.")
    log_print("Close script.")
    quit()
except Exception as exc:
    log_print("#Error - Something wrong with password file: \n" + str(exc) + "\nCheck step 7 and 8 in readme.")
    log_print("Close script.")
    quit()