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
- `"data"` will either be `None` or a dictionary containing useful command output
