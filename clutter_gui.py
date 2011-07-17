from __future__ import print_function
from __future__ import division

import clutter

import menu

from pprint import pprint

class Gui:
    TOP_LAYER_DEPTH = 0
    BUTTON_PRESS_DEPTH = 20
    MENU_INACTIVE_DEPTH = -1000
    MENU_ACTIVE_DEPTH = -1

    MENU_STEP = 200

    def __init__(self, config):
        self._config = config

        # stage
        self._stage = clutter.Stage()
        self._stage.set_size(config["width"], config["height"])
        self._stage.set_title(config["caption"])
        self._stage.connect("destroy", clutter.main_quit)
        self._stage.set_color(clutter.Color(0, 0, 0, 255))

        # background texture
        #self._bg = clutter.Texture(config["background"])
        #self._stage.add(self._bg)
        #self._bg.set_position(0, 0)
        #self._bg.set_size(self._stage.get_width(), self._stage.get_height())
        #self._bg.show()

        x_6 = self._stage.get_width() // 6
        y_6 = self._stage.get_height() // 6

        self._left = self._add_arrow("left", x_6, 3 * y_6, self._left_clicked)
        self._right = self._add_arrow("right", 5 * x_6, 3 * y_6, self._right_clicked)
        self._back = self._add_arrow("back", x_6, y_6, self._back_clicked)

        self._menu_row = None

        self._stage.show()

    def _add_arrow(self, image, x, y, arrow_action):
        arrow = clutter.Texture(self._config[image])
        self._stage.add(arrow)

        arrow.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
        arrow.set_position(x, y)
        arrow.set_depth(self.TOP_LAYER_DEPTH)

        arrow.set_reactive(True)
        arrow.connect('button-press-event', arrow_action)

        arrow.show()

        return arrow

    def _create_menu_row(self, menu):
        if self._menu_row:
            self._stage.remote(self._menu_row)
            self._menu_row.destroy()

        row = clutter.Group()
        self._stage.add(row)

        for i in range(len(menu)):
            texture = clutter.Texture(menu[i].image)
            row.add(texture)

            texture.set_depth(self.MENU_INACTIVE_DEPTH)

            texture.connect('button-press-event', self._menu_clicked)
            texture.set_position(i * self.MENU_STEP, 0)

            texture.show()
    
            if i == self._current:
                texture.set_reactive(True);
                texture.set_depth(self.TOP_LAYER_DEPTH)

            menu[i].texture = texture

        row.set_y((self._stage.get_height() - row.get_height()) / 2)

        self._row = row

        self._scroll(0)

        row.show()

        return row

    def main(self):
        clutter.main()

    def set_root_menu(self, menu):
        """
        This is a simplified version of set_menu.
        """
        self._set_menu(menu)
        self._hide_arrow(self._back)

    def set_menu(self, menu, is_forward = True):
        """
        Set the current menu to be displayed.
        is_forward should be false when using a back link and true otherwise.
        """
        
        self._menu.last_index = self._current

        if is_forward:
            menu.parent = self._menu

        self._set_menu(menu)

        if bool(menu.parent):
            self._show_arrow(self._back)
        else:
            self._hide_arrow(self._back)

    def _set_menu(self, menu):
        self._menu = menu
        self._current = menu.last_index

        self._create_menu_row(menu)

    def go_back(self):
        """
        Move to the parent menu or do nothing if there is no parent.
        """
        if self._menu.parent:
            self.set_menu(self._menu.parent, is_forward = False)

    def _scroll(self, direction):
        current = self._current
        following = self._current + direction

        self._menu[current].texture.animate(clutter.EASE_IN_CUBIC, 200, "depth", self.MENU_INACTIVE_DEPTH)
        self._menu[following].texture.animate(clutter.EASE_OUT_CUBIC, 200, "depth", self.MENU_ACTIVE_DEPTH)

        new_x = (self._stage.get_width() / 2 - self._menu[0].texture.get_width() / 2) - self.MENU_STEP * following
        self._row.animate(clutter.EASE_IN_OUT_CUBIC, 1000, "x", new_x)

        self._menu[current].texture.set_reactive(False)
        self._menu[following].texture.set_reactive(True)

        self._current = following

        if following == 0:
            self._hide_arrow(self._left)
        elif not self._left.get_reactive():
            self._show_arrow(self._left)
        
        if following == len(self._menu) - 1:
            self._hide_arrow(self._right)
        elif not self._right.get_reactive():
            self._show_arrow(self._right)

    def _left_clicked(self, arrow, ev):
        self._blink_button(arrow)
        self._scroll(-1)

    def _right_clicked(self, arrow, ev):
        self._blink_button(arrow)
        self._scroll(1)

    def _back_clicked(self, arrow, ev):
        self._blink_button(arrow)
        self.go_back()

    def _menu_clicked(self, item, ev):
        self._blink_button(item)

        menuitem = self._menu[self._current]
        menuitem.action(menuitem, self)

    def _arrow_status(self):
        """
        Show or hide the left and right arrows.
        """
        self._left.disabled = not self._scroller.can_go(ScrollingMenu.LEFT)
        self._right.disabled = not self._scroller.can_go(ScrollingMenu.RIGHT)

    def _hide_arrow(self, arrow):
        arrow.set_reactive(False)
        arrow.animate(clutter.EASE_OUT_CUBIC, 500, "opacity", 0)

    def _show_arrow(self, arrow):
        arrow.animate(clutter.EASE_IN_OUT_CUBIC, 500, "opacity", 255)
        arrow.set_reactive(True)

    def _blink_button(self, button):
        original_depth = button.get_depth()

        def anim_out(animation):
            button.animate(clutter.EASE_OUT_EXPO, 750, "depth", original_depth)

        button.animate(clutter.EASE_IN_EXPO, 10,
            "depth", original_depth - self.BUTTON_PRESS_DEPTH).connect_after("completed", anim_out)

    def set_bg_text(self, line_number, text):
        """
        Set the text to be displayed on the background.
        There are four lines available.
        """
        self._bg_text[line_number].set_text(text)

    def can_go(self, direction):
        """
        Find out if the items selection can move in the given direction.
        """
        current = self.current
        if self.anim:
            current += self.anim_direction

        return (direction == self.LEFT and current >= 1) or \
            (direction == self.RIGHT and current < len(self.items) - 1)

