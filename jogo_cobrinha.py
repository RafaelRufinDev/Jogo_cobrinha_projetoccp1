import pygame as pg
import time
import random

# Variáveis globais para o estado do jogo e configurações da janela
# Cores do jogo
COLORS = {
    'white': (255, 255, 255),
    'gray': (150, 150, 150),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'red light 1': (50, 100, 50),
    'red light 2': (100, 150, 100),
    'red light 3': (150, 200, 150),
    'green': (0, 255, 0),
    'green light 1': (50, 255, 50),
    'green light 2': (100, 255, 100),
    'green light 3': (150, 255, 150),
    'blue': (0, 0, 255),
    'blue light 1': (50, 50, 255),
    'blue light 2': (100, 100, 255),
    'blue light 3': (150, 150, 255)
}

# Configurações da janela
WINDOW = None
FONT = None
FONT_RB = None
LAST_CLICK_STATUS = (False, False, False)
HOME_MENU = True
PAUSE_MENU = False
GAME_DIFFICULTY = 0
MOUSE = ((0, 0), (False, False, False), (False, False, False))

# Variáveis do jogo Snake
SNAKE_GAME_STATE = {
    'apple_position': (10, 10),
    'snake_position': [(41, 20), (41, 21), (41, 22), (41, 23), (42, 23), (43, 23)],
    'snake_direction': (-1, 0),
    'score': 0,
    'countdown': 3,
    'end_game': False,
    'key_pressed_this_frame': False, # Nova variável para controlar o movimento por frame
    'map_size': (53, 30),
    'game_map': [[''] * 53 for _ in range(30)] # Inicializa o mapa com 30 linhas e 53 colunas
}

# --- Funções da Janela ---

def initialize_window(screen_resolution='HD', window_title='New Game', icon=None):
    """Inicializa a janela do Pygame."""
    global WINDOW, FONT, FONT_RB
    resolutions = {
        'HD': (1280, 720),
        'FHD': (1920, 1080)
    }
    try:
        WINDOW = pg.display.set_mode(resolutions[screen_resolution])
    except KeyError:
        WINDOW = pg.display.set_mode(screen_resolution)

    pg.display.set_caption(window_title)
    if icon:
        pg.display.set_icon(icon)

    pg.font.init()
    FONT = pg.font.SysFont("Courier New", 50, bold=True)
    FONT_RB = pg.font.SysFont("Courier New", 30, bold=True)

def set_fps(fps=60):
    """Controla o FPS do jogo."""
    time.sleep(1 / fps)

def mouse_has_clicked(current_input):
    """Verifica se o mouse foi clicado (apenas no momento do clique, não segurado)."""
    global LAST_CLICK_STATUS
    left_button = False
    center_button = False
    right_button = False

    if LAST_CLICK_STATUS != current_input:
        if not LAST_CLICK_STATUS[0] and current_input[0]:
            left_button = True
        if not LAST_CLICK_STATUS[1] and current_input[1]:
            center_button = True
        if not LAST_CLICK_STATUS[2] and current_input[2]:
            right_button = True

    LAST_CLICK_STATUS = current_input
    return (left_button, center_button, right_button)

def clear_window(color):
    """Limpa a janela com a cor especificada."""
    pg.draw.rect(WINDOW, COLORS[color], (0, 0, WINDOW.get_width(), WINDOW.get_height()))

def transparent_background(color):
    """Cria um fundo transparente na janela."""
    surface = pg.Surface((WINDOW.get_width(), WINDOW.get_height()))
    surface.set_alpha(128)
    surface.fill(COLORS[color])
    WINDOW.blit(surface, (0, 0))

def transparent_surface(position_x, position_y, size_x, size_y):
    """Cria uma superfície transparente em uma posição e tamanho específicos."""
    surface = pg.Surface((size_x, size_y))
    surface.set_alpha(128)
    surface.fill(COLORS['white'])
    WINDOW.blit(surface, (position_x, position_y))

