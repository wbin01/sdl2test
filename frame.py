#!/usr/bin/env python3
import sys
import ctypes

import sdl2
import sdl2.ext


class Frame(object):
    """..."""
    def __init__(
            self, width: int = 400, height: int = 300, text: str = '',
            csd: bool = True, csd_move: bool = True, csd_resize: bool = True, csd_edge: int = 8
            ) -> None:
        """
        :param width:
        :param height:
        :param text:
        :param csd:
        :param csd_move:
        :param csd_resize:
        :param csd_edge:
        """
        # Args
        self.__width = width
        self.__height = height
        self.__text = text
        self.__csd = csd
        self.__csd_move = csd_move
        self.__csd_resize = csd_resize
        self.__csd_edge = csd_edge

        # Window
        sdl2.ext.init()
        sdl2.SDL_SetHint(sdl2.SDL_HINT_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR, b'1')
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_RED_SIZE, 8)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_GREEN_SIZE, 8)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_BLUE_SIZE, 8)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_ALPHA_SIZE, 8)

        self.__win = sdl2.ext.Window(
            self.__text,
            size=(self.__width, self.__height),
            flags=sdl2.SDL_WINDOW_BORDERLESS if self.__csd else None)
        
        self.__renderer = sdl2.SDL_CreateRenderer(
            self.__win.window, -1, sdl2.SDL_RENDERER_ACCELERATED)
        
        # Cursor
        self.__cursor_arrow = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_ARROW)
        self.__cursor_lr = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_SIZEWE)
        self.__cursor_tb = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_SIZENS)
        self.__cursor_tlbr = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_SIZENWSE)
        self.__cursor_trbl = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_SIZENESW)
        self.__cursor_drag = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_HAND)
        self.__cursor = self.__cursor_arrow
        
        # Control - Window
        self.__win_x = ctypes.c_int()
        self.__win_y = ctypes.c_int()
        self.__win_start_x = ctypes.c_int()
        self.__win_start_y = ctypes.c_int()

        # Control - Window move resize
        self.__start_w = ctypes.c_int()
        self.__start_h = ctypes.c_int()
        self.__mouse_action = None # None | 'drag' | 'resize'
        self.__cursor_edge = None
        self.__resizig = False
        self.__saved_edge_name = None

        # Control - Mouse
        self.__mouse_global_x = ctypes.c_int()
        self.__mouse_global_y = ctypes.c_int()
        self.__mouse_start_x = ctypes.c_int()
        self.__mouse_start_y = ctypes.c_int()
    
    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'width={self.__width!r}, '
            f'height={self.__height!r}, '
            f'text={self.__text!r}, '
            f'csd={self.__csd!r}, '
            f'csd_move={self.__csd_move!r}, '
            f'csd_resize={self.__csd_resize!r}, '
            f'csd_edge={self.__csd_edge!r}'
            ')')
    
    def __str__(self) -> str:
        return self.__class__.__name__

    def run(self) -> int:
        """..."""
        self.__win.show()

        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                self.__cursor_edge = self.__detect_edge(event)
                self.__set_cursor(self.__cursor_edge)

                if event.type == sdl2.SDL_QUIT:
                    running = False

                # Press
                elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    if event.button.button == sdl2.SDL_BUTTON_LEFT:
                        if self.__csd: self.__update_move_resize_controls(event)
                
                # Move
                elif event.type == sdl2.SDL_MOUSEMOTION and self.__mouse_action:
                    if self.__csd: self.__move_or_resize_window(event)
                
                # Release
                elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                    self.__mouse_action = None
                    self.__saved_edge_name = None
                    self.__resizig = False
                    
                    # sdl2.SDL_FreeCursor(self.__cursor)
                    sdl2.SDL_SetCursor(self.__cursor_arrow)

            sdl2.SDL_RenderPresent(self.__renderer)  # self.__win.refresh()
        return 0
    
    def __set_cursor(self, cursor_name: str) -> None:
        # sdl2.SDL_FreeCursor(self.__cursor)

        if self.__resizig:
            return
        
        if cursor_name == 'topleft':
            sdl2.SDL_SetCursor(self.__cursor_tlbr)
        elif cursor_name == 'topright':
            sdl2.SDL_SetCursor(self.__cursor_trbl)
        elif cursor_name == 'bottomleft':
            sdl2.SDL_SetCursor(self.__cursor_trbl)
        elif cursor_name == 'bottomright':
            sdl2.SDL_SetCursor(self.__cursor_tlbr)
        elif cursor_name == 'left':
            sdl2.SDL_SetCursor(self.__cursor_lr)
        elif cursor_name == 'right':
            sdl2.SDL_SetCursor(self.__cursor_lr)
        elif cursor_name == 'top':
            sdl2.SDL_SetCursor(self.__cursor_tb)
        elif cursor_name == 'bottom':
            sdl2.SDL_SetCursor(self.__cursor_tb)
        else:
            sdl2.SDL_SetCursor(self.__cursor_arrow)
 
    def __detect_edge(self, event) -> str:
        w = ctypes.c_int()
        h = ctypes.c_int()
        sdl2.SDL_GetWindowSize(self.__win.window, ctypes.byref(w), ctypes.byref(h))

        local_x = event.button.x
        local_y = event.button.y

        left   = local_x < self.__csd_edge
        right  = local_x > w.value - self.__csd_edge
        top    = local_y < self.__csd_edge
        bottom = local_y > h.value - self.__csd_edge

        if top and left: return 'topleft'
        if top and right: return 'topright'
        if bottom and left: return 'bottomleft'
        if bottom and right: return 'bottomright'
        if left: return 'left'
        if right: return'right'
        if top: return 'top'
        if bottom: return 'bottom'
        
        return None
    
    def __move_or_resize_window(self, event) -> None:
        sdl2.SDL_GetGlobalMouseState(
            ctypes.byref(self.__mouse_global_x), ctypes.byref(self.__mouse_global_y))

        mouse_delta_x = self.__mouse_global_x.value - self.__mouse_start_x.value
        mouse_delta_y = self.__mouse_global_y.value - self.__mouse_start_y.value

        # Drag
        if self.__csd_move and self.__mouse_action == 'drag':
            sdl2.SDL_SetWindowPosition(self.__win.window,
                self.__win_x.value + mouse_delta_x, self.__win_y.value + mouse_delta_y)

        # Resize
        elif self.__csd_resize and self.__mouse_action == 'resize':
            new_w = self.__start_w.value
            new_h = self.__start_h.value
            new_x = self.__win_start_x.value
            new_y = self.__win_start_y.value

            if 'right' in self.__saved_edge_name:
                new_w += mouse_delta_x
            if 'bottom' in self.__saved_edge_name:
                new_h += mouse_delta_y
            if 'left' in self.__saved_edge_name:
                new_w -= mouse_delta_x
                new_x += mouse_delta_x
            if 'top' in self.__saved_edge_name:
                new_h -= mouse_delta_y
                new_y += mouse_delta_y

            new_w = max(200, new_w)
            new_h = max(150, new_h)

            sdl2.SDL_SetWindowPosition(self.__win.window, new_x, new_y)
            sdl2.SDL_SetWindowSize(self.__win.window, new_w, new_h)

            self.__resizig = True
    
    def __update_move_resize_controls(self, event) -> None:
        self.__saved_edge_name = self.__cursor_edge
        sdl2.SDL_GetGlobalMouseState(
            ctypes.byref(self.__mouse_global_x), ctypes.byref(self.__mouse_global_y))

        if self.__cursor_edge:
            self.__mouse_action = 'resize'
            self.__mouse_start_x.value = self.__mouse_global_x.value
            self.__mouse_start_y.value = self.__mouse_global_y.value

            sdl2.SDL_GetWindowSize(self.__win.window,
                ctypes.byref(self.__start_w), ctypes.byref(self.__start_h))
    
            sdl2.SDL_GetWindowPosition(self.__win.window,
                ctypes.byref(self.__win_start_x), ctypes.byref(self.__win_start_y))
        else:
            self.__mouse_action = 'drag'
            sdl2.SDL_GetWindowPosition(
                self.__win.window, ctypes.byref(self.__win_x), ctypes.byref(self.__win_y))
            
            self.__mouse_start_x.value = self.__mouse_global_x.value
            self.__mouse_start_y.value = self.__mouse_global_y.value


if __name__ == "__main__":
    app = Frame()
    sys.exit(app.run())
