#!/usr/bin/env python3

# Install commands:
# sudo python3 -m venv caliumlite
# source caliumlite/bin/activate
# pip install pygame-ce
# pip install pyinstaller

# pyinstaller caliumlite.py --onefile
# chmod +x dist/caliumlite
# sudo mv dist/caliumlite /usr/local/bin
# sudo chmod +x /usr/local/bin/caliumlite

import pygame
import random
import sys
import threading

# Alphabet keys
k_a = pygame.K_a            # 'a' key
k_b = pygame.K_b            # 'b' key
k_c = pygame.K_c            # 'c' key
k_d = pygame.K_d            # 'd' key
k_e = pygame.K_e            # 'e' key
k_f = pygame.K_f            # 'f' key
k_g = pygame.K_g            # 'g' key
k_h = pygame.K_h            # 'h' key
k_i = pygame.K_i            # 'i' key
k_j = pygame.K_j            # 'j' key
k_k = pygame.K_k            # 'k' key
k_l = pygame.K_l            # 'l' key
k_m = pygame.K_m            # 'm' key
k_n = pygame.K_n            # 'n' key
k_o = pygame.K_o            # 'o' key
k_p = pygame.K_p            # 'p' key
k_q = pygame.K_q            # 'q' key
k_r = pygame.K_r            # 'r' key
k_s = pygame.K_s            # 's' key
k_t = pygame.K_t            # 't' key
k_u = pygame.K_u            # 'u' key
k_v = pygame.K_v            # 'v' key
k_w = pygame.K_w            # 'w' key
k_x = pygame.K_x            # 'x' key
k_y = pygame.K_y            # 'y' key
k_z = pygame.K_z            # 'z' key

# Number keys
k_0 = pygame.K_0            # '0' key
k_1 = pygame.K_1            # '1' key
k_2 = pygame.K_2            # '2' key
k_3 = pygame.K_3            # '3' key
k_4 = pygame.K_4            # '4' key
k_5 = pygame.K_5            # '5' key
k_6 = pygame.K_6            # '6' key
k_7 = pygame.K_7            # '7' key
k_8 = pygame.K_8            # '8' key
k_9 = pygame.K_9            # '9' key

# Special keys
k_SPACE = pygame.K_SPACE    # Spacebar
k_ENTER = pygame.K_RETURN   # Enter key
k_TAB = pygame.K_TAB        # Tab key
k_BACKSPACE = pygame.K_BACKSPACE  # Backspace key
k_ESCAPE = pygame.K_ESCAPE  # Escape key
k_SHIFT = pygame.K_LSHIFT   # Left Shift key
k_CTRL = pygame.K_LCTRL     # Left Control key
k_ALT = pygame.K_LALT       # Left Alt key

# Arrow Keys
k_UP = pygame.K_UP          # Up arrow key
k_DOWN = pygame.K_DOWN      # Down arrow key
k_LEFT = pygame.K_LEFT      # Left arrow key
k_RIGHT = pygame.K_RIGHT    # Right arrow key

# Function Keys
k_F1 = pygame.K_F1          # F1 key
k_F2 = pygame.K_F2          # F2 key
k_F3 = pygame.K_F3          # F3 key
k_F4 = pygame.K_F4          # F4 key
k_F5 = pygame.K_F5          # F5 key
k_F6 = pygame.K_F6          # F6 key
k_F7 = pygame.K_F7          # F7 key
k_F8 = pygame.K_F8          # F8 key
k_F9 = pygame.K_F9          # F9 key
k_F10 = pygame.K_F10        # F10 key
k_F11 = pygame.K_F11        # F11 key
k_F12 = pygame.K_F12        # F12 key

k_LMB = pygame.BUTTON_LEFT     # Left Mouse Button (LMB)
k_MMB = pygame.BUTTON_MIDDLE   # Middle Mouse Button (MMB)
k_RMB = pygame.BUTTON_RIGHT    # Right Mouse Button (RMB)
k_WHEELUP = pygame.MOUSEBUTTONUP # Mouse Wheel Up
k_WHEELDOWN = pygame.MOUSEBUTTONDOWN # Mouse Wheel Down

class engine:
    def __init__(self, WindowWidth, WindowHeight):
        self.width = WindowWidth
        self.height = WindowHeight
        self.AutomaticUpdates = True
        self.keypresses = []
        self.fillcolor = (255, 255, 255)

        self.setupfuncs = []
        self.loopfuncs = []
        self.inputfuncs = []
        self.threadedfuncs = {}

    # Pygame Setup
    def assignstandardfunctions(self, setupfuncs: list[callable], loopfuncs: list[callable], inputfuncs: list[callable]):
        """
        The functions in the setupfunc list are gonna be executed on startup, the functions in loopfuncs are gonna get executed on every tick and the functions in inputfuncs get called on every tick and receive a list of all pressed keys
        All functions require an input for the GAME variable. But the inputfunctions require a couple more:

        def inputfunc(keypresses: list[int], mouseposition: tuple[int, int], mousemovement: tuple[int, int])
        
        Keypresses is a list containing all current keypresses and mouseclicks (LMB, RMB and MMB). Mouseposition is the position of the mouse on the game window and mousemovement is how the mouse has moved since last frame

        """
        self.setupfuncs = setupfuncs
        self.loopfuncs = loopfuncs
        self.inputfuncs = inputfuncs


    def mainloop(self):
        for i in self.loopfuncs:
            i(self)


    def update(self):
        pygame.display.flip()
        self.screen.fill(self.fillcolor)


    def start(self):
        # Setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.run = True

        for i in self.setupfuncs:
            i(self)

        # Main loop:
        while self.run:
            self.mainloop()
            if self.AutomaticUpdates:
                self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.keypresses.append(event.key)
                
                if event.type == pygame.KEYUP:
                    self.keypresses.remove(event.key)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.keypresses.append(event.button)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.keypresses.remove(event.button)

            for i in self.inputfuncs:
                i(self, self.keypresses, pygame.mouse.get_pos(), pygame.mouse.get_rel())

    
    def threadfunction(self, name, function: callable):
        """
        Threads a function under the name "name"
        """
        self.threadedfuncs[name] = threading.Thread(target=function, args=[self])
        self.threadedfuncs[name].start()


    def stopthread(self, name):
        print(self.threadedfuncs)
        self.threadedfuncs[name].join()


if __name__ == "__main__":
    game = engine(1200, 800)
    #game.AssignStandardFunctions(setupfuncs=[Setup], loopfuncs=[Update], inputfuncs=[])
    game.fillcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    game.start()