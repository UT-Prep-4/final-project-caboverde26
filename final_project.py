import pygame
import random

pygame.init()

TILE_SIZE = 20
COLS, ROWS = 72, 35  
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def generate_maze(cols, rows):
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    visited = set()
    def carve_path(cx, cy):
        visited.add((cx, cy))
        grid[cy][cx] = 0
        
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < cols - 1 and 0 < ny < rows - 1 and (nx, ny) not in visited:
                grid[cy + dy//2][cx + dx//2] = 0
                carve_path(nx, ny)

    carve_path(1, 1)
    
    grid[rows - 2][1] = 0 
    grid[1][cols - 2] = 0 
    
    return grid

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("white") 
        pygame.draw.rect(self.image, (35, 45, 60), (0, 0, size, size), 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((46, 204, 113)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size - 8, size - 8)) 
        self.image.fill("red") 
        self.rect = self.image.get_rect()
        self.rect.x = x + 100
        self.rect.y = y + 100
        self.speed = 20

    def move(self, dx, dy, walls_group):
        self.rect.x += dx
        hit_list = pygame.sprite.spritecollide(self, walls_group, False)
        for wall in hit_list:
            if dx > 0: self.rect.right = wall.rect.left
            if dx < 0: self.rect.left = wall.rect.right
        self.rect.y += dy
        hit_list = pygame.sprite.spritecollide(self, walls_group, False)
        for wall in hit_list:
            if dy > 0: self.rect.bottom = wall.rect.top
            if dy < 0: self.rect.top = wall.rect.bottom

all_sprites = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

SPAWN_X, SPAWN_Y = 1 * TILE_SIZE, (ROWS - 2) * TILE_SIZE
GOAL_X, GOAL_Y = (COLS - 2) * TILE_SIZE, 1 * TILE_SIZE

player = Player(SPAWN_X, SPAWN_Y, TILE_SIZE)
goal = Goal(GOAL_X, GOAL_Y, TILE_SIZE)

def build_new_level():
    all_sprites.empty()
    walls_group.empty()
    
    maze_layout = generate_maze(COLS, ROWS)
    
    for r_idx, row in enumerate(maze_layout):
        for c_idx, cell in enumerate(row):
            if cell == 1:
                wall = Wall(c_idx * TILE_SIZE, r_idx * TILE_SIZE, TILE_SIZE)
                walls_group.add(wall)
                all_sprites.add(wall)
                
    all_sprites.add(goal)
    all_sprites.add(player)
    
    player.rect.x = SPAWN_X + 4
    player.rect.y = SPAWN_Y + 4

build_new_level()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  
        dx = -player.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
        dx = player.speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:    
        dy = -player.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:  
        dy = player.speed

    if dx != 0 or dy != 0:
        player.move(dx, dy, walls_group)

    if pygame.sprite.collide_rect(player, goal):
        build_new_level() 

    screen.fill("black") 
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
