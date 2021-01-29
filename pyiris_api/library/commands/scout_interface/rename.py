# API
# done


def main(self, to_rename, rename_val):
    try:
        self.config.scout_database[str(to_rename)][4] = str(rename_val)
        self.log.pos("Successfully renamed scout " + str(to_rename) + " to " + str(rename_val))
        self.config.change = True
        return {"status": "ok", "message": "Successfully renamed scout " + str(to_rename) + " to " + str(rename_val), "data": None}
    except (IndexError, KeyError):
        self.log.err('Please specify valid values, a valid ID and new name')
        return {"status": "error", "message": "Please specify valid values, a valid ID and new name", "data": None}