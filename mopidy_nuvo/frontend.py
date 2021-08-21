import logging
import pykka

from mopidy.core import CoreListener
from .interface import Interface

logger = logging.getLogger(__name__)

class NuvoFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super().__init__()

        self.config = config
        logger.info(config["Mopidy-Nuvo"])
        self.core = core

    def on_start(self):
        self.interface = Interface(self.config,self.core)

    def on_stop(self):
        self.interface.stop()

    def on_event(self, name, **data):
        self.interface.onMopidyEvent(name, **data)

