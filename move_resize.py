import sys
import ctypes
import sdl2
import sdl2.ext

W, H = 400, 300
EDGE = 8

def hit_test(x, y, w, h):
    left   = x < EDGE
    right  = x > w - EDGE
    top    = y < EDGE
    bottom = y > h - EDGE

    if top and left:    return 'topleft'
    if top and right:   return 'topright'
    if bottom and left: return 'bottomleft'
    if bottom and right:return 'bottomright'
    if left:   return 'left'
    if right:  return 'right'
    if top:    return 'top'
    if bottom: return 'bottom'
    return None


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window('Custom Window', size=(W, H), flags=sdl2.SDL_WINDOW_BORDERLESS)
    renderer = sdl2.SDL_CreateRenderer(window.window, -1, sdl2.SDL_RENDERER_ACCELERATED)
    window.show()

    # Flags
    mode = None # None | "drag" | "resize"
    resize_mode = None

    # ctypes
    mouse_global_x = ctypes.c_int()
    mouse_global_y = ctypes.c_int()
    mouse_start_x = ctypes.c_int()
    mouse_start_y = ctypes.c_int()

    win_x = ctypes.c_int()
    win_y = ctypes.c_int()
    win_start_x = ctypes.c_int()
    win_start_y = ctypes.c_int()

    start_w = ctypes.c_int()
    start_h = ctypes.c_int()

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False

            # Press
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    local_x = event.button.x
                    local_y = event.button.y

                    resize_mode = hit_test(local_x, local_y, W, H)

                    sdl2.SDL_GetGlobalMouseState(
                        ctypes.byref(mouse_global_x), ctypes.byref(mouse_global_y))

                    if resize_mode:
                        mode = 'resize'
                        mouse_start_x.value = mouse_global_x.value
                        mouse_start_y.value = mouse_global_y.value

                        sdl2.SDL_GetWindowSize(
                            window.window, ctypes.byref(start_w), ctypes.byref(start_h))
                        
                        sdl2.SDL_GetWindowPosition(
                            window.window, ctypes.byref(win_start_x), ctypes.byref(win_start_y))
                    else:
                        mode = 'drag'
                        sdl2.SDL_GetWindowPosition(
                            window.window, ctypes.byref(win_x), ctypes.byref(win_y))
                        mouse_start_x.value = mouse_global_x.value
                        mouse_start_y.value = mouse_global_y.value

            # Release
            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                mode = None
                resize_mode = None

            # Move
            elif event.type == sdl2.SDL_MOUSEMOTION and mode:
                sdl2.SDL_GetGlobalMouseState(
                    ctypes.byref(mouse_global_x), ctypes.byref(mouse_global_y))

                mouse_delta_x = mouse_global_x.value - mouse_start_x.value
                mouse_delta_y = mouse_global_y.value - mouse_start_y.value

                # Drag
                if mode == 'drag':
                    sdl2.SDL_SetWindowPosition(
                        window.window, win_x.value + mouse_delta_x, win_y.value + mouse_delta_y)

                # Resize
                elif mode == 'resize':
                    new_w = start_w.value
                    new_h = start_h.value
                    new_x = win_start_x.value
                    new_y = win_start_y.value

                    if 'right' in resize_mode:
                        new_w += mouse_delta_x
                    if 'bottom' in resize_mode:
                        new_h += mouse_delta_y
                    if 'left' in resize_mode:
                        new_w -= mouse_delta_x
                        new_x += mouse_delta_x
                    if 'top' in resize_mode:
                        new_h -= mouse_delta_y
                        new_y += mouse_delta_y

                    new_w = max(200, new_w)
                    new_h = max(150, new_h)

                    sdl2.SDL_SetWindowPosition(window.window, new_x, new_y)
                    sdl2.SDL_SetWindowSize(window.window, new_w, new_h)

        sdl2.SDL_RenderPresent(renderer)

    return 0


if __name__ == '__main__':
    sys.exit(run())
