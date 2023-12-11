import pygame
import sys
import random
import pygame_menu

# Definir constantes
WINDOW_SIZE = 15
CELL_SIZE = 50
WIDTH = WINDOW_SIZE * CELL_SIZE
HEIGHT = WINDOW_SIZE * CELL_SIZE
FPS = 10

# Definir colores
WHITE = (255, 255, 255)
BLACK = (255, 255, 255) # quería que el fondo fuera blanco al final

# Función para establecer la dificultad
def set_difficulty(value, difficulty):
    global FPS
    if difficulty == 'Fácil':
        FPS = 10
    elif difficulty == 'Intermedio':
        FPS = 20
    elif difficulty == 'Difícil':
        FPS = 30

# Función principal para ejecutar el juego
def start_the_game():
    global running, in_menu
    running = True
    in_menu = False

def show_winner_menu():
    menu = pygame_menu.Menu('¡Ganaste!', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Salir', sys.exit)
    menu.mainloop(screen)

# Definir clases
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "images/personaje.png")
        self.bombs = pygame.sprite.Group()

class Bomb(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "images/bomba.png")
        self.explosion_images = [
            pygame.image.load(f"images/explosion_{i}.png") for i in range(6)
        ]
        self.explosion_index = 0
        self.exploding = False
        self.explosion_timer = 3 * FPS  # 3 segundos

class Wall(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "images/pared.png")

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "images/enemigo.png")

class Treasure(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "images/tesoro.png")

class Block(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "images/bloque.png")

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Crear menú principal
menu = pygame_menu.Menu('Bienvenido', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

# Agregar elementos al menú principal
menu.add.text_input('Nombre: ', default='Jugador')
menu.add.selector('Dificultad: ', [('Fácil', 'Fácil'), ('Intermedio', 'Intermedio'), ('Difícil', 'Difícil')],
                   onchange=set_difficulty)
menu.add.button('Comenzar', start_the_game)
menu.add.button('Salir', pygame_menu.events.EXIT)

in_menu = True

# Funciones auxiliares
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def load_level(level):
    walls = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    treasures = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    for row_index, row in enumerate(level):
        for col_index, cell in enumerate(row):
            x = col_index * CELL_SIZE
            y = row_index * CELL_SIZE

            if cell == 1:
                blocks.add(Block(x, y))
            elif cell == 2:
                walls.add(Wall(x, y))
            elif cell == 3:
                enemies.add(Enemy(x, y))
            elif cell == 4:
                player = Player(x, y)
            elif cell == 5:
                treasures.add(Treasure(x, y))

    return walls, blocks, treasures, enemies, player

# con esta matriz construyo el nivel 
level_matrix = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2],
    [2, 0, 2, 2, 2, 2, 0, 4, 0, 2, 2, 2, 2, 0, 2],
    [2, 3, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 2],
    [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2],
    [2, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2],
    [2, 1, 2, 1, 2, 1, 0, 1, 0, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 0, 2, 2, 0, 2, 0, 2, 2, 0, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 0, 1, 3, 1, 2, 1, 2, 1, 2],
    [2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2],
    [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2],
    [2, 0, 2, 1, 2, 1, 2, 5, 2, 1, 2, 1, 2, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]

walls, blocks, treasures, enemies, player = load_level(level_matrix)

