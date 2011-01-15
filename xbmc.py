import urllib
import os

import jsonrpc2

class Xbmc:
    def __init__(self, config):
        self.call = jsonrpc2.JsonRPCProxy((config["host"], config["port"]))

        self.CACHE_DIR = config["cache dir"]

        if not os.path.exists(self.CACHE_DIR):
            print "Making directory " + self.CACHE_DIR
            os.mkdir(self.CACHE_DIR)

        self.DL_URL = "http://" + config["host"] + ":" + str(config["dl port"]) + "/vfs/"

    def get_file(self, name):
        """
        Returns a path of a cached (local) version of the file from the xbmc store.
        """
        name = urllib.quote(name, '')
    
        cached_name = os.path.join(self.CACHE_DIR, name)

        if not os.path.exists(cached_name):
            urllib.urlretrieve(self.DL_URL + name, cached_name)
            
        return cached_name

    