def create_button(position, size, background_color, text, mouse_state, index_of_qtd=(1, 1), border_color=COLORS['black'], border_width=5, font_color=COLORS['black'], text_size=32):
    """Cria e renderiza um botão."""
    position_x, position_y = 0, 0
    if isinstance(position, tuple):
        position_x, position_y = position[0], position[1]
    elif position == 'center':
        if index_of_qtd[1] == 1:
            position_x = (WINDOW.get_width() / 2) - (size[0] / 2)
            position_y = (WINDOW.get_height() / 2) - (size[1] / 2)
        else:
            position_x = WINDOW.get_width() / 2 - (size[0] / 2)
            sum_btn_height = size[1] * index_of_qtd[1]
            sum_gap_btn_height = (size[1] / 2) * (index_of_qtd[1] - 1)
            btn_set_height = sum_btn_height + sum_gap_btn_height
            margin_y = (WINDOW.get_height() - btn_set_height) / 2
            position_y = margin_y + ((size[1] * 1.5) * (index_of_qtd[0] - 1))

    size_x, size_y = size[0], size[1]

    pg.draw.rect(WINDOW, background_color, (position_x, position_y, size_x, size_y))

    if position_x <= mouse_state[0][0] <= position_x + size_x and \
       position_y <= mouse_state[0][1] <= position_y + size_y:
        transparent_surface(position_x, position_y, size_x, size_y)

    pg.draw.rect(WINDOW, border_color, (position_x, position_y, size_x, size_y), border_width)

    font_button = pg.font.SysFont("Consolas", text_size, bold=True)
    text_render = font_button.render(text, True, font_color)
    text_size_x = text_render.get_width()
    text_size_y = text_render.get_height()
    text_position_x = position_x + (size_x / 2) - (text_size_x / 2)
    text_position_y = position_y + (size_y / 2) - (text_size_y / 2)
    WINDOW.blit(text_render, (text_position_x, text_position_y))

    if position_x <= mouse_state[0][0] <= position_x + size_x and \
       position_y <= mouse_state[0][1] <= position_y + size_y and mouse_state[2][0]:
        return text
    else:
        return None

def home_screen(button_list, button_layout=(1, 1)):
    """Renderiza a tela inicial com botões."""
    button_action = [None] * len(button_list)

    for i in range(len(button_list)):
        try:
            button_action[i] = create_button("center", (300, 100), COLORS[button_list[i][1]], button_list[i][0], MOUSE, index_of_qtd=(i + 1, button_layout[1]), border_color=COLORS[button_list[i][2]])
        except IndexError: # Caso não haja border_color na tupla
            button_action[i] = create_button("center", (300, 100), COLORS[button_list[i][1]], button_list[i][0], MOUSE, index_of_qtd=(i + 1, button_layout[1]))

    for action in button_action:
        if action is not None:
            return action
    return None

def pause_screen(button_list, button_layout=(1, 1)):
    """Renderiza a tela de pause com botões."""
    transparent_background('white')

    button_action = [None] * len(button_list)

    for i in range(len(button_list)):
        button_action[i] = create_button("center", (300, 100), COLORS[button_list[i][1]], button_list[i][0], MOUSE, index_of_qtd=(i + 1, button_layout[1]))

    for action in button_action:
        if action is not None:
            return action
    return None

# --- Funções do Jogo Snake ---

def snake_change_direction(key):
    """Altera a direção da cobra com base na tecla pressionada."""
    global SNAKE_GAME_STATE
    if not SNAKE_GAME_STATE['key_pressed_this_frame']: # Permite apenas uma mudança de direção por frame
        if (key == 'w' or key == 'up') and SNAKE_GAME_STATE['snake_direction'] != (0, 1):
            SNAKE_GAME_STATE['snake_direction'] = (0, -1)
            SNAKE_GAME_STATE['key_pressed_this_frame'] = True
        elif (key == 'a' or key == 'left') and SNAKE_GAME_STATE['snake_direction'] != (1, 0):
            SNAKE_GAME_STATE['snake_direction'] = (-1, 0)
            SNAKE_GAME_STATE['key_pressed_this_frame'] = True
        elif (key == 's' or key == 'down') and SNAKE_GAME_STATE['snake_direction'] != (0, -1):
            SNAKE_GAME_STATE['snake_direction'] = (0, 1)
            SNAKE_GAME_STATE['key_pressed_this_frame'] = True
        elif (key == 'd' or key == 'right') and SNAKE_GAME_STATE['snake_direction'] != (-1, 0):
            SNAKE_GAME_STATE['snake_direction'] = (1, 0)
            SNAKE_GAME_STATE['key_pressed_this_frame'] = True

