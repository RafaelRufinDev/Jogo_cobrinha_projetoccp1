from Bytes_Universe_Game_Engine_V1 import Window
import pygame as pg 
import random
import time



class Snake_Game:
    def __init__(self):
        # cores do jogo
        self.color = {
            'black': (  0,   0,   0),
            'gray':  (150, 150, 150),
            'white': (255, 255, 255),
            'red':   (255,   0,   0),
            'green': (  0, 255,   0),
            'blue':  (  0,   0, 255)
        }

        # fonte do contador de pontuação
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", 50, bold=True)

        # mapa do jogo

        self.map_size = (53, 30)
        self.map = [['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']]
        #posições iniciais da cobra e da maçã
        self.apple_position = (10, 10)
        self.snake_position = [(41, 20), (41, 21), (41, 22), (41, 23), (42, 23), (43, 23)]
        self.snake_direction = (-1, 0)
        self.score = 0
        self.countdown = 3
        self.end_game = False
        self.key_pressed = False
        self.key_pressed_log = ''

    def snake_change_direction(self, key):
        if (key == 'w' or key == 'up') and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif (key == 'a' or key == 'left') and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif (key == 's' or key == 'down') and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)
        elif (key == 'd' or key == 'right') and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)

    def game_start_countdown(self, window):
        #desenho de um círculo na tela
        pg.draw.circle(window, self.color['white'], (636, 360), 50)

        # texto desenhado ao centro do círculo, contador
        if self.countdown == 3:
            countdown_text = self.font.render('3', True, self.color['black'])
            window.blit(countdown_text, (620, 336))
            self.countdown -= 1
        elif self.countdown == 2:
            countdown_text = self.font.render('2', True, self.color['black'])
            window.blit(countdown_text, (620, 336))
            self.countdown -= 1
        elif self.countdown == 1:
            countdown_text = self.font.render('1', True, self.color['black'])
            window.blit(countdown_text, (620, 336))
            self.countdown -= 1
        elif self.countdown == 0:
            countdown_text = self.font.render('Go!', True, self.color['black'])
            window.blit(countdown_text, (595, 336))
            self.countdown -= 1

        pg.display.update()
        time.sleep(1)

    def draw_map_elements(self, window):
        # tamanho do quadrado(cada bloco)
        side = window.get_height() / self.map_size[1]

        # loop para encontrar elementos no mapa
        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                #desenho da posição da cobra
                if self.map[y][x] == 's':
                    pg.draw.rect(window, self.color['green'], (x * side , y * side, side, side))
                # desenho da posição da maçã
                if self.map[y][x] == 'a':
                    pg.draw.rect(window, self.color['red'], (x * side , y * side, side, side))

    def update_snake_position(self, snake):
        snake_size = len(snake) - 1
        for i in range(len(snake)):
            if snake_size - i == 0:
                self.snake_position[0] = (self.snake_position[0][0] + self.snake_direction[0], self.snake_position[0][1] + self.snake_direction[1])
            else:
                self.snake_position[snake_size - i] = self.snake_position[snake_size - i - 1]

    def sort_apple_position(self):
        map_x = len(self.map[0])
        map_y = len(self.map)
        x = random.randint(0, map_x - 1)
        y = random.randint(0, map_y - 1)
        self.apple_position = (x, y)

    def clear_map(self, target_map):
        for y in range(len(target_map)):
            for x in range(len(target_map[0])):
                target_map[y][x] = ''

    def add_snake_position(self, map_size, snake):
        for y in range(map_size[1]):
            for x in range(map_size[0]):
                for s in range(len(snake)):
                    if snake[s][0] == x and snake[s][1] == y:
                        self.map[y][x] = 's'

    def add_apple_position(self, map_size, apple):
        for y in range(map_size[1]):
            for x in range(map_size[0]):
                if y == apple[1] and x == apple[0]:
                    self.map[y][x] = 'a'

    def snake_get_apple(self):
        # verificador se a maçã foi comida pela cobra
        # se a posição da cobra for igual a posição da maçã, a cobra come a maçã
        # e a maçã é reposicionada em outra posição aleatória
        # e a pontuação aumenta em 1
        if self.snake_position[0] == self.apple_position:
            self.snake_position.append(self.snake_position[len(self.snake_position) - 1])
            self.sort_apple_position()
            self.score += 1

    def draw_score(self, window):
        score_text = self.font.render('Score: ' + str(self.score), True, self.color['white'])
        window.blit(score_text, (0, 0))

    def end_of_game(self):
        # verificar se a cobra saiu do mapa
        # se a posição da cobra for menor que 0 ou maior que o tamanho do mapa, o jogo acaba    
        # e a pontuação é zerada
        # e a cobra é reposicionada na posição inicial

        if self.snake_position[0][0] < 0 or self.snake_position[0][1] < 0 or self.snake_position[0][0] > self.map_size[0] - 1 or self.snake_position[0][1] > self.map_size[1] - 1:
            self.end_game = True

        # verificar se a cobra colidiu com ela mesma
        # se a posição da cobra for igual a qualquer outra posição da cobra, o jogo acaba
        # e a pontuação é zerada
        # e a cobra é reposicionada na posição inicial
        
        for i in range(1, len(self.snake_position)):
            if self.snake_position[0] == self.snake_position[i]:
                self.end_game = True

    def draw_end_game(self, window):
        # Desenho tela de fim de jogo
        if self.end_game == True:
            score_text = self.font.render('End Game', True, self.color['white'])
            window.blit(score_text, (525, 336))

    def home_screen_animation(self, window):
        # atualizar a posição da cobra
        self.update_snake_position(self.snake_position)

        # script de atualização da posição da cobra
        if self.snake_position[0] == (12, 20) and len(self.snake_position) <= 25:
            self.snake_direction = (0, -1)
        elif self.snake_position[0] == (12, 15):
            self.snake_direction = (-1, 0)
        elif self.snake_position[0] == (10, 15):
            self.snake_direction = (0, -1)
        elif self.snake_position[0] == (10, 10):
            self.snake_position.append(self.snake_position[len(self.snake_position) - 1])
            self.score += 1
            self.apple_position = (40, 15)
        elif self.snake_position[0] == (10, 5):
            self.snake_direction = (1, 0)
        elif self.snake_position[0] == (41, 5):
            self.snake_direction = (0, 1)
        elif self.snake_position[0] == (41, 10):
            self.snake_direction = (-1, 0)
        elif self.snake_position[0] == (40, 10):
            self.snake_direction = (0, 1)
        elif self.snake_position[0] == (40, 15):
            self.snake_position.append(self.snake_position[len(self.snake_position) - 1])
            self.score += 1
            self.apple_position = (10, 10)
        elif self.snake_position[0] == (40, 20):
            self.snake_direction = (-1, 0)
        elif self.snake_position[0] == (-30, 20):
            self.score = 0
            self.snake_position = [(55, 20), (56, 20), (57, 20), (58, 20), (59, 20)]

        self.clear_map(self.map)

        self.add_snake_position(self.map_size, self.snake_position)
        self.add_apple_position(self.map_size, self.apple_position)

        self.draw_map_elements(window)
        self.draw_score(window)

    def reset_game(self):
        self.end_game = False
        self.score = 0
        self.snake_position = [(40, 20), (41, 20), (41, 21), (41, 22), (41, 23), (42, 23)]
        self.apple_position = (10, 10)
        self.snake_direction = (-1, 0)