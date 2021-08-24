# Handles the serial connection between the extension and the Grand Concerto/Essentia
import logging
import serial

from threading import Thread
from mopidy import exceptions

logger = logging.getLogger(__name__)


class Connection():
    def __init__(self, port):
        self.serial = serial.Serial()
        self.serial.baudrate = 57600
        self.serial.port = port
        self.serial.open()

        self.limbo = ""

        if not self.serial.is_open:
            raise exceptions.FrontendError("Serial connection could not be opened.")
        else:
            logger.info("Serial connection has been successfully opened")

    def listen(self,callback):
        self.listener = callback
        self.watcher = Watcher(parent=self)
        self.watcher.start()

    def send(self,message):
        self.serial.write(("*"+message+"\r").encode("ascii"))

    def receiving(self):
        self.listener(self.serial.read_until(b"\x0d\x0a").decode("ascii"))
        self.receiving()

    def line(self, source, line, message=""):
        self.send(f'S{source}DISPLINE{line}"{message}"')
        

class Watcher(Thread):
    def __init__(self,parent):
        self.parent = parent
        super(Watcher, self).__init__()
    
    def run(self):
        while True:
            self.parent.listener(self.parent.serial.read_until(b"\x0d\x0a").decode("ascii"))