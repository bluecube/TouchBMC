class Animation(object):
    """
    An object that can be animated.
    important fields: disabled, rect, anim_length, anim, repeat, running, dirty
    If the dirty flag is true, then we need update even though the animation is
    not running
    """

    def __init__(self):
        self.disabled = False
        self.anim = 0
        self.repeat = False
        self.running = True
        self.dirty = False

    def draw(self, surface):
        """
        Draw the animation to the surface.
        Default implementation uses the fields self.image and self.rect
        """
        pass

    def update(self):
        """
        Update the animation, returns True if we need more ticks,
        False if the anim is finished.
        The default animation steps through an animation couter
        self.anim, based on the other fields ... use the code, Luke.
        You must set self.anim_length before calling this method!
        """
        dirty = self.dirty
        self.dirty = False

        if not self.running:
            return dirty

        self.anim += 1

        if self.anim >= self.anim_length:
            self.anim = 0
            self.running = self.repeat
        
        return self.running or dirty
        
class StillImage(Animation):
    """
    Convinience class for drawing still images within animation.
    Has the same functionality as pygame Sprite ...
    important fields: disabled, image, rect
    """

    def __init__(self):
        Animation.__init__(self)

    def draw(self, surface):
        """
        Draw the image according to self.image and self.rect
        """
        surface.blit(self.image, self.rect.topleft)

    def update(self):
        """
        Still images don't need updating.
        """
        return False

class AnimationManager(Animation):
    """
    A group of animations.
    This is not as fancy as pygame.Group, only adding is supported
    """

    def __init__(self):
        Animation.__init__(self)
        self._animations = []

    def __iter__(self):
        return iter(self._animations)

    def add(self, anim):
        self._animations.append(anim)
        
    def update(self):
        """
        Update all enabled animations added to this manager,
        return if a timer ticks are necessary for anyone.
        """
        need_ticks = False

        for anim in self:
            if anim.disabled:
                continue
            need_ticks = need_ticks or anim.update()

        return need_ticks

    def draw(self, surface):
        """
        Draw all of the enabled animations.
        """
        for anim in self:
            if anim.disabled:
                continue
            anim.draw(surface)
