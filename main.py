import asyncio, pygame, time, math, sys, platform

pygame.init()
pygame.mixer.init()

# ----------- GLOBALS ----------- #
# check if python is running through emscripten
WEB_PLATFORM = sys.platform == "emscripten"
if WEB_PLATFORM:
    # for document/canvas interaction
    import js # type: ignore
    # keep pixelated look for pygbag
    platform.window.canvas.style.imageRendering = "pixelated"

WIDTH, HEIGHT = 640, 480
SCALE = 2

class App:
    def __init__(self):
        # no need for separate scaling, pygbag scales canvas automatically
        self.display = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)
        self.screen = pygame.Surface((WIDTH // SCALE, HEIGHT // SCALE))
        self.active = True # if tab is focused when running through web

        self.clock = pygame.time.Clock()
        # delta time
        self.dt = 1
        self.last_time = time.time() - 1/60
    
    # put all the game stuff here
    def update(self):
        # update delta time
        self.dt = (time.time() - self.last_time) * 60
        self.last_time = time.time()

        self.screen.fill((int(255 - (math.sin(time.time()) * 125 + 125)), int(math.sin(time.time()) * 125 + 125), 0))

    # asynchronous main loop to run in browser
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.WINDOWRESIZED:
                    self.screen = pygame.Surface((self.display.get_width() // SCALE, self.display.get_height() // SCALE))
            
            # update game
            self.update()

            # check if tab is focused if running through web (avoid messing up dt and stuff)
            if WEB_PLATFORM:
                self.active = not js.document.hidden

            # check if page is active
            if self.active:
                if WEB_PLATFORM:
                    pygame.display.set_caption(f"FPS: {self.clock.get_fps() :.1f}")
                else:
                    pygame.display.set_caption(f"FPS: {self.clock.get_fps() :.1f} Display: {self.screen.get_width()} * {self.screen.get_height()}")
                # scale display
                self.display.blit(pygame.transform.scale2x(self.screen), (0, 0))
                pygame.display.flip()
            else:
                pygame.display.set_caption("IDLE")

            await asyncio.sleep(0) # keep this for pygbag to work
            self.clock.tick(60) # don't really need more than 60 fps

# run App() asynchronously so it works with pygbag
async def main():
    app = App()
    await app.run()

# start
asyncio.run(main())
