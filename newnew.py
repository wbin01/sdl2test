import sys
import ctypes
import sdl2
import sdl2.ext

W, H = 800, 600
R = 30

# QT_QPA_PLATFORM=xcb python newnew.py
# SDL_VIDEODRIVER=x11 python newnew.py

def run():
    sdl2.ext.init()

    # Força buffer com alpha real
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_RED_SIZE, 8)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_GREEN_SIZE, 8)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_BLUE_SIZE, 8)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_ALPHA_SIZE, 8)

    window = sdl2.ext.Window(
        "Rounded",
        size=(W, H),
        flags=sdl2.SDL_WINDOW_BORDERLESS
    )

    renderer = sdl2.SDL_CreateRenderer(
        window.window, -1,
        sdl2.SDL_RENDERER_ACCELERATED
    )

    sdl2.SDL_SetRenderDrawBlendMode(renderer, sdl2.SDL_BLENDMODE_BLEND)
    window.show()

    running = True
    while running:
        dragging = False
        start_x = start_y = 0
        win_x = win_y = 0

        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
            
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    dragging = True
                    sdl2.SDL_GetGlobalMouseState(ctypes.byref(mx), ctypes.byref(my))
                    sdl2.SDL_GetWindowPosition(window.window,
                                            ctypes.byref(win_x),
                                            ctypes.byref(win_y))
                    start_x, start_y = mx.value, my.value

            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                dragging = False

            elif event.type == sdl2.SDL_MOUSEMOTION and dragging:
                sdl2.SDL_GetGlobalMouseState(ctypes.byref(mx), ctypes.byref(my))
                dx = mx.value - start_x
                dy = my.value - start_y
                sdl2.SDL_SetWindowPosition(window.window, win_x + dx, win_y + dy)

        # Limpa com alpha 0 (transparente real)
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0)
        sdl2.SDL_RenderClear(renderer)

        # Corpo
        sdl2.SDL_SetRenderDrawColor(renderer, 50, 50, 50, 255)
        sdl2.SDL_RenderFillRect(
            renderer,
            sdl2.SDL_Rect(R, 0, W-2*R, H)
        )
        sdl2.SDL_RenderFillRect(
            renderer,
            sdl2.SDL_Rect(0, R, W, H-2*R)
        )

        # Cantos
        for cx, cy in [
            (R, R), (W-R, R),
            (R, H-R), (W-R, H-R)
        ]:
            for y in range(-R, R):
                for x in range(-R, R):
                    if x*x + y*y <= R*R:
                        sdl2.SDL_RenderDrawPoint(renderer, cx+x, cy+y)

        sdl2.SDL_RenderPresent(renderer)

    return 0

if __name__ == "__main__":
    sys.exit(run())
