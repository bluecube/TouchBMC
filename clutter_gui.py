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

        x_6 = self._stage.get_width() // 6
        y_6 = self._stage.get_height() // 6

        self._left = self._add_arrow("left", x_6, 3 * y_6, self._left_clicked)
        self._right = self._add_arrow("right", 5 * x_6, 3 * y_6, self._right_clicked)
        self._back = self._add_arrow("back", x_6, y_6, self._back_clicked)

        self._row = self._create_menu_row()

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

    def _create_menu_row(self):
        row = clutter.Group()
        self._stage.add(row)

        row.show()

        return row

    def main(self):
        clutter.main()

    def set_root_menu(self, menu):
        """
        This is a simplified version of set_menu.
        """
        self._set_menu(menu)
        self._hide_button(self._back)

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
            self._show_button(self._back)
        else:
            self._hide_button(self._back)

    def _set_menu(self, menu):
        self._menu = menu
        self._current = menu.last_index

        self._row.remove_all()

        for i in range(len(menu)):
            texture = clutter.Texture(menu[i].image)
            self._row.add(texture)

            texture.set_depth(self.MENU_INACTIVE_DEPTH)

            texture.connect('button-press-event', self._menu_clicked)
            texture.set_position(i * self.MENU_STEP, 0)

            texture.show()
    
            if i == self._current:
                texture.set_reactive(True);
                texture.set_depth(self.TOP_LAYER_DEPTH)

            menu[i].texture = texture

        self._row.set_position(
            self._row_x_coord(),
            (self._stage.get_height() - self._row.get_height()) / 2)

        self._arrow_visibility()

    def go_back(self):
        """
        Move to the parent menu or do nothing if there is no parent.
        """
        if self._menu.parent:
            self.set_menu(self._menu.parent, is_forward = False)

    def _row_x_coord(self ):
        return (self._stage.get_width() / 2 - self._menu[0].texture.get_width() / 2) - self.MENU_STEP * self._current

    def _scroll(self, direction):
        current = self._current
        following = self._current + direction

        self._current = following

        self._menu[current].texture.set_reactive(False)

        def after_animation(anim):
            self._menu[following].texture.set_reactive(True)

        self._menu[current].texture.animate(clutter.EASE_IN_CUBIC, 200,
            "depth", self.MENU_INACTIVE_DEPTH)
        self._menu[following].texture.animate(clutter.EASE_OUT_CUBIC, 200,
            "depth", self.MENU_ACTIVE_DEPTH)

        self._row.detach_animation()
        self._row.animate(clutter.EASE_IN_OUT_CUBIC, 1000,
            "x", self._row_x_coord()).connect_after("completed", after_animation)


        self._arrow_visibility()

    def _arrow_visibility(self):
        if self._current == 0:
            self._hide_button(self._left)
        elif not self._left.get_reactive():
            self._show_button(self._left)
        
        if self._current == len(self._menu) - 1:
            self._hide_button(self._right)
        elif not self._right.get_reactive():
            self._show_button(self._right)

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

    def _hide_button(self, arrow):
        arrow.set_reactive(False)
        arrow.animate(clutter.EASE_IN_OUT_CUBIC, 500, "opacity", 0)

    def _show_button(self, arrow):
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
        pass
