# API
# done


def main(self, list_type):
	if list_type == 'wh' or list_type == "whitelist":
		if len(self.config.white_list) > 0:
			self.log.pos('Whitelisted hosts : ')
			for i in self.config.white_list:
				self.log.blank('   ' + i)
			self.log.blank('')
		else:
			self.log.inf('No Whitelisted hosts')
		return {"status": "ok", "message": "", "data": {"whitelist": self.config.white_list}}
	elif list_type == 'bl':
		if len(self.config.black_list) > 0:
			self.log.pos('Blacklisted hosts : ')
			for i in self.config.black_list:
				self.log.blank('   ' + i)
			self.log.blank('')
		else:
			self.log.inf('No Blacklisted hosts')
		return {"status": "ok", "message": "", "data": {"blacklist": self.config.black_list}}
	elif list_type == 'all':
		if len(self.config.black_list) > 0:
			self.log.pos('Whitelisted hosts : ')
			for i in self.config.white_list:
				self.log.blank('   ' + i)
			self.log.blank('')
		else:
			self.log.inf('No Whitelisted hosts')
		if len(self.config.black_list) > 0:
			self.log.pos('Blacklisted hosts : ')
			for i in self.config.black_list:
				self.log.blank('   ' + i)
			self.log.blank('')
		else:
			self.log.inf('No Blacklisted hosts')
		return {"status": "ok", "message": "", "data": {"whitelist": self.config.white_list, "blacklist": self.config.black_list}}
	elif list_type == 'key':
		self.log.inf('Currently used key : ')
		self.log.blank('   ' + self.config.key)
		return {"status": "ok", "message": "", "data": {"key": self.config.key}}
	else:
		self.log.err("Invalid list_type use 'bl' for blacklist, 'wh' for whitelist, 'all' for both and 'key' for the key")
		return {"status": "error", "message": "Invalid list_type use 'bl' for blacklist, 'wh' for whitelist, 'all' for both and 'key' for the key", "data": None}
