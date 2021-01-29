# API
# done


def main(self, list_type, hostname):
    if list_type == 'wh' or list_type == "whitelist":
        self.config.white_list.append(hostname)
        self.config.white_list = list(set(self.config.white_list))
        self.log.pos("Added " + hostname + " to whitelist")
        return {"status": "ok", "message": "Added " + hostname + " to whitelist", "data": {"whitelist": self.config.white_list}}
    elif list_type == 'bl' or list_type == "blacklist":
        self.config.black_list.append(hostname)
        self.config.black_list = list(set(self.config.black_list))
        self.log.pos("Added " + hostname + " to blacklist")
        return {"status": "ok", "message": "Added " + hostname + " to blacklist", "data": {"blacklist": self.config.black_list}}
    else:
        self.log.err("Invalid list_type, use 'bl' for blacklist and 'wh' for whitelist")
        return {"status": "error", "message": "Invalid list_type, use 'bl' for blacklist and 'wh' for whitelist", "data": None}
