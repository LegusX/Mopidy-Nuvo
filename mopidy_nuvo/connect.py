# Handles the serial connection between the extension and the Grand Concerto/Essentia
import logging
import serial
import re
import time

from mopidy import exceptions

logger = logging.getLogger(__name__)


class Connection():
    def __init__(self, port):
        self.serial = serial.Serial()
        self.serial.baudrate = 57600
        self.serial.port = port
        self.serial.open()

        self.limbo = ""
        # self.listeners = []

        if not self.serial.is_open:
            raise exceptions.FrontendError("Serial connection could not be opened.")
        else:
            logger.info("Serial connection has been successfully opened")



        # while True:
        #     if hasattr(self, 'listener'):
        #         response = self.serial.read_until(size=20)
        #         message = response.decode("utf-8")
        #         logger.info(message)
        #         self.listener(message)

        
        # while self.serial.in_waiting > 0:
        #     logger.info("data to read.")
        #     read = self.serial.read(self.serial.in_waiting).decode("utf-8")
        #     logger.info(read)

            # if '\x0d\x0a' in read:
            #     responses = read.split('\x0d\x0a')
            #     logger.info(responses)
            #     if self.limbo != "":
            #         responses[0] = self.limbo+responses[0] # Finish off the poor guy stuck in limbo now that we have the last of his response
            #         responses[0] = responses[0].replace('\x0d\x0a', '') # In the highly unlikely chance that the \x0d and \x0a are split up, this is how we deal with it.
            #         self.limbo = ""
            #     for response in responses:
            #         logger.info(response)
            #         self.listener()

            #         # for listener in self.listeners:
            #         #     if listener.check(response):
            #         #         # Check if listener is permanent. If it isn't, then we can remove it so it doesn't get called again
            #         #         if not listener.perm:
            #         #             self.listeners.remove(listener)
            #         #         break # The listener confirmed a match so we can move on
            # else:
            #     self.limbo += read # add what we've read to limbo so we can deal with it at the end of the response
    
    def listen(self,callback):
        self.listener = callback
        self.receiving()

    def send(self,message):
        # logger.info(message)
        self.serial.write(("*"+message+"\r").encode("ascii"))

    def receiving(self):
        buffer = ''
        while True:
            time.sleep(0.02)
            buffer = buffer + self.serial.read(self.serial.in_waiting).decode("ascii")
            if buffer != '':
                logger.info(buffer)
            if '\x0d\x0a' in buffer:
                lines = buffer.split('\x0d\x0a')
                self.listener(lines.pop(0))

                buffer = '\x0d\x0a'.join(lines)


class Listener():
    def __init__(self,match,callback,permanent=False):
        self.cb = callback
        self.regex = match
        self.perm = permanent
    
    def check(self,response):
        match = re.search(self.regex, response)
        if match == None:
            return False
        else:
            self.cb()
            return True

