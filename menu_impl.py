from menu import MenuItem, Menu, HierarchicalMenu
from xbmc import Xbmc
from config import config
import sys

xbmc = Xbmc(config)

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
        if 'thumbnail' in album:
            image = xbmc.get_file(album["thumbnail"])
        else:
            image = "circle.png"

        def action(gui2):
            tracks_action(gui2, album["albumid"])

        return (image, text, action)

    albums_action.menu.fill(*map(convert, result["albums"]))

    Menu.action_helper(albums_action.menu)(gui)

def artists_action(gui):
    """
    Load the list of artists from the XBMC and display the menu.
    """
    
    result = xbmc.call.AudioLibrary.GetArtists()

    def convert(artist):
        text = artist["label"]
        if 'thumbnail' in artist:
            image = xbmc.get_file(artist["thumbnail"])
        else:
            image = "circle.png"

        def action(gui2):
            albums_action(gui2, artist["artistid"])

        return (image, text, action)

    artists_action.menu.fill(*map(convert, result["artists"]))

    Menu.action_helper(artists_action.menu)(gui)

artists_action.menu = HierarchicalMenu(config)
albums_action.menu = HierarchicalMenu(config)

library_menu = Menu(
    ("circle.png", "Artists ...", artists_action),
    ("circle.png", "Albums ...", albums_action),
)

power_menu = Menu(
    ("power.png", "Power off", 0),
    ("close.png", "Exit", lambda gui: sys.exit()),
)

root_menu = Menu(
    ("prev.png", "Previous", 0),
    ("circle.png", "Library ...", Menu.action_helper(library_menu)),
    ("play.png", "Play", 0),
    ("next.png", "Next", 0),
    ("stop.png", "Stop", 0),
    ("power.png", "Power ...", Menu.action_helper(power_menu)),
    current = 2
)

