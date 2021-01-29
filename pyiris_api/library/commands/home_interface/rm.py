# API
# done


def main(self, list_type, hostname):
    try:
        if list_type == 'wh' or list_type == "whitelist":
            self.config.white_list.remove(hostname)
            self.log.pos("Removed " + hostname + " from Whitelist")
            return {"status": "ok", "message": "Removed " + hostname + " from Whitelist", "data": {"whitelist": self.config.white_list}}
        elif list_type == 'bl' or list_type == "blacklist":
            self.config.black_list.remove(hostname)
            self.log.pos("Removed " + hostname + " from Blacklist")
            return {"status": "ok", "message": "Removed " + hostname + " from Blacklist", "data": {"blacklist": self.config.black_list}}
        else:
            self.log.err("Invalid list_type, use 'bl' for blacklist and 'wh' for whitelist")
            return {"status": "error", "message": "Invalid list_type, use 'bl' for blacklist and 'wh' for whitelist", "data": None}
    except ValueError:
        self.log.err(hostname + " does not exist in " + ["whitelist" if list_type == "wh" else "blacklist" if list_type == "bl" else list_type][0])
        return {"status": "error", "message": hostname + " does not exist in " + ["whitelist" if list_type == "wh" else "blacklist" if list_type == "bl" else list_type][0], "data": None}
