from __future__ import unicode_literals

import urllib
import os

import jsonrpc.proxy


class Xbmc:
    PLAYING, PAUSED, IDLE = range(3)

    def __init__(self, config):
        self.call = jsonrpc.proxy.JSONRPCProxy.from_url(config["jsonrpc url"])

        self.CACHE_DIR = config["cache dir"]

        if not os.path.exists(self.CACHE_DIR):
            print "Making directory " + self.CACHE_DIR
            os.mkdir(self.CACHE_DIR)

    @property
    def player_status(self):
        try:
            result = self.call.AudioPlayer.State()
        except jsonrpc.common.RPCError as e:
            if e.code == -32100:
                return self.IDLE
            
            raise

        if result['paused']:
            return self.PAUSED

        return self.PLAYING

    def get_file(self, name):
        """
        Returns a path of a cached (local) version of the file from the xbmc store.
        """
        name = urllib.quote(name, '')
    
        cached_name = os.path.join(self.CACHE_DIR, name)

        if not os.path.exists(cached_name):
            urllib.urlretrieve(self.DL_URL + name, cached_name)
            
        return cached_name

    @property
    def labels(self):
        """
        Returns a dictionary with information about a playing track.
        """

        labels = self.call.System.GetInfoLabels([
            "MusicPlayer.Title",
            "MusicPlayer.Album",
            "MusicPlayer.Artist",
            "Player.Time",
            "Player.Duration"])

        ret = {}
        ret["title"] = labels["MusicPlayer.Title"]
        ret["album"] = labels["MusicPlayer.Album"]
        ret["artist"] = labels["MusicPlayer.Artist"]
        ret["time"] = labels["Player.Time"]
        ret["duration"] = labels["Player.Duration"]

        return ret
        
