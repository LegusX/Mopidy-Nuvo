# This code will be handling most of the connection between Nuvo and Mopidy
import logging
import time
import socket

from .connect import Connection

logger = logging.getLogger(__name__)

source = 0
currentTrackLength = 0 # Current track length has to be saved because we have to send it every time the track is seeked
class Interface():
    def __init__(self,config,core):
        global source

        self.config = config
        self.core = core
        self.zones = [False]*20

        source = config["Mopidy-Nuvo"]["source"]

        logger.info(config["Mopidy-Nuvo"])

        self.connection = Connection(config["Mopidy-Nuvo"]["port"], config["Mopidy-Nuvo"]["disable_extra_sources"], source)
        self.connection.listen(self.onNuvoEvent)
        self.connection.send(f"SCFG{source}NUVONET0") #Ensure that the system doesn't mark this as a nuvonet source

        nothingPlaying(self.connection, self.config)

        # Get the current on/off states of all zones
        for x in range(1,20):
            self.connection.send(f"Z{x}STATUS?")

    def onMopidyEvent(self, name, **data):
        if name == 'track_playback_paused':
            paused(self.connection, **data)
        elif name == 'track_playback_ended':
            ended(self.connection, self.core, self.config, **data)
        elif name == 'track_playback_resumed':
            resumed(self.connection, **data)
        elif name == 'track_playback_started':
            started(self.connection, **data)
        elif name == 'seeked':
            seeked(self.connection, **data)
        return

    def onNuvoEvent(self, event):
        if 'PREV' in event:
            self.core.playback.previous()
        elif 'NEXT' in event:
            self.core.playback.next()
        elif 'PLAYPAUSE' in event:
            if self.core.playback.get_state().get() == 'playing':
                self.core.playback.pause()
            else:
                self.core.playback.resume()
        elif ',ON' in event:
            zone = int(event.split(",ON")[0].replace("#Z", "")) # Get the zone number out of the event message
            self.zones[zone-1] = True

            if self.config["Mopidy-Nuvo"]["autopause"] and self.core.playback.get_state().get() == 'paused':
                self.core.playback.resume()
        elif ',OFF' in event:
            zone = int(event.split(",OFF")[0].replace("#Z", "")) # Get the zone number out of the event message
            self.zones[zone-1] = False
            
            if self.config["Mopidy-Nuvo"]["autopause"] and True not in self.zones:
                self.core.playback.pause()


# Informs the Nuvo system that the track has been paused
def paused(connection, tl_track, time_position):
    connection.send(f"S{source}DISPINFO,{round(currentTrackLength/100, 1)},{round(time_position/100, 1)},3")
    return

# Informs the Nuvo system that the track has ended
def ended(connection, core, config, tl_track, time_position):
    connection.send(f"S{source}DISPINFO,{round(currentTrackLength/100, 1)},{round(time_position/100, 1)},1")
    time.sleep(5)
    # If there is still nothing playing after a couple seconds we'll revert to the no music playing screen
    if core.playback.get_state().get() == 'stopped':
        nothingPlaying(connection, config)
    return

# Informs the Nuvo system that the track has resumed
def resumed(connection, tl_track, time_position):
    connection.send(f"S{source}DISPINFO,{round(currentTrackLength/100, 1)},{round(time_position/100, 1)},0")
    return

# Informs the Nuvo system that a new track has started
def started(connection, tl_track):
    global currentTrackLength
    track = tl_track.track

    # Combine all the artists into one list
    artistsList = track.artists.union(track.composers).union(track.performers)
    artists = []
    for artist in artistsList:
        artists.append(artist.name)

    # Update the title/artist/album
    connection.line(source, 1)
    connection.line(source, 2, ", ".join(artists))
    connection.line(source, 3, track.name)
    connection.line(source, 4, track.album.name)

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

# Displays the IP to connect to a web interface like Iris.
# Useful for the less tech savvy members of a household or for when you can't be bothered to remember the IP.
def nothingPlaying(connection, config):
    connection.line(source, 1)
    connection.line(source, 2, "There's nothing playing! Go to:")

    connection.line(source, 3, getIP()+":"+str(config["http"]["port"]))

    connection.line(source, 4, "in your web browser to start playing some music!")

    # Set current timestamp to zero because nothing is playing
    connection.send(f"S{source}DISPINFO,0,0,1")

# Source: https://stackoverflow.com/a/28950776
def getIP():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP