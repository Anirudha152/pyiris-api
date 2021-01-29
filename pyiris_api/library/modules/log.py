class Main:
	def __init__(self, pyiris_self):
		self.config = pyiris_self.config

	def inf(self, message):
		if self.config.verbose:
			print("\x1b[1m\x1b[34m[*]\x1b[0m" + message)

	def pos(self, message):
		if self.config.verbose:
			print("\x1b[1m\x1b[32m[+]\x1b[0m" + message)

	def war(self, message):
		if self.config.verbose:
			print("\x1b[1m\x1b[33m[!]\x1b[0m" + message)

	def err(self, message):
		if self.config.verbose:
			print("\x1b[1m\x1b[31m[-]\x1b[0m" + message)

	def blank(self, message):
		if self.config.verbose:
			print(message)

	def lod(self, message):
		if self.config.verbose:
			print("\x1b[1m\x1b[34m[...]\x1b[0m" + message)