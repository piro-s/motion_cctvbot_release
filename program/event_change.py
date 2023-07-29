import json
import sys
from variables import *


image_filename = sys.argv[1]

log_print("+Start - New motion image and event.")

try:
    log_print("Trying to open a file: '" + event_filename + "'.")
    with open(event_filename, 'r') as file:
        new_event = json.load(file)
except FileNotFoundError:
    log_print("#Error - Missing event file: '" + event_filename + "', check step 7 in readme.")
except Exception as exc:
    log_print("#Error - Something wrong with event file: \n" + str(exc) + "\nCheck step 7 in readme.")

new_event['event'] = 'True' # New event has appeared
new_event['file'] = image_filename # Captured image
try:
    log_print("Trying to open a file: '" + event_filename + "'.")
    with open(event_filename, 'w') as file:
        json.dump(new_event, file)
except FileNotFoundError:
    log_print("#Error - Missing event file: '" + event_filename + "', check step 7 in readme.")
except Exception as exc:
    log_print("#Error - Something wrong with event file: \n" + str(exc) + "\nCheck step 7 in readme.")

log_print("-Stop - New motion image and event.")