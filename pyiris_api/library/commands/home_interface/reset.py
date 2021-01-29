# API
# done


def main(self, list_type):
    if list_type == 'wh' or list_type == "whitelist":
        self.config.white_list = []
        self.log.pos('Reset Whitelist')
        return {"status": "ok", "message": "Reset Whitelist", "data": {"whitelist": self.config.white_list}}
    elif list_type == 'bl' or list_type == "blacklist":
        self.config.black_list = []
        self.log.pos('Reset Blacklist')
        return {"status": "ok", "message": "Reset Blacklist", "data": {"blacklist": self.config.black_list}}
    elif list_type == 'all':
        self.config.white_list = []
        self.config.black_list = []
        self.log.pos('Reset All')
        return {"status": "ok", "message": "Reset All", "data": {"whitelist": self.config.white_list, "blacklist": self.config.black_list}}
    else:
        self.log.err("Invalid list_type, use 'bl' for blacklist, 'wh' for whitelist or 'all' for both lists")
        return {"status": "error", "message": "Invalid list_type, use 'bl' for blacklist, 'wh' for whitelist or 'all' for both lists", "data": None}
