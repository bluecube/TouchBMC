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

        self.bg_font = pygame.font.SysFont(config["bg font"], config["bg font size"])
        self.BG_FONT_COLOR = config["bg font color"]
        self.BG_FONT_POS = config["bg font pos"]

        self.ANTIALIAS = config["antialias"]


        self.disabled_y = int(self.DISABLED_LINE * self.screen.get_height())

    def set_menu(self, menu):
        """
        Set the current menu (array of MenuItem)
        """
        self.anim = 0
        self.menu = menu
        self.current = 0

        self.dirty = True

    def set_bg_text(self, text):
        """
        Set the text to be displayed on the background.
        The parameter text should be an iterable with lines to display
        """
        
        self.bg_text = map(lambda str: self.bg_font.render(str, self.ANTIALIAS, self.BG_FONT_COLOR), text)

        self.dirty = True

    def set_back_link(self, action):
        """
        Set the action for the back link.
        If action is false then no backwards link will be displayed.
        """
        back_action = action

    def update(self):
        """
        Step the animation, if applicable.
        """
        if self.anim == 0:
            return

        if self.anim >= self.SCROLL_TIME:
            self.current += self.anim_direction
            self.anim = 0;
        else:
            self.anim += 1

        self.dirty = True

    def xy_from_center(self, img, centerx, centery):
        """
        Calculate coordinates of the top left corner from the center coords.
        """
        x = centerx - img.get_width() / 2
        y = centery - img.get_height() / 2
        return (x, y)

    def draw(self):
        """
        Redraw the whole screen, clear the dirty flag.
        """
        self.screen.blit(self.background, (0, 0))

        if len(self.bg_text):
            self.draw_bg_text()

        for i in xrange(0, len(self.menu)):
            self.draw_item(i)

        if self.can_go(self.LEFT):
            self.screen.blit(self.left, \
                self.xy_from_center(self.left, self.DISTANCE / 2, self.screen.get_height() / 2))
        if self.can_go(self.RIGHT):
            self.screen.blit(self.right, \
                self.xy_from_center(self.right, self.screen.get_width() - self.DISTANCE / 2, self.screen.get_height() / 2))

        if self.back_action:
            self.screen.blit(self.back, \
                self.xy_from_center(self.back, self.DISTANCE / 2, self.DISTANCE / 2))

    def draw_item(self, i):
        """
        Draw a single menu item to its correct position.
        """
        x = self.screen.get_width() / 2

        # position of item #i if it was not moving
        x += (i - self.current) * self.DISTANCE 

        if self.anim:    
            # animation time (from 0 to 1)
            t = self.anim / float(self.SCROLL_TIME)

            # position of the anim (quadratic function of time)
            x -= int(self.anim_direction * self.DISTANCE * (2 * t - t ** 2))

            if i == self.current or i == self.current + self.anim_direction:
                if i == self.current:
                    t = 1 - t

                poly = t*t * (-5 + t * (14 + t * -8))

                y = int(poly * self.screen.get_height() / 2 + (1 - poly) * self.disabled_y)
            else:
                y = self.disabled_y
        else:
            if i == self.current:
                y = self.screen.get_height() / 2
            else:
                y = self.disabled_y

        
        item = self.menu[i]
        img = item.image

        self.screen.blit(img, self.xy_from_center(img, x, y))

	if self.anim or i != self.current:
		return
	
	#draw the text

        try:
            text = item.rendered_text
        except AttributeError:
            text = self.font.render(item.text, self.ANTIALIAS, self.FONT_COLOR)
            item.rendered_text = text

        x += img.get_width() / 2 - text.get_width();
        y -= img.get_height() / 2 + self.font.get_ascent();

        self.screen.blit(text, (x, y))

    def draw_bg_text(self):
        """
        Actually draw the background text.
        """
        (offset, y) = self.BG_FONT_POS
        for line in self.bg_text:
            x = self.screen.get_width() - offset - line.get_width();
            self.screen.blit(line, (x, y))
            y += self.bg_font.get_linesize()

    def can_go(self, direction):
    	"""
	Find out if the menu selection can move in the given direction.
	"""
        current = self.current
        if self.anim:
            current += self.anim_direction

        return (direction == self.LEFT and current >= 1) or \
            (direction == self.RIGHT and current < len(self.menu) - 1)

    def start_anim(self, direction):
    	"""
	Start animation in the given direction, restart an animation if it was already running.
	"""
        if not self.can_go(direction):
            return

        if self.anim:
            self.current += self.anim_direction
        
        self.anim = 1
        self.anim_direction = direction

    def work(self):
    	"""
	Process a single frame
	"""
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
    	"""
	Do the correct thing when a click is detected
	"""

	# we only have nine sensitive areas
        (x, y) = pos
        x = x // (self.screen.get_width() / 3)
        y = y // (self.screen.get_height() / 3)

        if x == 0 and y == 0 and self.back_action:
            back_action()
        elif y == 1:
            if x == 0:
                self.start_anim(self.LEFT)
            if x == 1:
                self.menu[self.current].action()
            if x == 2:
                self.start_anim(self.RIGHT)

    dirty = False

    anim = 0
    anim_direction = LEFT

    back_action = 0
    bg_text = ()
