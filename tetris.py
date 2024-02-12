import pygame
import random

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ajout de plusieurs couleurs
COLORS = [
    (255, 0, 0),    # Rouge
    (0, 255, 0),    # Vert
    (0, 0, 255),    # Bleu
    (255, 255, 0),  # Jaune
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

# Définition des formes des blocs
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[4, 4, 0],
     [0, 4, 4]],

    [[5, 5, 5, 5]],

    [[6, 6, 6],
     [0, 0, 6]],

    [[7, 7, 7],
     [7, 0, 0]],
]


# Classe pour représenter les blocs
class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(shapes)
        self.color = random.choice(COLORS)  # Choix aléatoire de couleur

    def draw(self, surface):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] != 0:
                    pygame.draw.rect(surface, self.color, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, BLACK, (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Classe principale du jeu
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        return Piece(GRID_WIDTH // 2 - 2, 0)

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.piece.draw(self.screen)
        pygame.display.update()

    def check_collision(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape[i])):
                if self.piece.shape[i][j] != 0:
                    if i + self.piece.y >= GRID_HEIGHT or \
                       j + self.piece.x < 0 or j + self.piece.x >= GRID_WIDTH or \
                       self.grid[i + self.piece.y][j + self.piece.x] != 0:
                        return True
        return False

    def merge_piece(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape[i])):
                if self.piece.shape[i][j] != 0:
                    self.grid[i + self.piece.y][j + self.piece.x] = self.piece.color

    def remove_full_rows(self):
        rows_to_remove = []
        for i in range(len(self.grid)):
            if all(cell != 0 for cell in self.grid[i]):
                rows_to_remove.append(i)
                self.score += 1
        for row in rows_to_remove:
            del self.grid[row]
            self.grid.insert(0, [0] * GRID_WIDTH)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.piece.move(-1, 0)
                        if self.check_collision():
                            self.piece.move(1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.piece.move(1, 0)
                        if self.check_collision():
                            self.piece.move(-1, 0)
                    if event.key == pygame.K_DOWN:
                        self.piece.move(0, 1)
                        if self.check_collision():
                            self.piece.move(0, -1)
                    if event.key == pygame.K_UP:
                        self.piece.rotate()
                        if self.check_collision():
                            self.piece.rotate()

            self.piece.move(0, 1)
            if self.check_collision():
                self.piece.move(0, -1)
                self.merge_piece()
                self.remove_full_rows()
                self.piece = self.new_piece()
                if self.check_collision():
                    self.game_over = True

            self.draw()
            self.clock.tick(5)

# Lancement du jeu
if __name__ == '__main__':
    pygame.init()
    game = Tetris()
    game.run()