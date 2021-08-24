import logging
import pathlib
import pkg_resources

from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-Nuvo").version

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-Nuvo"
    ext_name = "Mopidy-Nuvo"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        # TODO: Comment in and edit, or remove entirely
        schema["source"] = config.Integer(minimum=0,maximum=6)
        schema["port"] = config.String()
        schema["disable_extra_sources"] = config.Boolean()
        schema["autopause"] = config.Boolean()
        return schema

    def setup(self, registry):
        from .frontend import NuvoFrontend
        registry.add("frontend", NuvoFrontend)
