import sys
import sdl2.ext

# Set
RESOURCES = sdl2.ext.Resources(__file__, 'resources')

# Window
sdl2.ext.init()

window = sdl2.ext.Window('Hello World!', size=(400, 300))
window.show()

# Sprite
factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite = factory.from_image(RESOURCES.get_path('hello.bmp'))

spriterenderer = factory.create_sprite_render_system(window)
sprite.position = 10, 20
spriterenderer.render(sprite)

# Run
processor = sdl2.ext.TestEventProcessor()
processor.run(window)

# Exit
sdl2.ext.quit()
