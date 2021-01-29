# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import alsaaudio')
        self.config.functions.append('''
def set_audio(data):
    vol_level = data.split(' ',1)[1]
    vol = alsaaudio.Mixer(alsaaudio.mixers()[0])
    vol.setvolume(int(vol_level))
    send_all(s,'[+]Set volume to : ' + str(vol_level))''')
        self.config.logics.append('''
            elif command == "set_audio":
                set_audio(data)''')
        self.config.help_menu['set_audio <number>'] = 'Set system wide audio level by percentage, volume range is 0-100'
    elif option == 'info':
        self.log.blank('\nName             : Set Audio component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : alsaaudio (external)' \
                       '\nCommands         : set_audio <number>' \
                       '\nDescription      : Sets the system audio levels\n')
        return {
            "Name": "Set Audio component",
            "OS": "Linux",
            "Required Modules": "alsaaudio (external)",
            "Commands": "set_audio <number>",
            "Description": "Sets the system audio levels"
        }