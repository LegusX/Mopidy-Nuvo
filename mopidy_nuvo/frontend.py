import logging
import pykka

from mopidy import core
from .connect import Connection

logger = logging.getLogger(__name__)

class NuvoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(NuvoFrontend, self).__init__()
        print(config)
        self.core = core

        self.con = Connection(config)

