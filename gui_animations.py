import pygame
import math
from pygame.locals import *
from animation import *

class ScrollingText(Animation):
    """
    One line of text that is possibly scrolling.
    """

    def __init__(self, config, screen, row, font):
        Animation.__init__(self)
        self.repeat = True

        self._config = config
        self._screen = screen
        self._font = font

        self._x, self._y = config["bg font pos"]
        self._y += row * font.get_ascent()
    
        self.disabled = True
        self._text = ""

        self._space, dummy = font.size(" ")
        
    def set_text(self, text):
        """
        Set the text to display.
        This disables the animation if text is empty, otherwise
        renders the text and modifies self.rect.
        """
        if text == "":
            self.disabled = True
            self.rendered = None
            return
        
        if self._text == text:
            return

        self.text = text;

        self.disabled = False

        self.rendered = self._font.render(text, self._config["antialias"],
            self._config["bg font color"])
        self.rendered.fill((255, 255, 255, self._config["bg font alpha"]),
            special_flags = BLEND_RGBA_MULT)


        effective_width = self._screen.get_width() - 2 * self._x

        self.running = (effective_width < self.rendered.get_width())
        self.anim = 0

        self.anim_len = self.rendered.get_width() + self._space

        if self.running:
            self.rect = Rect(0, self._y, screen.get_width(), self.rendered.get_height())
        else:
            x = self._screen.get_width() - self.rendered.get_width() - self._x
            self.rect = Rect(x, self._y, self.rendered.get_width(), self.rendered.get_height())

        self.dirty = True

    def draw(self, screen):
        """
        Draw the text to the given screen
        """

        #TODO: Modify the scrolling speed
        if self.anim:
            screen.blit(self.rendered, (-self.anim_state, self.rect.top))
            screen.blit(self.rendered, (self.anim_len - self.anim_state, self.rect.top))
        else:
            screen.blit(self.rendered, self.rect.topleft)

class Image(StillImage):
    """
    A simple image from a file.
    """
    def __init__(self, path, x, y, cache, topleft_pos = False):
        """
        Constructs a new (not moving) animation,
        loads it with an image and sets its rect
        to have a center point at (x, y).
        """
        StillImage.__init__(self)

        self.image = cache.open(path)
        self.rect = self.image.get_rect()
        if topleft_pos:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (x, y)

class PositionBar(StillImage):
    """
    The bar at the bottom that shows the positions for dragging.
    Regenerates its content from a given menu, but rect stays always the same.
    """
    def __init__(self, config, screen):
        StillImage.__init__(self)
        self.rect = pygame.rect.Rect(
            config["drag offset"],
            config["drag area"],
            screen.get_width() - 2 * config["drag offset"],
            screen.get_height() - config["drag area"])
        self._config = config

    def set_menu(self, menu):
        """
        Generate the little pictures.
        """
        self.image = pygame.Surface(self.rect.size, SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        step = int(math.ceil(len(menu) / float(self._config["a lot of items"])))

        displayed_indices = xrange(0, len(menu), step)

        bin_width = self.rect.width / float(len(displayed_indices))

        allowed_width = int(0.9 * bin_width)
        allowed_height = int(self.rect.height)

        x = bin_width / 2
        for i in displayed_indices:
            img = self._resize(menu[i].image, allowed_width, allowed_height)

            self.image.blit(img,
                (x - img.get_width() / 2,
                (self.image.get_height() - img.get_height()) / 2))

            x += bin_width

        self.image.fill((255, 255, 255, self._config["bar alpha"]),
            special_flags = BLEND_RGBA_MULT)

        self.dirty = True

    def _resize(self, img, allowed_width, allowed_height):
        if img.get_width() < allowed_width and img.get_height < allowed_height:
            return img

        aspect = img.get_width() / float(img.get_height())
        allowed_aspect = allowed_width / float(allowed_height)

        if aspect > allowed_aspect:
            width = allowed_width
            height = int(allowed_width / aspect)
        else:
            width = int(allowed_height * aspect)
            height = allowed_height

        return pygame.transform.smoothscale(img, (width, height))
        

class ScrollingMenu(Animation):
    LEFT = -1
    RIGHT = 1

    def __init__(self, config, screen):
        Animation.__init__(self)
        self._config = config
        self.repeat = False
        self.anim_length = int(config["menu scroll time"] * config["fps"])
        self._screen = screen
        self.running = False
        self.font = pygame.font.SysFont(config["font"], config["font size"])

        self.disabled_y = 400 # TODO: This shouldn't be here

        self._dont_scroll = False

    def set_menu(self, menu):
        self._items = menu
        self._current = menu.last_index
        self.update()

    def stop(self):
        """
        Immediately stop the animation.
        """
        self.running = False
        self.anim = 0

    def start(self, direction):
        """
        Start animating in the given direction, possibly
        interrupting another animation.
        Returns False if there are no more items in the given direction
        (and the scroll was aborted), True otherwise.
        """
        if not self.can_go(direction):
            return False

        self.anim = 0
        self._current += direction
        self._direction = direction
        self.running = True

        return True

    def can_go(self, direction):
        """
        Returns False if there are no more items in the given direction,
        True otherwise.
        """
        return ((direction == ScrollingMenu.LEFT and self._current > 0) or
            direction == ScrollingMenu.RIGHT and self._current < (len(self._items) - 1))

    def update(self):
        if self._dont_scroll:
            assert not self.running
            return False

        need_ticks = Animation.update(self)

        if not self.running:
            self.scroll(self._current, 0)
            return need_ticks

        t = self.anim / float(self.anim_length)

        t = (2 * t - t ** 2) # scroll dynamics

        if self._direction >= 0:
            self.scroll(self._current - 1, t)
        else:
            self.scroll(self._current, 1 - t)

        return need_ticks

    def _set_dont_scroll(self, state):
        """
        Disables calling the scroll method during update.
        Used to avoid destroying the calculated posuitoon when dragging.
        Trying to animate while this is set is an error.
        """
        self._dont_scroll = state

    def scroll(self, current, t):
        """
        Update positions of the items.
        This part doesn't contain the dynamics
        """

        x = self._screen.get_width() / 2
        x -= current * self._config["item distance"]
        x -= int(self._config["item distance"] * t)

        for i in xrange(len(self._items)):
            self._items[i].rect.center = (x, self.disabled_y)
            x += self._config["item distance"]

        if t > 0 and t < 1:
            poly = t * t * (-5 + t * (14 + t * -8))
            y = int(poly * self._screen.get_height() / 2 + (1 - poly) * self.disabled_y)
            self._items[current+1].rect.centery = y

            t = 1 - t
            poly = t * t * (-5 + t * (14 + t * -8))
            y = int(poly * self._screen.get_height() / 2 + (1 - poly) * self.disabled_y)
            self._items[current].rect.centery = y
        else:
            self._items[current + int(t)].rect.centery = self._screen.get_height() / 2

    def draw(self, screen):
        if not len(self._items):
            return

        for i in xrange(len(self._items)):
            item = self._items[i]
            screen.blit(item.image, item.rect.topleft)

        if self.running:
            return
        
        #draw the text

        item = self._items[self._current]

        if len(item.text) == 0:
            return

        try:
            text = item.rendered_text
        except AttributeError:
            text = self.font.render(item.text, self._config["antialias"], self._config["font color"])
            item.rendered_text = text

        (x, y) = item.rect.midtop

        x -= text.get_width() / 2;
        y -= self.font.get_ascent();

        screen.blit(text, (x, y))

