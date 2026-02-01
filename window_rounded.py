import sys
import sdl2
import sdl2.ext
import ctypes
import math

WIDTH, HEIGHT = 400, 300
RADIUS = 24
"""
window = sdl2.SDL_CreateShapedWindow(
    b"shaped",
    100, 100,
    800, 600,
    sdl2.SDL_WINDOW_BORDERLESS
)
E aplicar um SDL_Surface como máscara.

"""

def run():
    sdl2.ext.init()

    window = sdl2.ext.Window(
        "Rounded",
        size=(WIDTH, HEIGHT),
        flags=sdl2.SDL_WINDOW_BORDERLESS | sdl2.SDL_WINDOW_ALLOW_HIGHDPI
    )

    # Permitir alpha real no compositor
    sdl2.SDL_SetHint(sdl2.SDL_HINT_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR, b"0")

    renderer = sdl2.SDL_CreateRenderer(
        window.window, -1,
        sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
    )

    sdl2.SDL_SetRenderDrawBlendMode(renderer, sdl2.SDL_BLENDMODE_BLEND)

    window.show()

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False

        # Limpa tudo transparente
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0)
        sdl2.SDL_RenderClear(renderer)

        # Desenha "corpo" da janela
        sdl2.SDL_SetRenderDrawColor(renderer, 40, 40, 40, 255)
        body = sdl2.SDL_Rect(RADIUS, 0, WIDTH - 2*RADIUS, HEIGHT)
        sdl2.SDL_RenderFillRect(renderer, body)

        body = sdl2.SDL_Rect(0, RADIUS, WIDTH, HEIGHT - 2*RADIUS)
        sdl2.SDL_RenderFillRect(renderer, body)

        # Desenha 4 círculos (cantos)
        for cx, cy in [
            (RADIUS, RADIUS),
            (WIDTH - RADIUS, RADIUS),
            (RADIUS, HEIGHT - RADIUS),
            (WIDTH - RADIUS, HEIGHT - RADIUS),
        ]:
            for y in range(-RADIUS, RADIUS):
                for x in range(-RADIUS, RADIUS):
                    if x*x + y*y <= RADIUS*RADIUS:
                        sdl2.SDL_RenderDrawPoint(renderer, cx+x, cy+y)

        sdl2.SDL_RenderPresent(renderer)

    return 0

if __name__ == "__main__":
    sys.exit(run())
