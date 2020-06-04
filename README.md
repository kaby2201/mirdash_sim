## MiRDash SIM API
### A mobile industrial robots simulator API

### API support:
* MIR100 REST API 2.8.3
* MiR200 MIR200 REST API 2.8.3
* MIR500 REST API 2.8.3

### Project setup
The description below are for pycharm, do your search for other ede's.
You will need to create an isolated environment. 
* Start pyCharm and navigate to  "Settings"
* Click on Project Interpreter
* Click then on Add, to add a new environment
* Click then on Ok
* Install the required models, open terminal in Pycharm terminal and run the command
``
pip install -r requirements.txt
``

* Try to run the application, if you get the error "ImportError: connot import name 'cachedproporty' from werkezeug'"
* In your project go to ``\venv\lib\site-packages\fask_restplus\fields.py`` on line 17 update the line to
``
from werkzeug.utils import cached_property
``

* In your project go to ``\venv\lib\site-packages\fask_restplus\api.py`` on line 24 update the line to
``
from werkzeug.utils import cached_property
``


### Terminal commands

    Initial installation: make install

    To run test: make tests

    To run application: make run

    To run all commands at once : make all


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.


### Contributing
If you want to contribute to this mirdash sim, clone the repository and just start making pull requests.

```
https://github.com/kaby2201/mirdash_sim.git
```