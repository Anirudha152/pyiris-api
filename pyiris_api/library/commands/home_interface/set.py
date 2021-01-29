# API
#


def main(self, list_type, set_to):
	if type(set_to) == list:
		if list_type == 'wh' or list_type == "whitelist":
			self.config.white_list = set_to
			self.config.white_list = list(set(self.config.white_list))
			self.log.pos("Set whitelist to " + str(self.config.white_list))
			return {"status": "ok", "message": "Set whitelist to " + str(self.config.white_list), "data": {"whitelist": self.config.white_list}}
		elif list_type == 'bl' or list_type == "blacklist":
			self.config.black_list = set_to
			self.config.black_list = list(set(self.config.black_list))
			self.log.pos("Set blacklist to " + str(self.config.black_list))
			return {"status": "ok", "message": "Set blacklist to " + str(self.config.black_list), "data": {"blacklist": self.config.black_list}}
		else:
			self.log.err("Invalid list_type, use 'bl' for blacklist and 'wh' for whitelist")
			return {"status": "error", "message": "Invalid list_type, use 'bl' for blacklist and 'wh' for whitelist", "data": None}
	else:
		self.log.err("Invalid set_to type, it must be a list")
		return {"status": "error", "message": "Invalid set_to type, it must be a list", "data": None}
