# API
# done


def main(self, id):
    if id in list(self.config.listener_database.keys()):
        return False
    else:
        return True
