import pygame as pg
import time

# cores do jogo
white   = (255, 255, 255)
gray    = (150, 150, 150)
black   = (  0,   0,   0)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)

class Window:
    def __init__(self, screen_resolution='HD', window_title='New Game', icon=None, fps=60):
        # variáveis do jogo
        self.resolutions = {
            'HD': (1280, 720),
            'FHD': (1920, 1080)
        }
        try:
            self.window = pg.display.set_mode(self.resolutions[screen_resolution])
        except:
            self.window = pg.display.set_mode(screen_resolution)
        # Define o título da janela para self.window_title e o título do ícone para self.icon

        #posição do mouse em relação ao pygame
        self.mouse_0 = {'x' : None, 'y' : None, 'left button' : None, 'clicked' : False}
        self.mouse = ((0,0)(False,False,False), (False, False,False))

        # variáveis de fonte de texto
        pg.font.init()
        self.fonte = pg.font.SysFont('Courier New', 50, bold=True)   
        self.fonte = pg.font.SysFont('Courier New', 30, bold=True)   

        self.last_click_status = (False, False, False)

        self.home_menu = True
        self.pause_menu = False
        self.game_difficulty = 0

        #cores game
        self.color = {
            'white' : (255, 255, 255),
            'gray' : (150, 150, 150),
            'black' : (  0,   0,   0),
            'red'   : (255,   0,   0),
            'red light1' : (50, 100, 50),
            'red light2' : (100, 150, 100),
            'red light3' : (100, 200, 150),
            'green' : (  0, 255,   0),
            'green light1' : (50, 255, 50),
            'green light2' : (100, 255, 100),
            'green light3' : (150, 255, 150),
            'blue'  : (  0,   0, 255),
            'blue light1' : (50, 50, 255),
            'blue light2' : (100, 100, 255),
            'blue light3' : (150, 150, 255)
        }

        # tempo de pausa, 1s #

        def fps(self, fps=60):
            time.sleep(1/fps)

        #informações do jogo/sistema #

            if self.last_click_status == input:
                return (False,False,False)
            else:
                left_button = False
                center_button = False
                right_button = False
                if self.last_click_status[0] == False and input[0] == True:
                    left_button = True
                if self.last_click_status[1] == False and input[1] == True:
                    center_button = True        
                if self.last_click_status[2] == False and input[2] == True: 
                    right_button = True

                self.last_click_status

                return (left_button, center_button, right_button)

            # desenho do jogo 

            def clear_window(self, alpha=128):
                pg.draw.rect(self.window, color, (0, 0, self.window.get_width(), self.window.get_height()))

            def trasparent_background(self,color):
                surface = pg.Surface((self.window.get_width(), self.window.get_height()))
                surface.set_alpha(128)
                surface.fill(self.color[color])
                self.window.blit(surface, (0, 0))
            
            def transparent_suface(self, positions_x, positions_y, size_X, size_y):
                surface = pg.Surface((size_X, size_y))
                surface.set_alpha(128)
                surface.fill(white)
                self.window.blit(surface, (positions_x, positions_y))
                

                