# This code will be handling most of the connection between Nuvo and Mopidy
import logging
import asyncio

from .connect import Connection

logger = logging.getLogger(__name__)

source = 0
currentTrackLength = 0 # Current track length has to be saved because we have to send it every time the track is seeked
class Interface():
    def __init__(self,config,core):
        global source

        self.config = config
        self.core = core
        source = config["Mopidy-Nuvo"]["source"]

        self.connection = Connection(config["Mopidy-Nuvo"]["port"])
        self.connection.listen(self.buttonHandler)
        self.connection.send(f"SCFG{source}NUVONET0") #Ensure that the system doesn't mark this as a nuvonet source

    def onMopidyEvent(self, name, **data):
        if name == 'track_playback_paused':
            paused(self.connection, **data)
        elif name == 'track_playback_ended':
            ended(self.connection, **data)
        elif name == 'track_playback_resumed':
            resumed(self.connection, **data)
        elif name == 'track_playback_started':
            started(self.connection, **data)
        elif name == 'seeked':
            seeked(self.connection, **data)
        return

    def buttonHandler(self, button):
        logger.info(self)
        logger.info(button)
        logger.info(self.core.__dir__())
        if 'PREV' in button:
            self.core.playback.previous()
        elif 'NEXT' in button:
            self.core.playback.next()
        elif 'PLAYPAUSE' in button:
            if self.core.playback.get_state() == 'PLAYING':
                self.core.playback.pause()
            else:
                self.core.playback.resume()


# Informs the Nuvo system that the track has been paused
def paused(connection, tl_track, time_position):
    return

# Informs the Nuvo system that the track has ended
def ended(connection, tl_track, time_position):
    return

# Informs the Nuvo system that the track has resumed
def resumed(connection, tl_track, time_position):
    return

# Informs the Nuvo system that a new track has started
def started(connection, tl_track):
    global currentTrackLength
    track = tl_track.track

    artistsList = track.artists.union(track.composers).union(track.performers)
    artists = []
    for artist in artistsList:
        artists.append(artist.name)

    # Update the title/artist/album
    connection.send('S{}DISPLINE2"{}"'.format(source, ", ".join(artists)))
    connection.send('S{}DISPLINE3"{}"'.format(source, track.name))
    connection.send('S{}DISPLINE1"{}"'.format(source, track.album.name))

    #Update track status
    connection.send('S{}DISPINFO,{},0,2'.format(source, round(track.length/100), 1))

    currentTrackLength = track.length
    return

# Informs the Nuvo system that the track has been seeked
# Must convert from milliseconds to deciseconds
def seeked(connection, time_position):
    global currentTrackLength
    connection.send('S{}DISPINFO,{},{},0'.format(source, round(currentTrackLength/100, 1), round(time_position/100, 1)))
    return
