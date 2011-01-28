import pygame.event
from pygame.locals import *

class State(object):
    """
    Base class for gui states.
    """
    @classmethod
    def handle_event(cls, gui, ev):
        """
        This method handles event that occured on the gui
        and returns a new state.
        """
        raise NotImplementedError()

    @classmethod
    def enter(cls, gui):
        """
        Do the action on entering the state
        and set the state in gui
        """
        oldState = None
        try:
            oldState = gui._state;
        except AttributeError:
            pass
            
        if oldState:
            oldState.exit(gui)

        gui._state = cls

    @classmethod
    def exit(cls, gui):
        pass

class DimmedState(State):
    """
    Foreground is hidden.
    """
    @classmethod
    def enter(cls, gui):
        super(DimmedState, cls).enter(gui)
        gui._foreground_manager.disabled = True

    @classmethod
    def exit(cls, gui):
        gui._foreground_manager.disabled = False

    @classmethod
    def handle_event(cls, gui, ev):
        if ev.type == MOUSEBUTTONUP:
            IdleState.enter(gui)

class IdleState(State):
    """
    Waiting for user input.
    """
    @classmethod
    def enter(cls, gui):
        super(IdleState, cls).enter(gui)
        gui._dim_counter = 0

    @classmethod
    def handle_event(cls, gui, ev):
        if ev.type == MOUSEBUTTONDOWN:
            x, y = ev.pos
            if y > gui._config["drag area"]:
                DraggingState.enter(gui)
                DraggingState._dragging(gui, ev)
        elif ev.type == MOUSEBUTTONUP:
            gui._dim_counter = 0
            x, y = ev.pos

            # we only have nine sensitive areas
            x = x // (gui._screen.get_width() / 3)
            y = y // (gui._screen.get_height() / 3)

            if x == 0 and y == 0:
                gui.go_back()
            elif y == 1:
                if x == 0:
                    gui.scroll_left()
                elif x == 1:
                    gui.action()
                elif x == 2:
                    gui.scroll_right()

        elif ev.type == USEREVENT:
            gui._dim_counter += 1
            if gui._dim_counter > gui._config["hide fg counter top"]:
                DimmedState.enter(gui)


class DraggingState(State):
    """
    Dragging in the bottom row.
    """
    @classmethod
    def enter(cls, gui):
        super(DraggingState, cls).enter(gui)
        gui._scroller._set_dont_scroll(True)

    @classmethod
    def exit(cls, gui):
        gui._scroller._set_dont_scroll(False)
        gui._scroller.update()

    @classmethod
    def handle_event(cls, gui, ev):
        if ev.type == MOUSEMOTION:
            cls._dragging(gui, ev)
        elif ev.type == MOUSEBUTTONUP:
            IdleState.enter(gui)

    @classmethod
    def _dragging(cls, gui, ev):
        (x, y) = ev.pos
        item_count = len(gui._scroller._items)
        fractional = ((item_count * (x - gui._config["drag offset"])) /
            float(gui._screen.get_width() - 2 * gui._config["drag offset"]))

        fractional = max(0.5, min(fractional, item_count - 0.5))
        
        gui._scroller._current = int(fractional)
        fractional -= 0.5
        
        gui._arrow_status()
        gui._scroller.scroll(int(fractional), fractional - int(fractional))
        gui._manager.draw(gui._screen)
    
