****************************
Mopidy-Nuvo
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Nuvo
    :target: https://pypi.org/project/Mopidy-Nuvo/
    :alt: Latest PyPI version

Mopidy extension for using Nuvo control pads as a Mopidy frontend.


Installation
============

Install by running::

   sudo python3 -m pip install Mopidy-Nuvo

See https://mopidy.com/ext/Mopidy-Nuvo/ for alternative installation methods.

Connecting to your Grand Concerto or Essentia system
====================================================
*Please note: This was designed for the Grand Concerto and I cannot promise it'll work on the Essentia, but from everything I've read it should work in a similar fashion.*
1. Connect your server to the Grand Concerto/Essentia as a source. 
    On the back of the system there should be 6 RCA audio ports. If you're using the built in aux port on your system, you will likely need an aux to RCA converter for this. Take note of what source number you are connected to because you will need this for configuration.
2. Connect your server to the Grand Concerto/Essentia over serial.
    On the back of the system you will find a serial port labeled::
        "Programming and Serial Control" - Grand Concerto
        "RS232" - Essentia
    
    
    You will need to connect to this port through a serial cable. Once you've done so, figure out what the port it is so you can put it in the configuration.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Nuvo to your Mopidy configuration file::

    [Mopidy-Nuvo]
    enabled = false
    # What source number your Pi is connected to
    source = 1
    # What port the serial connection is on
    port = /dev/ttyUSB0
    # Disable any other source that isn't used by the Pi. Only do this if Mopidy is the only thing you want to use with your Nuvo
    disable_extra_sources = false 
    # Automatically pause your music if all zones are turned off, and unpause once one is turned on. (Doesn't do anything yet)
    autopause = true 


Project resources
=================

- `Source code <https://github.com/LegusX/mopidy-nuvo>`_
- `Issue tracker <https://github.com/LegusX/mopidy-nuvo/issues>`_
- `Changelog <https://github.com/LegusX/mopidy-nuvo/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Logan Henrie <https://github.com/LegusX>`__
- Current maintainer: `Logan Henrie <https://github.com/LegusX>`__
- `Contributors <https://github.com/LegusX/mopidy-nuvo/graphs/contributors>`_
