import logging
import pykka
import subprocess

from mopidy import core
from .interface import Interface

logger = logging.getLogger(__name__)

class NuvoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super().__init__()

        self.config = config
        self.core = core

    def on_start(self):
        subprocess.run(["sudo", "chmod", "a+rw", self.config["Mopidy-Nuvo"]["port"]])
        logger.info("Starting Mopidy-Nuvo")
        self.interface = Interface(self.config,self.core)

    def on_stop(self):
        self.interface.stop()

    def on_event(self, name, **data):
        logger.info(name)
        self.interface.onMopidyEvent(name, **data)

