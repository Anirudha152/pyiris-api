# WEB + COM
# done
import time
import library.commands.global_interface.quit as quit
import library.commands.home_interface.regen as regen
import library.commands.home_interface.add as add
import library.commands.home_interface.rm as rm
import library.commands.home_interface.reset as reset
import library.modules.config as config
import library.commands.home_interface.show as show

config.main()
interface = config.interface
if interface == "CUI":
    import library.commands.global_interface.clear as clear
    import library.commands.global_interface.python as python
    import library.commands.global_interface.local as local
    import library.commands.global_interface.help as help
    import library.interfaces.listener_interface as listener_interface
    import library.interfaces.scout_interface as scout_interface
    import library.interfaces.generator_interface as generator_interface

try:
    import readline
except ImportError:
    import gnureadline as readline


home_commands = ['clear', 'help', 'local', 'python', 'quit', 'add', 'regen', 'reset', 'rm', 'show', 'generator',
                 'listeners',
                 'scouts']


def home_completer(text, state):
    for cmd in home_commands:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


def main(prompt = None):
    if interface == "GUI":
        command = prompt.split(' ', 1)[0].lower()
        if command == 'add':
            output = add.main(prompt)
        elif command == 'regen':
            output = regen.main(prompt)
        elif command == 'rm':
            output = rm.main(prompt)
        elif command == 'reset':
            output = reset.main(prompt)
        elif command == 'show':
            output = show.main(prompt)
        return output
    elif interface == "CUI":
        readline.parse_and_bind("tab: complete")
        readline.set_completer(home_completer)
        while True:
            try:
                prompt = input('\x1b[1m\x1b[37mPyIris (Home) > \x1b[0m').strip()
                command = prompt.split(' ', 1)[0].lower()
                if command == 'add':
                    add.main(prompt)
                elif command == 'clear':
                    clear.main()
                elif command == 'generator':
                    print(config.inf + 'Switching...')
                    generator_interface.main()
                    readline.parse_and_bind("tab: complete")
                    readline.set_completer(home_completer)
                elif command in ('?', 'help'):
                    help.main('home', prompt)
                elif command == 'listeners':
                    print(config.inf + 'Switching...')
                    listener_interface.main()
                    readline.parse_and_bind("tab: complete")
                    readline.set_completer(home_completer)
                elif command in ('!', 'local'):
                    local.main(prompt)
                elif command == 'python':
                    python.main()
                elif command == 'quit':
                    quit.main()
                elif command == 'regen':
                    regen.main()
                elif command == 'reset':
                    reset.main(prompt)
                elif command == 'rm':
                    rm.main(prompt)
                elif command == 'scouts':
                    print(config.inf + 'Switching...')
                    scout_interface.main()
                    readline.parse_and_bind("tab: complete")
                    readline.set_completer(home_completer)
                elif command == 'show':
                    show.main(prompt)
                elif not command:
                    pass
                else:
                    print(config.neg + 'Invalid command, run "help" for help menu')
            except EOFError:
                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    quit.main()
            except KeyboardInterrupt:
                quit.main()


