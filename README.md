## motion_cctv_bot  
Setting up motion with a notification in a telegram (screenshot + recognized objects).  
To result go to [Step 14](#14-Results-of-work).  

---
#### 1. Install motion from [git](https://motion-project.github.io/motion_download.html).  

---
#### 2. Create motion folder (for captured images and a log file) and log file:  
    cd ~
    mkdir motion
    mkdir motion/capture
    echo -n > motion/motion.log

---
#### 3. Edit motion.conf (/usr/local/etc/motion/motion.conf):  
    # Enable daemon
    daemon on

    # Path to log file
    log_file /home/_user_/motion/motion.log

    # Directory for captured image
    target_dir /home/_user_/motion/capture

    # Disable video device (camera will be in the config file)
    ; video_device value

    # Enable motion picture
    picture_output first

    # Disable movie output if needed
    movie_output off

    # Threshold for triggers motion detection (default: 1500)
    threshold 2500

    # Automatically tune the noise threshold (default: on)
    noise_tune on

    # Minimum motion frame
    minimum_motion_frames 3

    # Frame for precapture motion
    pre_capture 2

    # Number of frames to capture after motion is no longer detected (default: 0)
    post_capture 1

    # Pause after the end, until a new capture (in seconds)
    event_gap 5

    # The encoding quality of the movie. (0=use bitrate. 1=worst quality, 100=best)
    movie_quality 100

    # The quality (in percent) to be used by the jpeg and webp compression (default: 75)
    picture_quality 100

    # Restrict webcontrol to localhost
    webcontrol_localhost off

    # Restrict stream to localhost
    stream_localhost off

    # Camera config:
    camera /usr/local/etc/motion/camera1.conf

---
#### 4. Edit camera1.conf (/usr/local/etc/motion/camera1.conf):  
    # Camera name (to log file)
    camera_name camera1

    # Camera ID
    camera_id 101

    # Camera (example for my netcam):
    netcam_url rtsp://admin:password@192.168.1.IP/user=admin&password=password&channel=1&stream=1.sdp?real_stream--rtp-caching=100

    # Stream port
    stream_port 8081
    stream_localhost off

    # Image width (for my camera)
    width 704

    # Image height (for my camera)
    height 576

    # Framerate (for my camera)
    framerate 10

    # Picture name
    picture_filename %$_%Y%m%d_%H%M%S_%v

    # Movie name (if movie_output on)
    movie_filename %$_%Y%m%d_%H%M%S_%v

---
#### 5. Install python, telebot, openvc and numpy
    apt install python3 python3-pip
    pip install telebot opencv-python numpy

---
#### 6. To recognize objects using this [script](https://github.com/paveldat/objects_detection_on_image/).  

---
#### 7. Copy the necessary files from program/ to a motion folder.  
+ cctvbot.py  
+ coco.names.txt  
+ credential  
+ event.json  
+ event_change.py  
+ motion_start.sh  
+ motion_detect.sh  
+ password.py  
+ telegram_token  
+ users.json  
+ yolo_script.py  
+ cctvbot.log  
+ variables.py  
+ clear_log.sh # If needed for cleaning (e.g. once a month)

---
#### 8. Create password for your bot:  
8.1. Change password (line 3) in password.py.  
8.2. Run script:  

    python3 password.py

---
#### 9. Change variables for script:  
9.1. Folder for bot files in _variables.py_:  

    motion_folder = '/home/_user_/motion/'
9.2. Folder for captured images in _variables.py_:  

    capture_folder = '/home/_user_/motion/capture/'
9.3. IP for camera webcontrol (localIP:motion_webcontrolport) in _variables.py_:  

    camera_localip = 'http://192.168.0.IP:WebControlPort/00000/' # 00000 - id for all cameras, change if needed
9.4. Log and cctvbot.py files in _motion_start.sh_:  

    _user_ in lines 3-5
9.5. Log and event_change.py files in _motion_detect.sh_:  

    _user_ in lines 3-4

9.6. Log file in _clear_log.sh_:  

    _user_ in line 3
9.7. Types of recognizable objects: now these are:  

+ person  
+ car  
+ truck  
+ bird  
+ dog  
+ cat  

If you need to add other types, then copy the object type from the file 'Resources/coco.names.txt' and add to
variable 'classes_to_look_for' in file: yolo_script.py, line 24.  

---
#### 10. Add event script in camera1.conf (/usr/local/etc/motion/camera1.conf):  
    on_picture_save 'bash /home/_user_/motion/motion_detect.sh %$ %f'

---
#### 11. Create your bot (use [BotFather](https://t.me/BotFather)).  
11.1. Add [BotFather](https://t.me/BotFather) to your telegram.  
11.2. Send /newbot to create new bot.  
11.3. Enter your bot name.  
11.4. Enter your bot login.  
11.5. Paste in telegram_token (motion/telegram_token) your bot token.  
11.6. Next push Edit Bot -> Edit Commands, enter next command (send in one message):  

    current_image - Send current image.
    last_image - Send latest motion image.
    list_images - Send list of all motion images.

---
#### 12. Create and launch autostartup script:  
12.1. Create file:  

    touch /etc/systemd/system/motion_autostartup.service
    chmod 664 /etc/systemd/system/motion_autostartup.service
    nano /etc/systemd/system/motion_autostartup.service

12.2. In file:  

    [Unit]
    Description=Autostartup motion
    [Service]
    Type=oneshot
    RemainAfterExit=true
    User=root
    ExecStart=/home/_user_/motion/motion_start.sh
    [Install]
    WantedBy=multi-user.target

12.3. Launch:  

    systemctl daemon-reload
    systemctl start motion_autostartup.service
    systemctl status motion_autostartup.service
    systemctl enable motion_autostartup.service

---
#### 13. Add your bot in telegram and register.  

---
#### <a name="14-Results-of-work"></a>14. Results of work  
###### Events:  

+ Event 1:  
![event_1](images/events/event_1.png)  
Captured and result:  
[![event_1_captured](images/captured/event_1_captured_preview.jpg)](images/captured/event_1_captured.jpg) [![event_1_result](images/captured/event_1_result_preview.jpg)](images/captured/event_1_result.jpg)  

+ Event 2:  
![event_2](images/events/event_2.png)  
Captured and result:  
[![event_2_captured](images/captured/event_2_captured_preview.jpg)](images/captured/event_2_captured.jpg) [![event_2_result](images/captured/event_2_result_preview.jpg)](images/captured/event_2_result.jpg)  

+ Event 3:  
![event_3](images/events/event_3.png)  
Captured and result:  
[![event_3_captured](images/captured/event_3_captured_preview.jpg)](images/captured/event_3_captured.jpg) [![event_3_result](images/captured/event_3_result_preview.jpg)](images/captured/event_3_result.jpg)  

###### Commands:  

+ Current image:  
![command_current_image](images/commands/command_current.png)

+ Last motion image:  
![command_last_image](images/commands/command_last.png)

+ List all motion images:  
[![command_list_1](images/commands/command_list_1_preview.png)](images/commands/command_list_1.png) 
[![command_list_2](images/commands/command_list_2_preview.png)](images/commands/command_list_2.png) 
[![command_list_3](images/commands/command_list_3_preview.png)](images/commands/command_list_3.png) 
[![command_list_4](images/commands/command_list_4_preview.png)](images/commands/command_list_4.png)  
And getting the required images:  
[![image_get_1](images/commands/image_get_1_preview.jpg)](images/commands/image_get_1.jpg) 
[![image_get_2](images/commands/image_get_2_preview.jpg)](images/commands/image_get_2.jpg)  

###### Funny objects:  

+ Funny 1:  
![funny_1](images/funny/funny_1.png)  
Object:  
[![funny_1_result](images/funny/funny_1_result_preview.jpg)](images/funny/funny_1_result.jpg)  

+ Funny 2:  
![funny_2](images/funny/funny_2.png)  
Object:  
[![funny_2_result](images/funny/funny_2_result_preview.jpg)](images/funny/funny_2_result.jpg)  

+ Funny 3:  
![funny_3](images/funny/funny_3.png)  
Object:  
[![funny_3_result](images/funny/funny_3_result_preview.jpg)](images/funny/funny_3_result.jpg)  