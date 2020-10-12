# GUI + CUI
# done
import time
import library.commands.scout_interface.show as show
import library.commands.scout_interface.rename as rename
import library.commands.scout_interface.kill as kill
import library.commands.scout_interface.sleep as sleep
import library.commands.scout_interface.ping as ping
import library.commands.scout_interface.disconnect as disconnect
import library.interfaces.direct_interface as direct_interface
import library.modules.config as config

try:
    import readline
except ImportError:
    import gnureadline as readline

config.main()
interface = config.interface
if interface == "CUI":
    import library.commands.scout_interface.more as more
    import library.commands.global_interface.clear as clear
    import library.commands.global_interface.quit as quit
    import library.commands.global_interface.python as python
    import library.commands.global_interface.local as local
    import library.commands.global_interface.help as help
elif interface == "GUI":
    from flask import jsonify
scout_commands = ['clear', 'help', 'local', 'python', 'quit', 'bridge', 'disconnect', 'kill', 'more', 'ping', 'rename',
                  'show', 'sleep', 'back']


def scout_completer(text, state):
    for cmd in scout_commands:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


def main(prompt=None):
    if interface == "GUI":
        command = prompt.split(' ', 1)[0].lower()
        if command == "disconnect":
            output = disconnect.main(prompt)
        elif command == "kill":
            output = kill.main(prompt)
        elif command == "ping":
            output = ping.main(prompt)
        elif command == "rename":
            output = rename.main(prompt)
        elif command == "sleep":
            output = sleep.main(prompt)
        elif command == "bridge":
            config.bridged = True
            config.bridged_to = [prompt.split(' ', 1)[1].lower(), config.scout_database[prompt.split(' ', 1)[1].lower()][1] + ":" + config.scout_database[prompt.split(' ', 1)[1].lower()][2]]
            output = jsonify({"output": "Success", "output_message": "Bridging successful", "data": config.bridged_to})
        return output
    elif interface == "CUI":
        readline.parse_and_bind("tab: complete")
        readline.set_completer(scout_completer)
        while True:
            try:
                prompt = input(
                    '\x1b[1m\x1b[37mPyIris (\x1b[0m' + '\x1b[1m\x1b[31mScouts\x1b[0m' + '\x1b[1m\x1b[37m) > \x1b[0m').strip()
                command = prompt.split(' ', 1)[0].lower()
                if command == 'back':
                    print(config.inf + 'Returning...')
                    return
                elif command == 'bridge':
                    stat = direct_interface.main(prompt)
                    if stat == 'home':
                        return
                    readline.parse_and_bind("tab: complete")
                    readline.set_completer(scout_completer)
                elif command == 'clear':
                    clear.main()
                elif command == 'disconnect':
                    disconnect.main(prompt)
                elif command in ('?', 'help'):
                    help.main('scout', prompt)
                elif command == 'kill':
                    kill.main(prompt)
                elif command in ('!', 'local'):
                    local.main(prompt)
                elif command == 'rename':
                    rename.main(prompt)
                elif command == 'sleep':
                    sleep.main(prompt)
                elif command == 'ping':
                    ping.main(prompt)
                elif command == 'python':
                    python.main()
                elif command == 'quit':
                    quit.main()
                elif command == 'show':
                    show.main(prompt)
                elif command == 'more':
                    more.main(prompt)
                elif not command:
                    pass
                else:
                    print(config.neg + 'Invalid command, run "help" for help menu')
            except KeyboardInterrupt:
                quit.main()
