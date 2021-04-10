# API
# done
import os
import shutil
import pyiris_api


def main(self, compiler_settings):
    local_dir = os.getcwd()
    if os.name == 'nt':
        filename = 'payload.exe'
    else:
        filename = 'payload'
    self.log.inf("Initiating compilation of scout : " + local_dir)
    tags = []

    if "onefile" not in compiler_settings.keys():
        tags.append("--onefile")
    else:
        if compiler_settings["onefile"]:
            tags.append("--onefile")
    if "windowed" in compiler_settings.keys():
        if compiler_settings['windowed']:
            tags.append('--windowed')
    if "custom_icon_filepath" in compiler_settings.keys():
        if compiler_settings['custom_icon_filepath'] != "":
            if os.path.exists(compiler_settings['custom_icon_filepath']):
                self.log.pos("Custom .ico file found and loaded")
                tags.append('--icon "' + compiler_settings['custom_icon_filepath'] + '"')
            else:
                self.log.war("Custom .ico file not found")
                tags.append('--icon "' + os.path.join(pyiris_api.__path__[0], 'resources', 'windows_service.ico') + '"')
                self.log.inf("Default .ico file used")
        else:
            tags.append('--icon "' + os.path.join(pyiris_api.__path__[0], 'resources', 'windows_service.ico') + '"')
            self.log.inf("Default .ico file used")
    else:
        tags.append('--icon "' + os.path.join(pyiris_api.__path__[0], 'resources', 'windows_service.ico') + '"')
        self.log.inf("Default .ico file used")
    command = 'pyinstaller ' + ' '.join(tags) + ' payload.py'
    self.log.inf('Removing residue folders...')
    for i in ['build', 'dist', '__pycache__']:
        if os.path.isdir(os.path.join(os.getcwd(), i)):
            shutil.rmtree('build')
    for i in os.listdir(os.getcwd()):
        if i.endswith('.spec'):
            os.remove(i)
    self.log.inf('Compiling file...')
    os.system(command)
    # remove garbage dirs and copy compiled exe out of dist into the root//local_datetime folder
    if os.path.isdir(os.path.join(os.getcwd(), 'build')):
        shutil.rmtree('build')
    else:
        self.log.err('Error, could not successfully compile scout (Is "pyinstaller" installed and visible iFn your PATH?)')
        return {"status": "error", "message": 'Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)', "data": None}

    if os.path.exists(os.path.join(os.getcwd(), 'dist', filename)):  # single file scout compiled
        shutil.copy(os.path.join(os.getcwd(), 'dist', filename), os.path.join(os.getcwd(), filename))
        shutil.rmtree('dist')
        self.log.pos('Successfully compiled single file scout to : ' + os.path.join(os.getcwd(), filename))
    elif os.path.isdir(os.path.join(os.getcwd(), 'dist', 'payload')):  # folder scout
        self.log.pos('Successfully compiled scout, scout folder is located at : ' + os.path.join(os.getcwd(), 'dist', 'payload'))
    else:
        self.log.err('Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)')
        return {"status": "error", "message": 'Error, could not successfully compile scout (Is "pyinstaller" installed and visible in your PATH?)', "data": None}
    if os.path.isdir(os.path.join(os.getcwd(), '__pycache__')):
        shutil.rmtree('__pycache__')
    for i in os.listdir(os.getcwd()):
        if i.endswith('.spec'):
            os.remove(i)
    return {"status": "ok", "message": "Generation and Compilation Successful", "data": None}