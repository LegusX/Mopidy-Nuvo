# Handles the serial connection between the extension and the Grand Concerto/Essentia

import serial

class Connection():
    def __init__(self, config):
        self.config = config