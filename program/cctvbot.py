"""
Script for processing captured images from motion and processing commands with
a bot.
Folder for other files associated with the script is written to a variable:
'motion_folder' (variables.py, line 5).
Folder for captured images from the camera is written to a variable:
'capture_folder' (variables.py, line 6).
Variable for camera web-control IP address: 'camera_localip' (variables.py, 
line 7).
If no log is needed, change the value of the variable 'log' (variables.py, 
line 14) from 'True' to 'False'.
Since the bot sometimes terminates its work (low Internet connection speed, or
some other incomprehensible reason), when the bot terminates (if an error
occurs and it closes), the script restarts it after 60 seconds. If this is not
required, then change the value of the 'infinty' (variables.py, line 15) 
variable from 'True' to 'False'.
"""

import glob
import requests
import time
import math
import telebot
from threading import Thread
from telebot import types # For types
from hashlib import sha256 # For password
from yolo_script import * # For image processing


###--------------------------------------------------------------------------###
# Prepare to start


from variables import * # Import all global variables and log functions

bot = telebot.TeleBot(telegram_token) # Create bot


###--------------------------------------------------------------------------###
# functions


def send_message(chat_id, message): # Send message with error log
    try:
        log_print("Attempt to send a message.")
        bot.send_message(chat_id, message)
        log_print("Message sended successfully.")
    except Exception as exc:
        time.sleep(15)
        log_print("#Error - Bot send message:\n")
        log_print(str(exc))


def send_document(chat_id, document, message): # Send document with error log
    try:
        log_print("Attempt to send a document.")
        bot.send_document(chat_id, document=document, caption=message, timeout=60)
        log_print("Document sended successfully.")
    except Exception as exc:
        time.sleep(15)
        log_print("#Error - Bot send document: \n")
        log_print(str(exc))


def save_users_json(): # Saving a registered user
    try:
        log_print("Trying to open a file: '" + users_filename + "'.")
        with open(users_filename, 'w') as file:
            json.dump(users, file)
        log_print("File: '" + users_filename + "' opened successfully.")
    except Exception as exc:
        log_print("#Error - Something wrong with users file: \n" + str(exc) + "\n")
        log_print("Close script.")
        quit()


