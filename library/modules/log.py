# GUI
# done
import os
import logging
import inspect
from library.modules import config
from colorlog import ColoredFormatter
config.main()

logging.getLogger('werkzeug').disabled = True

format = "%(log_color)s%(levelname)s%(reset)s >> %(message)s"
level = config.level

logging.root.setLevel(level)
formatter = ColoredFormatter(format)
stream = logging.StreamHandler()
stream.setLevel(level)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(level)
log.addHandler(stream)


def plaintext(text):
	if level == logging.INFO or level == logging.DEBUG:
		log.info(text)


def page_loaded(page):
	if level == logging.INFO or level == logging.DEBUG:
		plaintext("\n--------------------------------------")
		log.info(f"[\033[92m{page}\033[0m] - Loading Page...")


def request_made(request, process):
	if level == logging.INFO or level == logging.DEBUG:
		log.info(f"[\033[94m{process}\033[0m] - {request}")


def log_normal(text):
	if level == logging.INFO or level == logging.DEBUG:
		caller = inspect.getframeinfo(inspect.stack()[1][0])
		filename = caller.filename.split("\\")[-1]
		function = inspect.currentframe().f_back.f_code.co_name + "()"
		line = str(caller.lineno)
		log.info(f"[\x1b[1m\x1b[35m{filename}\x1b[0m/\x1b[1m\x1b[35m{function}\x1b[0m:\x1b[1m\x1b[35m{line}\x1b[0m] - {text}")


def log_warning(text):
	if level == logging.INFO or level == logging.DEBUG or level == logging.WARNING:
		caller = inspect.getframeinfo(inspect.stack()[1][0])
		filename = caller.filename.split("\\")[-1]
		function = inspect.currentframe().f_back.f_code.co_name + "()"
		line = str(caller.lineno)
		log.warning(f"[\x1b[1m\x1b[35m{filename}\x1b[0m/\x1b[1m\x1b[35m{function}\x1b[0m:\x1b[1m\x1b[35m{line}\x1b[0m] - {text}")


def log_error(text):
	if level == logging.INFO or level == logging.DEBUG or level == logging.WARNING or level == logging.ERROR:
		caller = inspect.getframeinfo(inspect.stack()[1][0])
		filename = caller.filename.split("\\")[-1]
		function = inspect.currentframe().f_back.f_code.co_name + "()"
		line = str(caller.lineno)
		log.error(f"[\x1b[1m\x1b[35m{filename}\x1b[0m/\x1b[1m\x1b[35m{function}\x1b[0m:\x1b[1m\x1b[35m{line}\x1b[0m] - {text}")