#!/usr/bin/env python3
import ctypes
import math

import sdl2
import sdl2.ext


class Draw(object):
    """..."""
    def __init__(self, frame, renderer) -> None:
        self.__frame = frame
        self.__renderer = renderer

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def image(self) -> None:
        """..."""
        pass

    def rect(
        self, x, y, w, h, radius=8, color=(0,0,0,255),
        frame_background: bool = False) -> None:

        r = radius
        ren = self.__renderer
        cr, cg, cb, ca = color

        # IMPORTANTE: habilitar blend
        sdl2.SDL_SetRenderDrawBlendMode(
            ren, sdl2.SDL_BLENDMODE_BLEND
        )

        if frame_background:
            sdl2.SDL_SetRenderDrawColor(ren, 0, 0, 0, 0)
            sdl2.SDL_RenderClear(ren)

        # Corpo (sem AA)
        sdl2.SDL_SetRenderDrawColor(ren, cr, cg, cb, ca)

        sdl2.SDL_RenderFillRect(
            ren, sdl2.SDL_Rect(x + r, y, w - 2*r, h)
        )
        sdl2.SDL_RenderFillRect(
            ren, sdl2.SDL_Rect(x, y + r, w, h - 2*r)
        )

        # Cantos com alpha falloff
        # corners = [
        #     (x + r,     y + r),
        #     (x + w - r, y + r),
        #     (x + r,     y + h - r),
        #     (x + w - r, y + h - r),
        # ]

        corners = [
            (x + r - 1,     y + r - 1),     # top-left
            (x + w - r,     y + r - 1),     # top-right
            (x + r - 1,     y + h - r),     # bottom-left
            (x + w - r,     y + h - r),     # bottom-right
        ]

        for cx, cy in corners:
            # for dy in range(-r, r):
            #     for dx in range(-r, r):
            for dy in range(-r, r+1):
                for dx in range(-r, r+1):

                    dist = math.sqrt(dx*dx + dy*dy)

                    if dist <= r:
                        # faixa de suavização (1px)
                        edge = r - dist
                        if edge < 1.0:
                            alpha = int(ca * edge)  # 0..ca
                        else:
                            alpha = ca

                        sdl2.SDL_SetRenderDrawColor(
                            ren, cr, cg, cb, alpha
                        )
                        sdl2.SDL_RenderDrawPoint(
                            ren, cx + dx, cy + dy
                        )

    def text(self) -> None:
        """..."""
        pass
