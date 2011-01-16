import os
import pygame
import weakref
import urllib

class ImageCache:
    """
    Loading and caching of image surfaces.
    """

    def __init__(self, config):
        self.CACHE_DIR = config["cache dir"]

        if not os.path.exists(self.CACHE_DIR):
            print "Making directory " + self.CACHE_DIR
            os.mkdir(self.CACHE_DIR)

        self.DL_URL = "http://" + config["host"] + ":" + str(config["dl port"]) + "/vfs/"

        self.cache = weakref.WeakValueDictionary()

    def open_http(self, path, modify_func = None):
        """
        Returns a cached version of remote image.
        If modify_func is callable then it is given the 
        opened picture and its return value is stored in the cache.
        If modify_func is not callable convert_alpha() is used.
        """
        path = urllib.quote(path, '')
    
        cached_path = os.path.join(self.CACHE_DIR, path)

        if not os.path.exists(cached_path):
            urllib.urlretrieve(self.DL_URL + name, cached_path)
        
        return self.open(cached_path, modify_func)

    def open(self, path, modify_func = None):
        """
        Returns a cached version of a local file.
        If modify_func is callable then it is given the 
        opened picture and its return value is stored in the cache.
        """
        if self.cache.has_key(path):
            return self.cache[path]
        else:
            image = pygame.image.load(path)
            if callable(modify_func):
                image = modify_func(image)
            else:
                image = image.convert_alpha()

            self.cache[path] = image
            return image
