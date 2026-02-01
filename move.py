import sys
import ctypes
import sdl2
import sdl2.ext

W, H = 400, 300

def run():
    sdl2.ext.init()

    window = sdl2.ext.Window(
        "Drag Window",
        size=(W, H),
        flags=sdl2.SDL_WINDOW_BORDERLESS
    )

    renderer = sdl2.SDL_CreateRenderer(
        window.window, -1,
        sdl2.SDL_RENDERER_ACCELERATED
    )

    window.show()

    dragging = False
    start_x = start_y = 0

    win_x = ctypes.c_int()
    win_y = ctypes.c_int()
    mx = ctypes.c_int()
    my = ctypes.c_int()

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False

            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    dragging = True

                    sdl2.SDL_GetGlobalMouseState(
                        ctypes.byref(mx),
                        ctypes.byref(my)
                    )

                    sdl2.SDL_GetWindowPosition(
                        window.window,
                        ctypes.byref(win_x),
                        ctypes.byref(win_y)
                    )

                    start_x, start_y = mx.value, my.value

            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                dragging = False

            elif event.type == sdl2.SDL_MOUSEMOTION and dragging:
                sdl2.SDL_GetGlobalMouseState(
                    ctypes.byref(mx),
                    ctypes.byref(my)
                )

                dx = mx.value - start_x
                dy = my.value - start_y

                sdl2.SDL_SetWindowPosition(
                    window.window,
                    win_x.value + dx,
                    win_y.value + dy
                )

        sdl2.SDL_RenderPresent(renderer)

    return 0

if __name__ == "__main__":
    sys.exit(run())
