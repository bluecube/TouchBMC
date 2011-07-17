from menu import MenuItem, Menu
from config import config
import sys
#import pygame

class MenuImpl:
    """
    Class that implements the concrete menus for touchbmc.
    """

    def __init__(self, config, xbmc):
        self.config = config

        self.albums_menu = Menu(config)
        self.artists_menu = Menu(config)

#        def image_convert(image):
#            """
#            Change the image to the correct size
#            """
# 
#            allowed_width = int(config["item distance"] * 0.9)
#            allowed_height = int(config["height"] * 0.5)
#            
#            if image.get_width() < allowed_width and image.get_height < allowed_height:
#                return image.convert_alpha()
# 
#            aspect = image.get_width() / float(image.get_height())
#            allowed_aspect = allowed_width / float(allowed_height)
# 
#            if aspect > allowed_aspect:
#                width = allowed_width
#                height = int(allowed_width / aspect)
#            else:
#                width = int(allowed_height * aspect)
#                height = allowed_height
# 
#            image = pygame.transform.smoothscale(image, (width, height))
#            return image.convert_alpha()

        def tracks_action(menuitem, gui, album_id = None):
            pass

        def albums_action(menuitem, gui, artist_id = None):
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
                    pass
                    #image = self.cache.open_http(
                    #    album["thumbnail"], self.config["default album"],
                    #    image_convert)
                else:
                    image = self.cache.open(self.config["default album"])

                def action(menuitem2, gui2):
                    tracks_action(menuitem2, gui2, album["albumid"])

                return MenuItem(image, text, action)

            self.albums_menu.fill(*map(convert, result["albums"]))
            Menu.action_helper(self.albums_menu)(menuitem, gui)

        def artists_action(menuitem, gui):
            """
            Load the list of artists from the XBMC and display the menu.
            """
            
            result = xbmc.call.AudioLibrary.GetArtists()

            def convert(artist):
                text = artist["label"]
                if artist.has_key('thumbnail'):
                    image = self.cache.open_http(
                        artist["thumbnail"], self.config["default artist"],
                        image_convert)
                else:
                    image = self.cache.open(self.config["default artist"])

                def action(menuitem2, gui2):
                    albums_action(menuitem2, gui2, artist["artistid"])

                return MenuItem(image, text, action)

            self.artists_menu.fill(*map(convert, result["artists"]))
            Menu.action_helper(self.artists_menu)(menuitem, gui)
        
        def poweroff_action(menuitem, gui):
            gui.go_back()
            xbmc.call.System.Suspend()

        def playpause_action(menuitem, gui):
            state = ()
            print state
        
        self.power_menu = Menu(
            MenuItem(config["shutdown"], "Power off", poweroff_action),
            MenuItem(config["exit"], "Exit", lambda menuitem, gui: sys.exit()),
        )

        self.library_menu = Menu(
            MenuItem(config["artists"], "Artists ...", artists_action),
            MenuItem(config["albums"], "Albums ...", albums_action),
        )

        self.root = Menu(
            MenuItem(config["prev"], "Previous", lambda menuitem, gui: xbmc.call.AudioPlayer.SkipPrevious()),
            MenuItem(config["next"], "Next", lambda menuitem, gui: xbmc.call.AudioPlayer.SkipNext()),
            MenuItem(config["play"], "Play", lambda menuitem, gui: xbmc.call.AudioPlayer.PlayPause()),
            MenuItem(config["stop"], "Stop", lambda menuitem, gui: xbmc.call.AudioPlayer.Stop()),
            MenuItem(config["artists"], "Artists ...", artists_action),
            MenuItem(config["albums"], "Albums ...", albums_action),
            MenuItem(config["power"], "Power ...",
                Menu.action_helper(self.power_menu)),
            current = 2
        )

    def get_root_menu(self):
        return self.root

