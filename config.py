from __future__ import unicode_literals

config = {}

config["left"] = "skin/left.png"
config["right"] = "skin/right.png"
config["back"] = "skin/left.png"
config["prev"] = "skin/prev.png"
config["next"] = "skin/next.png"
config["play"] = "skin/play.png"
config["next"] = "skin/next.png"
config["stop"] = "skin/stop.png"
config["power"] = "skin/power.png"
config["shutdown"] = "skin/power.png"
config["exit"] = "skin/close.png"
config["artists"] = "skin/artist.png"
config["albums"] = "skin/album.png"
config["default artist"] = "skin/artist.png"
config["default album"] = "skin/album.png"

config["caption"] = "TouchBMC"

config["antialias"] = True

config["fps"] = 20
config["update fps"] = 2

config["menu scroll time"] = 0.5
config["hide fg counter top"] = 4 # in 5 sec units
config["item distance"] = 200
config["drag offset"] = 50
config["drag area"] = 520

config["a lot of items"] = 30

config["width"] = 800
config["height"] = 600

config["font"] = "Bitstream Vera Sans"
config["font size"] = 48
config["font color"] = (100, 100, 100)

config["bg font"] = "Bitstream Vera Sans"
config["bg font size"] = 64
config["bg font color"] = (100, 100, 100)
config["bg font pos"] = (10, 10)
config["bg font alpha"] = 128
config["bg text"] = (
    "{title}",
    "{artist}",
    "{album}",
    "{time} / {duration}"
)


config["bar alpha"] = 128

config["HierarchicalMenu font"] = "Bitstream Vera Sans"
config["HierarchicalMenu font size"] = 150
config["HierarchicalMenu font color"] = (30, 30, 30)

config["jsonrpc url"] = "http://10.0.0.200/jsonrpc"
config["vfs url"] = "http://10.0.0.200/vfs/"

config["cache dir"] = "/tmp/cache/"
