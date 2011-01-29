import urllib
import os

import json_rpc2_proxy

class Xbmc:
    def __init__(self, config):
        self.call = json_rpc2_proxy.JsonRPCProxy((config["host"], config["port"]))

        self.CACHE_DIR = config["cache dir"]

        if not os.path.exists(self.CACHE_DIR):
            print "Making directory " + self.CACHE_DIR
            os.mkdir(self.CACHE_DIR)

    def get_file(self, name):
        """
        Returns a path of a cached (local) version of the file from the xbmc store.
        """
        name = urllib.quote(name, '')
    
        cached_name = os.path.join(self.CACHE_DIR, name)

        if not os.path.exists(cached_name):
            urllib.urlretrieve(self.DL_URL + name, cached_name)
            
        return cached_name

    def get_status(self):
        """
        Returns a dictionary with information about a playing track.
        """
        ret = {}
        try:
            time = self.call.AudioPlayer.GetTime()
        except json_rpc2_proxy.JsonRPCException as e:
            if e.code != -32100:
                raise

            ret["playing"] = False
            return ret
        else:
            ret["playing"] = True
            ret["minute"], ret["second"] = divmod(time["time"], 60)
            ret["minute_total"], ret["second_total"] = divmod(time["total"], 60)
        
        ret["title"] = ""
        ret["artist"] = ""
        ret["album"] = ""

        return ret
        