def game_start_countdown():
    """Exibe a contagem regressiva antes do início do jogo."""
    global SNAKE_GAME_STATE
    pg.draw.circle(WINDOW, COLORS['white'], (636, 360), 50)

    if SNAKE_GAME_STATE['countdown'] == 3:
        countdown_text = FONT.render('3', True, COLORS['black'])
        WINDOW.blit(countdown_text, (620, 336))
    elif SNAKE_GAME_STATE['countdown'] == 2:
        countdown_text = FONT.render('2', True, COLORS['black'])
        WINDOW.blit(countdown_text, (620, 336))
    elif SNAKE_GAME_STATE['countdown'] == 1:
        countdown_text = FONT.render('1', True, COLORS['black'])
        WINDOW.blit(countdown_text, (620, 336))
    elif SNAKE_GAME_STATE['countdown'] == 0:
        countdown_text = FONT.render('Go!', True, COLORS['black'])
        WINDOW.blit(countdown_text, (595, 336))

    pg.display.update()
    # Atraso apenas para o contador, não afeta o loop principal do jogo
    time.sleep(1)
    SNAKE_GAME_STATE['countdown'] -= 1


def draw_map_elements():
    """Desenha a cobra e a maçã no mapa."""
    side = WINDOW.get_height() / SNAKE_GAME_STATE['map_size'][1]

    for y in range(SNAKE_GAME_STATE['map_size'][1]):
        for x in range(SNAKE_GAME_STATE['map_size'][0]):
            if SNAKE_GAME_STATE['game_map'][y][x] == 's':
                pg.draw.rect(WINDOW, COLORS['green'], (x * side, y * side, side, side))
            if SNAKE_GAME_STATE['game_map'][y][x] == 'a':
                pg.draw.rect(WINDOW, COLORS['red'], (x * side, y * side, side, side))

def update_snake_position():
    """Atualiza a posição da cobra."""
    # A cabeça da cobra se move na direção atual
    new_head_x = SNAKE_GAME_STATE['snake_position'][0][0] + SNAKE_GAME_STATE['snake_direction'][0]
    new_head_y = SNAKE_GAME_STATE['snake_position'][0][1] + SNAKE_GAME_STATE['snake_direction'][1]
    new_head = (new_head_x, new_head_y)

    # Adiciona a nova cabeça e remove a cauda
    SNAKE_GAME_STATE['snake_position'].insert(0, new_head)
    SNAKE_GAME_STATE['snake_position'].pop()

def sort_apple_position():
    """Gera uma nova posição aleatória para a maçã."""
    map_x = SNAKE_GAME_STATE['map_size'][0]
    map_y = SNAKE_GAME_STATE['map_size'][1]
    while True: # Garante que a maçã não nasça em cima da cobra
        x = random.randint(0, map_x - 1)
        y = random.randint(0, map_y - 1)
        if (x, y) not in SNAKE_GAME_STATE['snake_position']:
            SNAKE_GAME_STATE['apple_position'] = (x, y)
            break

def clear_map():
    """Limpa todos os elementos do mapa."""
    for y in range(SNAKE_GAME_STATE['map_size'][1]):
        for x in range(SNAKE_GAME_STATE['map_size'][0]):
            SNAKE_GAME_STATE['game_map'][y][x] = ''

def add_snake_position_to_map():
    """Adiciona a posição da cobra ao mapa."""
    for s_pos in SNAKE_GAME_STATE['snake_position']:
        s_x, s_y = s_pos
        if 0 <= s_y < SNAKE_GAME_STATE['map_size'][1] and 0 <= s_x < SNAKE_GAME_STATE['map_size'][0]:
            SNAKE_GAME_STATE['game_map'][s_y][s_x] = 's'

def add_apple_position_to_map():
    """Adiciona a posição da maçã ao mapa."""
    apple_x, apple_y = SNAKE_GAME_STATE['apple_position']
    if 0 <= apple_y < SNAKE_GAME_STATE['map_size'][1] and 0 <= apple_x < SNAKE_GAME_STATE['map_size'][0]:
        SNAKE_GAME_STATE['game_map'][apple_y][apple_x] = 'a'

def snake_get_apple():
    """Verifica se a cobra comeu a maçã e atualiza o estado do jogo."""
    global SNAKE_GAME_STATE
    if SNAKE_GAME_STATE['snake_position'][0] == SNAKE_GAME_STATE['apple_position']:
        # Adiciona um novo segmento à cobra (o segmento anterior é mantido na posição da cauda)
        SNAKE_GAME_STATE['snake_position'].append(SNAKE_GAME_STATE['snake_position'][-1])
        sort_apple_position()
        SNAKE_GAME_STATE['score'] += 1

def draw_score():
    """Desenha a pontuação na tela."""
    score_text = FONT.render('Score: ' + str(SNAKE_GAME_STATE['score']), True, COLORS['white'])
    WINDOW.blit(score_text, (0, 0))

