from models.users import *
from models.status import *
from models.registers import *
from models.mission import *
from models.mission_queue import *
from models.statistics import *
import threading


class Mainvars:
    def __init__(self):
        if "mainvars" not in globals():
            self.unpause_mutex = threading.Lock()
            self.unpause_mutex.acquire()
            self.state_id = 4
            self.robotname = input("Enter robot name: ")
            while True:
                try:
                    self.port = int(input("Enter port number: "))
                    break
                except ValueError:
                    print("Port must be an integer")
        else:
            self.robotname = globals().get("mainvars").robotname
            self.port = globals().get("mainvars").port
            self.state_id = globals().get("mainvars").state_id
            self.unpause_mutex = globals().get("mainvars").unpause_mutex


mainvars = Mainvars()

if __name__ == '__main__':
    # debug changed to False to avoid server restarts while being used by a script
    # you can temporary change to true while developing to restart server automatically on code change
    app.run(debug=False, port=mainvars.port, host="0.0.0.0")