def authorization(message): # Authorization in bot
    chat_id = str(message.chat.id)

    if chat_id not in users.keys():
        try:
            log_print("Attempt to send a message.")
            password = bot.send_message(chat_id, "Введите пароль:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(password, processPassword)
            log_print("Message sended successfully.")
        except Exception as exc:
            time.sleep(15)
            log_print("#Error - Bot authorization: \n")
            log_print(str(exc))
    else:
        send_message(chat_id, "Вы уже зарегистрированы. Если хотите перерегистрироваться отправьте: /reg")


def processPassword(message): # Bot password verification
    global master_id
    chat_id = str(message.chat.id)

    if password_master == sha256(message.text.encode()).hexdigest():
        users[chat_id] = {'name' : 'Мастер'}
        save_users_json()
        master_id = chat_id
        send_message(chat_id, "Добро пожаловать, Мастер!")
    else:
        send_message(chat_id, text="Неправильный пароль, повторите все снова.")
        log_print("#Error - Wrong password. ")


def build_list(buttons_list): # For list of all motion images
    log_print("+Start - Create menu for list motion images.")
    last_page = math.ceil(len(buttons_list) / 10)
    current_page = types.InlineKeyboardMarkup()
    current_page_list = buttons_list[10 * (page - 1):10 * (page - 1) + 10] # Page -1, because pages start with 1

    for item in current_page_list:
        current_page.add(item)

    if page == 1:
        first_button = types.InlineKeyboardButton(text='<' + str(page) + '>', callback_data='/first_page')
        next_button = types.InlineKeyboardButton(text=str(page + 1), callback_data='/next_page')
        dots_button = types.InlineKeyboardButton(text='...', callback_data='/next10_page')
        last_button = types.InlineKeyboardButton(text=str(last_page), callback_data='/last_page')
        current_page.row(first_button, next_button, dots_button, last_button)
    elif page == 2:
        first_button = types.InlineKeyboardButton(text=str(page - 1), callback_data='/first_page')
        current_button = types.InlineKeyboardButton(text='<' + str(page) + '>', callback_data='/current_page')
        next_button = types.InlineKeyboardButton(text=str(page + 1), callback_data='/next_page')
        dots_button = types.InlineKeyboardButton(text='...', callback_data='/next10_page')
        last_button = types.InlineKeyboardButton(text=str(last_page), callback_data='/last_page')
        current_page.row(first_button, current_button, next_button, dots_button, last_button)
    elif page == 3:
        first_button = types.InlineKeyboardButton(text=str(page - 2), callback_data='/first_page')
        prev_button = types.InlineKeyboardButton(text=str(page - 1), callback_data='/prev_page')
        current_button = types.InlineKeyboardButton(text='<' + str(page) + '>', callback_data='/current_page')
        next_button = types.InlineKeyboardButton(text=str(page + 1), callback_data='/next_page')
        dots_button = types.InlineKeyboardButton(text='...', callback_data='/next10_page')
        last_button = types.InlineKeyboardButton(text=str(last_page), callback_data='/last_page')
        current_page.row(first_button, prev_button, current_button, next_button, dots_button, last_button)
    elif page == last_page - 2:
        first_button = types.InlineKeyboardButton(text='1', callback_data='/first_page')
        dots_button = types.InlineKeyboardButton(text='...', callback_data='/prev10_page')
        prev_button = types.InlineKeyboardButton(text=str(last_page - 2), callback_data='/prev_page')
        current_button = types.InlineKeyboardButton(text='<' + str(last_page - 2) + '>', callback_data='/current_page')
        next_button = types.InlineKeyboardButton(text=str(last_page - 1), callback_data='/next_page')
        last_button = types.InlineKeyboardButton(text=str(last_page), callback_data='/last_page')
        current_page.row(first_button, dots_button, prev_button, current_button, next_button, last_button)
    elif page == last_page - 1:
        first_button = types.InlineKeyboardButton(text='1', callback_data='/first_page')
        dots_button = types.InlineKeyboardButton(text='...', callback_data='/prev10_page')
        prev_button = types.InlineKeyboardButton(text=str(last_page - 2), callback_data='/prev_page')
        current_button = types.InlineKeyboardButton(text='<' + str(last_page - 1) + '>', callback_data='/current_page')
        last_button = types.InlineKeyboardButton(text=str(last_page), callback_data='/last_page')
        current_page.row(first_button, dots_button, prev_button, current_button, last_button)
    elif page == last_page:
        first_button = types.InlineKeyboardButton(text='1', callback_data='/first_page')
        dots_button = types.InlineKeyboardButton(text='...', callback_data='/prev10_page')
        prev_button = types.InlineKeyboardButton(text=str(last_page - 1), callback_data='/prev_page')
        last_button = types.InlineKeyboardButton(text='<' + str(last_page) + '>', callback_data='/last_page')
        current_page.row(first_button, dots_button, prev_button, last_button)
    else:
        first_button = types.InlineKeyboardButton(text='1', callback_data='/first_page')
        dots_button1 = types.InlineKeyboardButton(text='...', callback_data='/prev10_page')
        prev_button = types.InlineKeyboardButton(text=str(page - 1), callback_data='/prev_page')
        current_button = types.InlineKeyboardButton(text='<' + str(page) + '>', callback_data='/current_page')
        next_button = types.InlineKeyboardButton(text=str(page + 1), callback_data='/next_page')
        dots_button2 = types.InlineKeyboardButton(text='...', callback_data='/next10_page')
        last_button = types.InlineKeyboardButton(text=str(last_page), callback_data='/last_page')
        current_page.row(first_button, dots_button1, prev_button, current_button, next_button, dots_button2, last_button)

    log_print("-Stop - Create menu for list motion images.")

    return current_page


###--------------------------------------------------------------------------###
# Bot handlers


@bot.message_handler(commands=['start'])
def start(message, res=False):
    authorization(message)


@bot.message_handler(commands=['id'])
def show_id(message, res=False):
    chat_id = str(message.chat.id)

    send_message(chat_id, "ID вашего чата: " + chat_id)
    send_message(chat_id, "Имя в чате: " + users[chat_id]['name'])


@bot.message_handler(commands=['reg'])
def reg(message, res=False):
    global master_id
    chat_id = str(message.chat.id)

    if chat_id in users.keys(): # Delete user if registered
        log_print("Remove user: " + chat_id) # Log
        send_message(chat_id, "Удаляю текущего пользователя...")
        users.pop(chat_id, 'None')
        save_users_json()
        if master_id == chat_id: # If user is master
            master_id = 0
        else:
            send_message(master_id, "Удаляю пользователя: " + chat_id) # Send message to master

    send_message(chat_id, "Начата процедура регистрации:")
    authorization(message)


@bot.message_handler(commands=['current_image'])
def current_image(message, res=False):
    event_start = camera_localip + 'action/eventstart' # Send command to motion to start event
    event_end = camera_localip + 'action/eventend' # Send command to motion to end event
    log_print("+Start - Send commands for start and end event.")

    try:
        log_print("Attempt to send requsets to motion.")
        r = requests.get(url = event_start) # Send start event
        time.sleep(3) # Wait few seconds
        r = requests.get(url = event_end) # Send end event
        log_print("Requests sended successfully.")
    except Exception as exc:
            log_print("#Error - Request to motion for start and end event: \n")
            log_print(str(exc))
    log_print("-Stop - Send commands for start and end event.")


@bot.message_handler(commands=['last_image'])
def last_image(message, res=False):
    log_print("+Start - Send commands for get last motion image.")

    try:
        log_print("Trying to open a file: '" + event_filename + "'.")
        with open(event_filename, 'r') as file:
            new_event = json.load(file)
        log_print("File: '" + event_filename + "' opened successfully.")
    except FileNotFoundError:
        log_print("#Error - Missing event file: '" + event_filename + "', check step 7 in readme.")
    except Exception as exc:
        log_print("#Error - Something wrong with event file: \n" + str(exc) + "\nCheck step 7 in readme.")

    new_event['event'] = 'True' # To start processing the last captured image
    try:
        log_print("Trying to open a file: '" + event_filename + "'.")
        with open(event_filename, 'w') as file:
            json.dump(new_event, file)
        log_print("File: '" + event_filename + "' opened successfully.")
    except Exception as exc:
        log_print("#Error - Save event json: ")
        log_print(str(exc))

    log_print("-Stop - Send commands for get last motion image.")


@bot.message_handler(commands=['list_images'])
def list_images(message, res=False):
    global buttons_list
    log_print("+Start - Send commands for get list all motion image.")
    chat_id = str(message.chat.id)
    motion_images = [image for image in glob(capture_folder + '*.jpg')] # Get all images from capture folder
    motion_images.sort() # Sort list
    buttons_list = [] # Clear current buttons list

    for image in motion_images:
        image = image.removeprefix(capture_folder)
        buttons_list.append(types.InlineKeyboardButton(text=image, callback_data='/image_' + image))

    buttons = build_list(buttons_list)

    try:
        log_print("Attempt to send a message with buttons.")
        message_text = "События, произошедшие за все время: \n"
        bot.send_message(chat_id, text=message_text, reply_markup=buttons)
        log_print("Message sended successfully.")
    except Exception as exc:
        time.sleep(15)
        log_print("#Error - Send list of all images: ")
        log_print(str(exc))

    log_print("-Stop - Send commands for get list all motion image.")


@bot.callback_query_handler(func=lambda calldata: True)
def check_callback_data(calldata): # Image list handler
    global page, buttons_list
    chat_id = calldata.message.chat.id
    message_id = calldata.message.message_id
    log_print("+Start - Callback handler for list images.")

    if calldata.data == '/first_page': # Change page for 1 and update list
        page = 1
        buttons = build_list(buttons_list)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=buttons)
    elif calldata.data == '/next_page': # Change page to next and update list
        page = page + 1
        buttons = build_list(buttons_list)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=buttons)
    elif calldata.data == '/next10_page': # Change page to next and update list
        page = page + 10
        buttons = build_list(buttons_list)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=buttons)
    elif calldata.data == '/prev_page': # Change page to prev and update list
        page = page - 1
        buttons = build_list(buttons_list)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=buttons)
    elif calldata.data == '/prev10_page': # Change page to prev and update list
        page = page - 10
        buttons = build_list(buttons_list)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=buttons)
    elif calldata.data == '/last_page': # Change page to last and update list
        page = math.ceil(len(buttons_list) / 10)
        buttons = build_list(buttons_list)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=buttons)
    elif '/image_' in calldata.data: # Send image
        image = calldata.data.removeprefix('/image_')
        image = capture_folder + image

        try:
            log_print("Trying send image from menu buttons.")
            with open(image, 'rb') as file:
                send_document(calldata.message.chat.id, file, "Ваше изображение: ")
            log_print("File: '" + image + "' opened successfully.")
        except Exception as exc:
            time.sleep(15)
            log_print("#Error - Send list images: ")
            log_print(str(exc))

    log_print("-Stop - Callback handler for list images.")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = str(message.chat.id)
    message_text = message.text

    if chat_id not in users.keys():
        authorization(message)
    else:
        if message_text[0] == '/': # Incorrect command
            log_print("#Error - Receive incorrect command: '" + message_text + "'.")
            send_message(chat_id, "Некорректная команда: " + message_text)
        if message_text.endswith('.jpg'): # Send image if exist (for list_image command)
            if '..' in message_text:
                log_print("!!!Attention!!! - Attempting to access an external folder.")
                send_message(chat_id, "Попытка доступа к внешней папке.")
                send_message(chat_id, "До свидания.")
                users.pop(chat_id, 'None')
            elif glob(capture_folder + message_text):
                send_document(chat_id, capture_folder + message_text, message_text)
            else:
                log_print("#Error - Receive wrong filename: '" + message_text + "'.")
                send_message(chat_id, "Неправильное имя файла.")
        else:
            log_print("#Error - Receive incorrect message: '" + message_text + "'.")
            send_message(chat_id, "Я не чат-бот, используй команды!")



