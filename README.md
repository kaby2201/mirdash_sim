# Robot simulation API
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
