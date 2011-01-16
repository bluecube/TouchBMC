import sys
import math
import pygame
from pygame.locals import *
import math

from menu import Menu

class Gui:

    BG_TEXT_ANIM_SPEED = 1

    DISABLED_LINE = 420.0 / 600.0

    LEFT = -1
    RIGHT = 1

    def __init__(self, config, cache):
        # only initialize what we really need
        pygame.display.init()
        pygame.font.init()

        pygame.display.set_mode((config["width"], config["height"]), pygame.NOFRAME)# pygame.FULLSCREEN)
        pygame.display.set_caption(config["caption"])
        self.screen = pygame.display.get_surface()

        pygame.event.set_allowed([QUIT, MOUSEBUTTONUP, USEREVENT])

        self.background = pygame.image.load(config["background"]).convert()

        x_6 = self.screen.get_width() / 6
        y_6 = self.screen.get_height() / 6

        self.left = self.load_sprite(config["left"],   1 * x_6, 3 * y_6, cache)
        self.right = self.load_sprite(config["right"], 5 * x_6, 3 * y_6, cache)
        self.back = self.load_sprite(config["back"],   1 * x_6, 1 * y_6, cache)

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT, 5000)

        self.font = pygame.font.SysFont(config["font"], config["font size"])
        self.FONT_COLOR = config["font color"]

        self.bg_font = pygame.font.SysFont(config["bg font"], config["bg font size"])
        self.BG_FONT_COLOR = config["bg font color"]
        self.BG_FONT_POS = config["bg font pos"]

        self.ANTIALIAS = config["antialias"]
        self.FPS = config["fps"]
        self.ANIM_LENGTH = int(config["menu scroll time"] * self.FPS)
        self.HIDE_FG_COUNTER_TOP = config["hide fg counter top"]
        self.DISTANCE = config["item distance"]
        self.DRAG_OFFSET = config["drag offset"]
        self.DRAG_INIT_LENGTH = config["drag init length"]

        self.disabled_y = int(self.DISABLED_LINE * self.screen.get_height())

        self.hide_fg = True
        self.hide_fg_counter = 0
        self.current = 0
        self.mousedown_pos = None
        self.dragging = False

    def load_sprite(self, path, x, y, cache):
        """
        Constructs a new sprite, loads it with an image and sets its rect
        to have a center point at (x, y).
        """
        sprite = pygame.sprite.Sprite()
        sprite.image = cache.open(path)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = (x, y)

        return sprite

    def set_menu(self, menu, current = -1, is_forward = True):
        """
        Set the current menu to be displayed.
        current is the index of item that will be selected in the loaded menu.
        is_forward should be false when using a back link and true otherwise.
        """

        try:
            self.items.last_index = self.current

            if is_forward:
                menu.parent = self.items
        except AttributeError:
            pass

        self.anim = 0
        self.items = menu
        if current >= 0:
            self.current = current
        else:
            self.current = menu.last_index

        if menu.parent:
            def action(gui):
                gui.set_menu(menu.parent, is_forward = False)

            self.back_action = action
        else:
            self.back_action = None

        self.update()

    def set_bg_text(self, line_number, text):
        """
        Set the text to be displayed on the background.
        The parameter text should be an iterable with lines to display
        If the first line is too long, starts the line scrolling anim.
        """
        
        try:
            if self.bg_text[line_number].text == text:
                return
        except IndexError:
            pass

        (x_offset, y) = self.BG_FONT_POS

        y += line_number * self.bg_font.get_ascent()

        for i in range(len(self.bg_text), line_number + 1):
            self.bg_text.append(NoText())

        if text == "":
            self.bg_text[line_number] = NoText()
        else:
            self.bg_text[line_number] = ScrollingText(text, self.bg_font,
                self.screen, x_offset, y,
                self.ANTIALIAS, self.BG_FONT_COLOR,
                self.BG_TEXT_ANIM_SPEED)

    def update(self):
        """
        Step the animation, if applicable.
        """
        if self.anim >= self.ANIM_LENGTH:
            self.stop_anim()
        elif self.anim:
            self.anim += 1

        t = self.anim / float(self.ANIM_LENGTH)

        x = self.screen.get_width() / 2
        x -= self.current * self.DISTANCE
        x -= int(self.anim_direction * self.DISTANCE * (2 * t - t ** 2))

        for i in xrange(len(self.items)):
            if i == self.current or i == self.current + self.anim_direction:
                new_t = t
                if i == self.current:
                    new_t = 1 - t

                poly = new_t * new_t * (-5 + new_t * (14 + new_t * -8))

                y = int(poly * self.screen.get_height() / 2 + (1 - poly) * self.disabled_y)
            else:
                y = self.disabled_y

            item = self.items[i]
            item.rect.center = (x, y)

            x += self.DISTANCE

        for line in self.bg_text:
            line.update()

    def xy_from_center(self, img, centerx, centery):
        """
        Calculate coordinates of the top left corner from the center coords.
        """
        x = centerx - img.get_width() / 2
        y = centery - img.get_height() / 2
        return (x, y)

    def draw(self):
        """
        Redraw the whole screen.
        """
        
        self.screen.blit(self.background, (0, 0))

        self.draw_bg_text()

        if self.hide_fg:
            return

        self.draw_items()

        if self.can_go(self.LEFT):
            self.draw_sprite(self.left)

        if self.can_go(self.RIGHT):
            self.draw_sprite(self.right)

        if self.back_action:
            self.draw_sprite(self.back)

    def draw_items(self):
        """
        Draw menu items and its description text.
        """

        if not len(self.items):
            return

        for i in xrange(len(self.items)):
            item = self.items[i]
            self.draw_sprite(item)

        if self.anim:
            return
        
        #draw the text

        item = self.items[self.current]

        if len(item.text) == 0:
            return

        try:
            text = item.rendered_text
        except AttributeError:
            text = self.font.render(item.text, self.ANTIALIAS, self.FONT_COLOR)
            item.rendered_text = text

        (x, y) = item.rect.midtop

        x -= text.get_width() / 2;
        y -= self.font.get_ascent();

        self.screen.blit(text, (x, y))

    def draw_sprite(self, sprite):
        """
        Draws a sprite to the position given by its rect
        """
        self.screen.blit(sprite.image, sprite.rect.topleft)

    def draw_bg_text(self):
        """
        Actually draw the background text.
        """
        for line in self.bg_text:
            line.draw(self.screen)

    def can_go(self, direction):
        """
        Find out if the items selection can move in the given direction.
        """
        current = self.current
        if self.anim:
            current += self.anim_direction

        return (direction == self.LEFT and current >= 1) or \
            (direction == self.RIGHT and current < len(self.items) - 1)


    def start_anim(self, direction):
        """
        Start animation in the given direction, restart an animation if it was already running.
        """
        if not self.can_go(direction):
            return

        self.stop_anim()
        
        self.anim = 1
        self.anim_direction = direction

    def stop_anim(self):
        """
        Immediately stop the animation (skip the rest of it).
        """
        if not self.anim:
            return

        self.current += self.anim_direction
        self.anim = 0

    def work(self):
        """
        Process a single frame. Note that this might block.
        """
        self.clock.tick(self.FPS)

        self.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            self.process_event(event)

        if self.need_ticks():
            self.update()
        else:
            event = pygame.event.wait();
            self.process_event(event);

    def need_ticks(self):
        if self.anim:
            return True

        for line in self.bg_text:
            if line.anim:
                return True

        return False 

    def process_event(self, event):
        """
        Process a single event
        """
        # Don't forget to modify the allowed list in the constructor
        # when adding new events here!

        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            self.process_mousedown(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.process_mouseup(event.pos)
        elif event.type == MOUSEMOTION:
            self.process_mousemotion(event.pos)
        elif event.type == USEREVENT:
            self.process_hide_fg()

    def process_mousedown(self, pos):
        """
        Starts dragging
        """

        if self.hide_fg:
            return

        self.mousedown_pos = pos
        self.dragging = False

    def process_mousemotion(self, pos):
        """
        Handle drawing.
        """

        if not self.mousedown_pos:
            return

        self.hide_fg_counter = 0

        if not self.dragging:
            if self.drag_length(pos) > self.DRAG_INIT_LENGTH:
                self.dragging = True
        
        (x, y) = pos
        i = ((len(self.items) * (x - self.DRAG_OFFSET)) //
            (self.screen.get_width() - 2 * self.DRAG_OFFSET))

        if i < 0:
            i = 0
        elif i >= len(self.items):
            i = len(self.items) - 1

        if i == self.current:
            return;
        else:
            if i > self.current:
                direction = self.RIGHT
            else:
                direction = self.LEFT

            i -= direction
            if self.current != i or not self.anim:
                self.current = i - direction
                self.start_anim(direction)

    def drag_length(self, pos):
        x1, y1 = self.mousedown_pos
        x2, y2 = pos

        x = x1 - x2
        y = y1 - y2

        return math.sqrt(x * x + y * y)

    def process_mouseup(self, pos):
        """
        Do the correct thing when a click is detected
        """

        self.hide_fg_counter = 0

        was_dragging = self.dragging
        self.dragging = False
        self.mousedown_pos = None
        if was_dragging:
            return

        if self.hide_fg:
            self.hide_fg = False
            self.draw()
            return

        # we only have nine sensitive areas
        (x, y) = pos
        x = x // (self.screen.get_width() / 3)
        y = y // (self.screen.get_height() / 3)

        if x == 0 and y == 0 and callable(self.back_action):
            self.back_action(self)
        elif y == 1:
            if x == 0:
                self.start_anim(self.LEFT)
            if x == 1:
                self.stop_anim()

                item = self.items[self.current]
                if callable(item.action):
                    item.action(self)
                else:
                    print "Invalid action on item!"
            if x == 2:
                self.start_anim(self.RIGHT)

    def process_hide_fg(self):
        if self.hide_fg:
            return

        self.hide_fg_counter += 1
        if self.hide_fg_counter > self.HIDE_FG_COUNTER_TOP:
            self.hide_fg = True
            self.draw()

    anim = 0
    anim_direction = LEFT

    back_action = 0
    bg_text = []
    

class ScrollingText():
    """
    One line of text that is possibly scrolling.
    """

    def __init__(self, text, font, screen, x_offset, y, antialias, color, anim_speed):
        """
        text: string to render
        font: font object
        screen: screen to draw to
        x_offset: offset from the right corner of the screen
        y: y coordinate of the screen
        anim_speed: how many pixels per frame to move
        """

        self.rendered = font.render(text, antialias, color)
        self.text = text;

        self.anim_speed = anim_speed

        effective_width = screen.get_width() - 2 * x_offset

        self.anim = (effective_width < self.rendered.get_width())

        self.anim_state = 0

        (space_width, x) = font.size(" ")
        self.anim_len = self.rendered.get_width() + space_width

        if self.anim:
            self.rect = Rect(0, y, screen.get_width(), self.rendered.get_height())
        else:
            x = screen.get_width() - self.rendered.get_width() - x_offset
            self.rect = Rect(x, y, self.rendered.get_width(), self.rendered.get_height())

    def draw(self, screen):
        """
        Draw the text to the given screen
        """

        if self.anim:
            screen.blit(self.rendered, (-self.anim_state, self.rect.top))
            screen.blit(self.rendered, (self.anim_len - self.anim_state, self.rect.top))
        else:
            screen.blit(self.rendered, self.rect.topleft)

    def update(self):
        self.anim_state += self.anim_speed

        if(self.anim_state >= self.anim_len):
            self.anim_state -= self.anim_len

class NoText:
    anim = False
    text = ""

    def update(self):
        pass

    def draw(self, screen):
        pass
