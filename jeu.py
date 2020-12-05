import pygame
from menu import MainMenu

class Game():

    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = "8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.curr_menu = MainMenu(self) #reference vers la fonction menu principal

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text("Merci d'avoir joué !", 20, self.DISPLAY_W/2, self.DISPLAY_W/2)#fin du jeu
            self.window.blit(self.display, (0,0)) #coordonnees
            pygame.display.update()
            self.reset_keys()#remet toutes les cles a False

    #check the player inputs
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.type==pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK.KEY = True
                if event.type == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.type==pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()#pour les calculs, la position de rectangle
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)







