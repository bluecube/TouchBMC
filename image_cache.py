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

        self.DL_URL = config["vfs url"]

        self.cache = weakref.WeakValueDictionary()

    def open_http(self, path, alternate_path = None, modify_func = None):
        """
        Returns a cached version of remote image.
        alternate_path is a path to a local image that is used if the remote
        image cannot be retreived.
        If modify_func is callable then it is given the 
        opened picture and its return value is stored in the cache.
        If modify_func is not callable convert_alpha() is used.
        """
        path = urllib.quote(path, '')
    
        cached_path = os.path.join(self.CACHE_DIR, path)

        if not os.path.exists(cached_path):
            url = self.DL_URL + path
            try:
                urllib.urlretrieve(url, cached_path)
            except IOError:
                print "Retreiving remote image " + url + " failed."
                if alternate_path:
                    return self.open(alternate_path, modify_func)
                else:
                    raise
        
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