###--------------------------------------------------------------------------###
# Main functions


def start_bot():
    try:
        bot.infinity_polling(timeout=50)
    except Exception as exc:
        log_print("#Error - Bot polling: \n" + str(exc))
        time.sleep(60) # Timeout 60 second
        if infinity == 'True': # To run a bot in a recursive loop
            start_bot()


def check_event():
    # Processing new motion
    while True:
        if master_id: # If the master is registered in the chat
            try:
                with open(event_filename, 'r') as file:
                    new_event = json.load(file)
            except FileNotFoundError:
                log_print("No file: '" + event_filename + "', check step 7 in readme.")
            except Exception as exc:
                log_print("#Error - Save event json: ")
                log_print(str(exc))

            if new_event['event'] == 'True':
                log_print('+Start - Script event processing.')
                log_print("Motion image filename: " + new_event['file'])
                text_message = "Сработал датчик движения видеокамеры."

                try:
                    log_print("Trying to open a file: '" + new_event['file'] + "'.")
                    with open(new_event['file'], 'rb') as file:
                        send_document(master_id, file, text_message)
                    log_print("File: '" + new_event['file'] + "' opened successfully.")
                except FileNotFoundError:
                    log_print("#Error - motion image: '" + new_event['file'] + "' not found.")
                    send_message(master_id, "Не найден файл для отправки, попробуйте еще раз или свяжитесь с Мастером.")
                except Exception as exc:
                    log_print("#Error - Could't send motion image: ")
                    log_print(str(exc))

                yolo_scripts = start_image_object_detection(new_event['file']) # Processing image
                objects = yolo_scripts[0]
                result_image = yolo_scripts[1]

                if objects: # If objects founded
                    founded_str = '' # String for founded objects
                    founded_length = len(objects) - 1
                    for index, value in enumerate(objects):
                        founded_str = founded_str + value
                        if index != founded_length:
                            founded_str = founded_str + ', '
                    objects = [] # Clear array of found objects

                    log_print("Following objects were found in the image: '" + founded_str + "'.")
                    founded_str = 'На изображении были найдены объекты: ' + founded_str + '.' # String for founded objects
                    try:
                        log_print("Trying to open a file: '" + result_image + "'.")
                        with open(result_image, 'rb') as file:
                            send_document(master_id, file, founded_str)
                        log_print("File: '" + result_image + "' opened successfully.")
                    except FileNotFoundError:
                        log_print("#Error - motion image: '" + result_image + "' not found.")
                        send_message(master_id, "Не найден файл для отправки, попробуйте еще раз или свяжитесь с Мастером.")
                    except Exception as exc:
                        log_print("#Error - Could't send result motion image: ")
                        log_print(str(exc))
                else:
                    log_print("No objects in motion image.")
                    send_message(master_id, "Не удалось обнаружить объекты на изображении.")

                new_event['event'] = 'False' # Clear new event flag
                try:
                    log_print("Trying to open a file: '" + event_filename + "'.")
                    with open(event_filename, 'w') as file:
                        json.dump(new_event, file)
                    log_print("File: '" + new_event['file'] + "' opened successfully.")
                except FileNotFoundError:
                    log_print("No file: '" + event_filename + "', check step 7 in readme.")
                except Exception as exc:
                    log_print("#Error - Save event json: ")
                    log_print(str(exc))

                log_print('-Stop - Script event processing.')
            time.sleep(1) # 1 second timeout


###--------------------------------------------------------------------------###


# Start telebot and motion check
Thread(target=start_bot).start()
Thread(target=check_event).start()