def check_end_game():
    """Verifica as condições de fim de jogo (colisão com parede ou com a própria cobra)."""
    global SNAKE_GAME_STATE
    head_x, head_y = SNAKE_GAME_STATE['snake_position'][0]
    map_width, map_height = SNAKE_GAME_STATE['map_size']

    # Colisão com as paredes
    if not (0 <= head_x < map_width and 0 <= head_y < map_height):
        SNAKE_GAME_STATE['end_game'] = True
        return

    # Colisão com a própria cobra
    for i in range(1, len(SNAKE_GAME_STATE['snake_position'])):
        if SNAKE_GAME_STATE['snake_position'][0] == SNAKE_GAME_STATE['snake_position'][i]:
            SNAKE_GAME_STATE['end_game'] = True
            return

def draw_end_game():
    """Desenha a tela de fim de jogo."""
    if SNAKE_GAME_STATE['end_game']:
        end_game_text = FONT.render('Game Over!', True, COLORS['white'])
        text_rect = end_game_text.get_rect(center=(WINDOW.get_width() / 2, WINDOW.get_height() / 2 - 50))
        WINDOW.blit(end_game_text, text_rect)

        # Botão para reiniciar na tela de Game Over
        restart_button_action = create_button("center", (250, 70), COLORS['blue light 2'], "Restart", MOUSE, index_of_qtd=(2,1))
        if restart_button_action == 'Restart':
            reset_game()
            global HOME_MENU # Volta para o jogo, ou se quiser para home: HOME_MENU = True
            HOME_MENU = False
            SNAKE_GAME_STATE['countdown'] = 3 # Reinicia o contador para o novo jogo


def home_screen_animation():
    """Lógica da animação da cobra na tela inicial."""
    global SNAKE_GAME_STATE
    # Reduzir a velocidade da animação para torná-la mais suave
    set_fps(10) # FPS mais baixo para animação
    update_snake_position()

    # Script de movimento da cobra na tela inicial
    current_head = SNAKE_GAME_STATE['snake_position'][0]
    if current_head == (12, 20) and len(SNAKE_GAME_STATE['snake_position']) <= 25:
        SNAKE_GAME_STATE['snake_direction'] = (0, -1)
    elif current_head == (12, 15):
        SNAKE_GAME_STATE['snake_direction'] = (-1, 0)
    elif current_head == (10, 15):
        SNAKE_GAME_STATE['snake_direction'] = (0, -1)
    elif current_head == (10, 10):
        # A cobra "come" a maçã na animação
        if SNAKE_GAME_STATE['apple_position'] == (10,10): # Garante que só come uma vez
            SNAKE_GAME_STATE['snake_position'].append(SNAKE_GAME_STATE['snake_position'][-1])
            SNAKE_GAME_STATE['score'] += 1
            SNAKE_GAME_STATE['apple_position'] = (40, 15) # Move a maçã
        SNAKE_GAME_STATE['snake_direction'] = (1, 0) # Segue em frente
    elif current_head == (10, 5):
        SNAKE_GAME_STATE['snake_direction'] = (1, 0)
    elif current_head == (41, 5):
        SNAKE_GAME_STATE['snake_direction'] = (0, 1)
    elif current_head == (41, 10):
        SNAKE_GAME_STATE['snake_direction'] = (-1, 0)
    elif current_head == (40, 10):
        SNAKE_GAME_STATE['snake_direction'] = (0, 1)
    elif current_head == (40, 15):
        # A cobra "come" a maçã na animação
        if SNAKE_GAME_STATE['apple_position'] == (40,15): # Garante que só come uma vez
            SNAKE_GAME_STATE['snake_position'].append(SNAKE_GAME_STATE['snake_position'][-1])
            SNAKE_GAME_STATE['score'] += 1
            SNAKE_GAME_STATE['apple_position'] = (10, 10) # Move a maçã
        SNAKE_GAME_STATE['snake_direction'] = (-1, 0) # Segue em frente
    elif current_head == (40, 20):
        SNAKE_GAME_STATE['snake_direction'] = (-1, 0)
    elif current_head[0] < -5: # Sai da tela para resetar a posição
        SNAKE_GAME_STATE['score'] = 0
        SNAKE_GAME_STATE['snake_position'] = [(55, 20), (56, 20), (57, 20), (58, 20), (59, 20)]
        SNAKE_GAME_STATE['snake_direction'] = (-1, 0) # Volta para a direção inicial

    clear_map()
    add_snake_position_to_map()
    add_apple_position_to_map()
    draw_map_elements()
    draw_score()