# Bucle principal
running = True
while running:

    pygame.event.pump()  # Agrega esta línea para procesar eventos internos

    if in_menu:
        menu_events = menu.get_input_data()
        menu.update(pygame.event.get())
        menu.draw(screen)

        if menu.is_enabled() and 'Comenzar' in menu_events and menu_events['Comenzar']:
            start_the_game()
            in_menu = False
    else:
        keys = pygame.key.get_pressed()
        # Lógica de movimiento del enemigo
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, player):
                running = False
            # Generar movimiento aleatorio
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

            # Calcular nueva posición tentativa
            new_x, new_y = enemy.rect.x, enemy.rect.y
            if direction == "UP" and enemy.rect.y > 0:
                new_y -= CELL_SIZE
            elif direction == "DOWN" and enemy.rect.y < HEIGHT - CELL_SIZE:
                new_y += CELL_SIZE
            elif direction == "LEFT" and enemy.rect.x > 0:
                new_x -= CELL_SIZE
            elif direction == "RIGHT" and enemy.rect.x < WIDTH - CELL_SIZE:
                new_x += CELL_SIZE

            # Verificar si la nueva posición es un espacio vacío y no hay colisión con bloques
            is_empty_space = all(sprite.rect.collidepoint(new_x, new_y) == False for sprite in walls) and all(sprite.rect.collidepoint(new_x, new_y) == False for sprite in blocks)

            # Actualizar posición del enemigo si es un espacio vacío
            if is_empty_space:
                enemy.rect.x, enemy.rect.y = new_x, new_y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Lógica de movimiento del personaje
        new_x, new_y = player.rect.x, player.rect.y
        if keys[pygame.K_LEFT] and player.rect.x > 0:
            new_x -= CELL_SIZE
        elif keys[pygame.K_RIGHT] and player.rect.x < WIDTH - CELL_SIZE:
            new_x += CELL_SIZE
        elif keys[pygame.K_UP] and player.rect.y > 0:
            new_y -= CELL_SIZE
        elif keys[pygame.K_DOWN] and player.rect.y < HEIGHT - CELL_SIZE:
            new_y += CELL_SIZE

        
        # Verificar colisión con paredes y bloques
        collides_with_walls = any(sprite.rect.collidepoint(new_x, new_y) for sprite in walls)
        collides_with_blocks = any(sprite.rect.collidepoint(new_x, new_y) for sprite in blocks)

        # Actualizar posición del personaje si no colisiona con paredes ni bloques
        if not collides_with_walls and not collides_with_blocks:
            player.rect.x, player.rect.y = new_x, new_y

        if pygame.sprite.spritecollide(player, treasures, False):
            # Mostrar menú emergente
            show_winner_menu()

            # Salir del bucle principal
            running = False

        # Lógica para colocar bombas
        if keys[pygame.K_SPACE]:
            bomb = Bomb(player.rect.x, player.rect.y)
            player.bombs.add(bomb)

        # Lógica de explosión de bombas
        for bomb in player.bombs.copy():
            if not bomb.exploding:
                bomb.explosion_timer -= 1
                if bomb.explosion_timer <= 0:
                    bomb.exploding = True
                    explosion_cells = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]  # Celdas adyacentes
                    for cell in explosion_cells:
                        explosion_x = bomb.rect.x + cell[0] * CELL_SIZE
                        explosion_y = bomb.rect.y + cell[1] * CELL_SIZE

                        walls_hit = pygame.sprite.spritecollide(
                            Wall(explosion_x, explosion_y), walls, False
                        )
                        enemies_hit = pygame.sprite.spritecollide(
                            Enemy(explosion_x, explosion_y), enemies, False
                        )
                        player_hit = pygame.sprite.spritecollide(
                            Player(explosion_x, explosion_y), pygame.sprite.Group(player), False
                        )

                        for wall in walls_hit:
                            walls.remove(wall)

                        for enemy in enemies_hit:
                            enemies.remove(enemy)

                        for player_hit in player_hit:
                            running = False  # El jugador fue alcanzado por una bomba, terminar el juego

        screen.fill(BLACK)
        draw_grid()

        # Actualizar y dibujar sprites
        walls.draw(screen)
        blocks.draw(screen)
        treasures.draw(screen)
        enemies.draw(screen)
        player.bombs.draw(screen)
        screen.blit(player.image, player.rect)

        for bomb in player.bombs.copy():
            if bomb.exploding:
                if bomb.explosion_index < len(bomb.explosion_images):
                    bomb.image = bomb.explosion_images[bomb.explosion_index]
                    bomb.explosion_index += 1
                else:
                    player.bombs.remove(bomb)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
