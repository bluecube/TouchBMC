from menu import MenuItem, Menu, HierarchicalMenu
from config import config
import sys
import pygame

class MenuImpl:
    """
    Class that implements the concrete menus for touchbmc.
    """

    def __init__(self, config, xbmc, cache):
        self.cache = cache
        self.config = config

        self.albums_menu = HierarchicalMenu(config)
        self.artists_menu = HierarchicalMenu(config)

        def image_convert(image):
            """
            Change the image to the correct size
            """

            width = int(config["item distance"] * 0.9)
            if image.get_width() > width:
                height = int(image.get_height() * float(width) / image.get_width())
                image = pygame.transform.smoothscale(image, (width, height))

            return image.convert_alpha()

        def tracks_action(gui, album_id = None):
            pass

        def albums_action(gui, artist_id = None):
            """
            Load the list of artists from the XBMC and display the menu.
            """
            
            if artist_id:
                result = xbmc.call.AudioLibrary.GetAlbums(artistid = artist_id)
            else:
                result = xbmc.call.AudioLibrary.GetAlbums()

            def convert(album):
                text = album["label"]
                if album.has_key('thumbnail'):
                    image = self.cache.open_http(album["thumbnail"], image_convert)
                else:
                    image = self.cache.open(self.config["default album"])

                def action(gui2):
                    tracks_action(gui2, album["albumid"])

                return MenuItem(image, text, action)

            self.albums_menu.fill(*map(convert, result["albums"]))
            Menu.action_helper(self.albums_menu)(gui)

        def artists_action(gui):
            """
            Load the list of artists from the XBMC and display the menu.
            """
            
            result = xbmc.call.AudioLibrary.GetArtists()

            def convert(artist):
                text = artist["label"]
                if artist.has_key('thumbnail'):
                    image = self.cache.open_http(artist["thumbnail"], image_convert)
                else:
                    image = self.cache.open(self.config["default artist"])

                def action(gui2):
                    albums_action(gui2, artist["artistid"])

                return MenuItem(image, text, action)

            self.artists_menu.fill(*map(convert, result["artists"]))
            Menu.action_helper(self.artists_menu)(gui)
        
        def poweroff_action(gui):
            gui.go_back()
            xbmc.call.System.Suspend()

        self.power_menu = Menu(
            MenuItem(cache.open(config["shutdown"]), "Power off", poweroff_action),
            MenuItem(cache.open(config["exit"]), "Exit", lambda gui: sys.exit()),
        )

        self.library_menu = Menu(
            MenuItem(cache.open(config["artists"]), "Artists ...", artists_action),
            MenuItem(cache.open(config["albums"]), "Albums ...", albums_action),
        )

        self.root = Menu(
            MenuItem(cache.open(config["prev"]), "Previous", 0),
            MenuItem(cache.open(config["library"]), "Library ...",
                Menu.action_helper(self.library_menu)),
            MenuItem(cache.open(config["play"]), "Play", 0),
            MenuItem(cache.open(config["next"]), "Next", 0),
            MenuItem(cache.open(config["stop"]), "Stop", 0),
            MenuItem(cache.open(config["power"]), "Power ...",
                Menu.action_helper(self.power_menu)),
            current = 2
        )

    def get_root_menu(self):
        return self.root

