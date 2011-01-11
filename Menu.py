import os
import math
import pygame
from pygame.locals import *

class Menu:
    FPS = 30
    SCROLL_TIME = 0.5 * FPS
    DISTANCE = 200

    DISABLED_LINE = 420.0 / 600.0

    LEFT = -1
    RIGHT = 1

    def __init__(self, config):
        pygame.display.set_mode((config["width"], config["height"]))#, pygame.FULLSCREEN)
        pygame.display.set_caption(config["caption"])
        self.screen = pygame.display.get_surface()

       	self.background = pygame.image.load(config["background"]).convert()
       	self.left = pygame.image.load(config["left"]).convert_alpha()
       	self.right = pygame.image.load(config["right"]).convert_alpha()
       	self.back = pygame.image.load(config["back"]).convert_alpha()

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(config["font"], config["font size"])
        self.FONT_COLOR = config["font color"]

        self.bgFont = pygame.font.SysFont(config["bg font"], config["bg font size"])
        self.BG_FONT_COLOR = config["bg font color"]
        self.BG_FONT_POS = config["bg font pos"]

        self.ANTIALIAS = config["antialias"]


        self.disabledY = int(self.DISABLED_LINE * self.screen.get_height())

    def set_menu(self, menu):
        self.anim = 0
        self.menu = menu
        self.current = 0

        self.dirty = True

    def update(self):
        if self.anim >= self.SCROLL_TIME:
            self.current += self.animDirection
            self.anim = 0;
        else:
            self.anim += 1

        self.dirty = True

    def scroll_x_func(self, i):
        "Returns the X coordinate of a center of the menu item with index i"
        #screen center
        pos = self.screen.get_width() / 2

        # position of item #i if it was not moving
        pos += (i - self.current) * self.DISTANCE 

        # position of the anim (quadratic function of time)
        t = self.anim / float(self.SCROLL_TIME)
        pos -= int(self.animDirection * self.DISTANCE * (2 * t - t ** 2))

        return pos

    def scroll_y_func(self, i):
        if i == self.current or i == self.current + self.animDirection:
            t = self.anim / float(self.SCROLL_TIME)

            if i == self.current:
                t = 1 - t

            poly = t*t * (-5 + t * (14 + t * -8))

            return int(poly * self.screen.get_height() / 2 + (1 - poly) * self.disabledY)
        else:
            return self.disabledY

    def xy_from_center(self, img, centerx, centery):
        x = centerx - img.get_width() / 2
        y = centery - img.get_height() / 2
        return (x, y)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if len(self.bgText):
            self.draw_bg_text()

        for i in xrange(0, len(self.menu)):
            img = self.menu[i].image
            self.screen.blit(img, \
                self.xy_from_center(img, self.scroll_x_func(i), self.scroll_y_func(i)))

        if self.anim == 0 and len(self.menu) > 0:
            self.draw_text()
	
        if self.can_go(self.LEFT):
            self.screen.blit(self.left, \
                self.xy_from_center(self.left, self.DISTANCE / 2, self.screen.get_height() / 2))
        if self.can_go(self.RIGHT):
            self.screen.blit(self.right, \
                self.xy_from_center(self.right, self.screen.get_width() - self.DISTANCE / 2, self.screen.get_height() / 2))

        if self.backAction:
            self.screen.blit(self.back, \
                self.xy_from_center(self.back, self.DISTANCE / 2, self.DISTANCE / 2))

    def draw_text(self):
        "Draw the text on the current item"
        currentItem = self.menu[self.current]

        try:
            text = currentItem.renderedText
        except AttributeError:
            text = self.font.render(currentItem.text, self.ANTIALIAS, self.FONT_COLOR)
            currentItem.renderedText = text

        x = self.scroll_x_func(self.current) + currentItem.image.get_width() / 2 - text.get_width();
        y = self.scroll_y_func(self.current) - currentItem.image.get_height() / 2 - self.font.get_ascent();

        self.screen.blit(text, (x, y))

    def draw_bg_text(self):
        """
        Actually draw the background text.
        """
        (offset, y) = self.BG_FONT_POS
        for line in self.bgText:
            x = self.screen.get_width() - offset - line.get_width();
            self.screen.blit(line, (x, y))
            y += self.bgFont.get_linesize()

    def can_go(self, direction):
        "Returns true if we can move in the given direction with the menu"
        current = self.current
        if self.anim:
            current += self.animDirection

        return (direction == self.LEFT and current >= 1) or \
            (direction == self.RIGHT and current < len(self.menu) - 1)

    def start_anim(self, direction):
        if not self.can_go(direction):
            return

        if self.anim:
            self.current += self.animDirection
        
        self.anim = 1
        self.animDirection = direction

    def work(self):
        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return 0
            elif event.type == MOUSEBUTTONDOWN:
                self.process_click(event.pos)

        if self.anim:
            self.update()

        if self.dirty:
            self.draw()
            pygame.display.flip()

        return 1

    def process_click(self, pos):
        (x, y) = pos
        x = x // (self.screen.get_width() / 3)
        y = y // (self.screen.get_height() / 3)

        if x == 0 and y == 0 and self.backAction:
            backAction()
        elif y == 1:
            if x == 0:
                self.start_anim(self.LEFT)
            if x == 1:
                self.menu[self.current].action()
            if x == 2:
                self.start_anim(self.RIGHT)

    def set_bg_text(self, text):
        """
        Set the text to be displayed on the background.
        The parameter text should be an iterable with lines to display
        """
        
        self.bgText = map(lambda str: self.bgFont.render(str, self.ANTIALIAS, self.BG_FONT_COLOR), text)

        self.dirty = True

    dirty = False

    anim = 0
    animDirection = LEFT

    backAction = 0
    bgText = ()