def reset_game():
    """Reinicia o estado do jogo Snake para os valores iniciais."""
    global SNAKE_GAME_STATE
    SNAKE_GAME_STATE['end_game'] = False
    SNAKE_GAME_STATE['score'] = 0
    SNAKE_GAME_STATE['snake_position'] = [(40, 20), (41, 20), (41, 21), (41, 22), (41, 23), (42, 23)]
    SNAKE_GAME_STATE['apple_position'] = (10, 10)
    SNAKE_GAME_STATE['snake_direction'] = (-1, 0)
    SNAKE_GAME_STATE['countdown'] = 3
    SNAKE_GAME_STATE['key_pressed_this_frame'] = False # Reseta para novo jogo

# --- Loop Principal do Jogo ---

def run_game():
    """Função principal que executa o loop do jogo."""
    global HOME_MENU, PAUSE_MENU, MOUSE, SNAKE_GAME_STATE

    initialize_window(screen_resolution=(1272, 720))

    while True:
        # Resetar a flag de tecla pressionada no início de cada frame
        SNAKE_GAME_STATE['key_pressed_this_frame'] = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if not HOME_MENU and not PAUSE_MENU and not SNAKE_GAME_STATE['end_game'] and SNAKE_GAME_STATE['countdown'] <= 0:
                    snake_change_direction(pg.key.name(event.key))
                if pg.key.name(event.key) == 'escape':
                    if not HOME_MENU and not SNAKE_GAME_STATE['end_game']: # Só pode pausar se não estiver no menu inicial ou no fim de jogo
                        PAUSE_MENU = not PAUSE_MENU
                        if PAUSE_MENU: # Se entrou no pause, reseta o contador para 3
                            SNAKE_GAME_STATE['countdown'] = 3


        # Informações do mouse
        mouse_position = pg.mouse.get_pos()
        mouse_input = pg.mouse.get_pressed()
        mouse_click = mouse_has_clicked(mouse_input)
        MOUSE = (mouse_position, mouse_input, mouse_click)

        clear_window('black')

        if HOME_MENU:
            # Animação da tela inicial de menu
            home_screen_animation()

            # Menu da tela inicial
            button_action = home_screen([('Start', 'green', 'gray')])

            if button_action == 'Start':
                HOME_MENU = False
                reset_game() # Garante que o jogo comece do zero
        else:
            if not PAUSE_MENU and SNAKE_GAME_STATE['countdown'] <= 0 and not SNAKE_GAME_STATE['end_game']:
                update_snake_position()
                snake_get_apple() # Verifica a maçã após o movimento
                check_end_game() # Verifica fim de jogo após o movimento

            # Sempre desenha o mapa e a pontuação, independentemente do estado de pause/countdown
            clear_map()
            add_snake_position_to_map()
            add_apple_position_to_map()
            draw_map_elements()
            draw_score()


            if not PAUSE_MENU and SNAKE_GAME_STATE['countdown'] > 0 and not SNAKE_GAME_STATE['end_game']:
                game_start_countdown()

            if SNAKE_GAME_STATE['end_game']:
                draw_end_game()

            # Menu de pause
            if PAUSE_MENU:
                # O contador deve ser 3 no menu de pause, para quando voltar ao jogo ele recomeçar a contagem
                SNAKE_GAME_STATE['countdown'] = 3
                button_action = pause_screen([('Home Menu', 'green'), ('Restart', 'blue light 2'), ('Quit Game', 'red')], button_layout=(3, 3))

                if button_action == 'Home Menu':
                    PAUSE_MENU = False
                    HOME_MENU = True
                    reset_game()
                elif button_action == 'Restart':
                    PAUSE_MENU = False
                    reset_game()
                elif button_action == 'Quit Game':
                    pg.quit()
                    quit()

        pg.display.update()
        # O FPS do jogo normal é 30, mas na animação da tela inicial é menor
        if not HOME_MENU and not PAUSE_MENU and SNAKE_GAME_STATE['countdown'] <= 0 and not SNAKE_GAME_STATE['end_game']:
            set_fps(30)
        elif HOME_MENU:
            set_fps(10) # Animação mais lenta para a tela inicial
        else: # Tela de pause, fim de jogo ou countdown
            set_fps(60) # Ou um FPS alto para que os menus respondam rapidamente
            pass # Sem movimento da cobra nessas telas

if __name__ == '__main__':
    run_game()