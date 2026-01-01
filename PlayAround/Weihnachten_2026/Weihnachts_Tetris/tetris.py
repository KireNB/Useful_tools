import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# ------------------ KONSTANTEN ------------------
CELL = 32
COLS, ROWS = 10, 15
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FPS = 60
REIHEN_ZUM_SIEG = 5  # 5 Reihen zum Sieg

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎄 Weihnachts-Tetris 🎅")

CLOCK = pygame.time.Clock()

# ------------------ ASSET-PFADE ------------------
ASSETS = "assets"
IMAGES = os.path.join(ASSETS, "images")
SOUNDS = os.path.join(ASSETS, "sounds")

# ------------------ MUSIK ------------------
pygame.mixer.music.load(os.path.join(SOUNDS, "music.mp3"))
pygame.mixer.music.play(-1)

line_clear_sound = pygame.mixer.Sound(os.path.join(SOUNDS, "line_clear.mp3"))
win_sound = pygame.mixer.Sound(os.path.join(SOUNDS, "win_sleigh.mp3"))

# ------------------ SPRITES ------------------
SANTA = pygame.image.load(os.path.join(IMAGES, "santa_block.png")).convert_alpha()
SANTA = pygame.transform.scale(SANTA, (CELL, CELL))

# Nur ein Rentier für Sieg
REINDEER = pygame.transform.scale(
    pygame.image.load(os.path.join(IMAGES, "reindeer_0.png")).convert_alpha(),
    (64, 64)
)

SLEIGH = pygame.transform.scale(
    pygame.image.load(os.path.join(IMAGES, "sleigh.png")).convert_alpha(),
    (120, 50)
)

# ------------------ FORMEN ------------------
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

# ------------------ SPIELFELD ------------------
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
lines_cleared = 0


class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))


def valid(piece, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + dx
                ny = piece.y + y + dy
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and grid[ny][nx]:
                    return False
    return True


def lock_piece(piece):
    global lines_cleared

    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = 1

    new_grid = []
    cleared_this_turn = 0

    for row in grid:
        if all(row):
            lines_cleared += 1
            cleared_this_turn += 1
        else:
            new_grid.append(row)

    if cleared_this_turn > 0:
        line_clear_sound.play()

    while len(new_grid) < ROWS:
        new_grid.insert(0, [0] * COLS)

    for i in range(ROWS):
        grid[i] = new_grid[i]


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                WIN.blit(SANTA, (x * CELL, y * CELL))


def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                WIN.blit(
                    SANTA,
                    ((piece.x + x) * CELL, (piece.y + y) * CELL)
                )


def draw_info():
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Reihen: {lines_cleared}/{REIHEN_ZUM_SIEG}", True, (255, 255, 255))
    WIN.blit(text, (10, 10))


def win_animation():
    font = pygame.font.SysFont(None, 36)  # kleinerer Text
    sled_x = WIDTH // 2 - 60
    WIN.fill((20, 120, 40))

    text = font.render("🎉 Du hast gewonnen! 🎄", True, (255, 255, 255))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

    WIN.blit(SLEIGH, (sled_x, HEIGHT // 2))
    WIN.blit(REINDEER, (sled_x + 30, HEIGHT // 2 - 20))

    pygame.display.update()
    win_sound.play()
    pygame.time.wait(4000)
    pygame.quit()
    sys.exit()


def lose_animation():
    font = pygame.font.SysFont(None, 36)
    WIN.fill((100, 0, 0))
    text = font.render("Leider verloren! :(", True, (255, 255, 255))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
    pygame.display.update()
    pygame.time.wait(4000)
    pygame.quit()
    sys.exit()


# ------------------ HAUPTSCHLEIFE ------------------
piece = Piece()
fall_timer = 0

print("Steuerung:")
print("← / → : nach links/rechts")
print("↓ : schneller fallen")
print("↑ : Figur drehen")

while True:
    WIN.fill((0, 0, 0))
    fall_timer += CLOCK.get_time()

    if fall_timer > 500:
        if valid(piece, dy=1):
            piece.y += 1
        else:
            # Überprüfen, ob neue Figur überhaupt noch passt
            if not valid(piece):
                if lines_cleared < REIHEN_ZUM_SIEG:
                    lose_animation()
            lock_piece(piece)
            piece = Piece()
            # Prüfen auf Gewinn
            if lines_cleared >= REIHEN_ZUM_SIEG:
                win_animation()
        fall_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid(piece, dx=-1):
                piece.x -= 1
            if event.key == pygame.K_RIGHT and valid(piece, dx=1):
                piece.x += 1
            if event.key == pygame.K_DOWN and valid(piece, dy=1):
                piece.y += 1
            if event.key == pygame.K_UP:
                old = piece.shape
                piece.rotate()
                if not valid(piece):
                    piece.shape = old
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    draw_grid()
    draw_piece(piece)
    draw_info()
    pygame.display.update()
    CLOCK.tick(FPS)


# import pygame
# import random
# import sys
# import os

# pygame.init()
# pygame.mixer.init()

# # ------------------ KONSTANTEN ------------------
# CELL = 32
# COLS, ROWS = 10, 15
# WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
# FPS = 60
# REIHEN_ZUM_SIEG = 5  # jetzt 5 Reihen zum Sieg

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("🎄 Weihnachts-Tetris 🎅")

# CLOCK = pygame.time.Clock()

# # ------------------ ASSET-PFADE ------------------
# ASSETS = "assets"
# IMAGES = os.path.join(ASSETS, "images")
# SOUNDS = os.path.join(ASSETS, "sounds")

# # ------------------ MUSIK ------------------
# pygame.mixer.music.load(os.path.join(SOUNDS, "music.mp3"))
# pygame.mixer.music.play(-1)

# line_clear_sound = pygame.mixer.Sound(os.path.join(SOUNDS, "line_clear.mp3"))
# win_sound = pygame.mixer.Sound(os.path.join(SOUNDS, "win_sleigh.mp3"))

# # ------------------ SPRITES ------------------
# SANTA = pygame.image.load(os.path.join(IMAGES, "santa_block.png")).convert_alpha()
# SANTA = pygame.transform.scale(SANTA, (CELL, CELL))

# # Nur ein Rentier für die Sieg-Animation
# REINDEER = pygame.transform.scale(
#     pygame.image.load(os.path.join(IMAGES, "reindeer_0.png")).convert_alpha(),
#     (64, 64)
# )

# SLEIGH = pygame.transform.scale(
#     pygame.image.load(os.path.join(IMAGES, "sleigh.png")).convert_alpha(),
#     (120, 50)
# )

# # ------------------ FORMEN ------------------
# SHAPES = [
#     [[1, 1, 1, 1]],
#     [[1, 1], [1, 1]],
#     [[0, 1, 0], [1, 1, 1]],
#     [[1, 0, 0], [1, 1, 1]],
#     [[0, 0, 1], [1, 1, 1]],
# ]

# # ------------------ SPIELFELD ------------------
# grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
# lines_cleared = 0


# class Piece:
#     def __init__(self):
#         self.shape = random.choice(SHAPES)
#         self.x = COLS // 2 - len(self.shape[0]) // 2
#         self.y = 0

#     def rotate(self):
#         self.shape = list(zip(*self.shape[::-1]))


# def valid(piece, dx=0, dy=0):
#     for y, row in enumerate(piece.shape):
#         for x, cell in enumerate(row):
#             if cell:
#                 nx = piece.x + x + dx
#                 ny = piece.y + y + dy
#                 if nx < 0 or nx >= COLS or ny >= ROWS:
#                     return False
#                 if ny >= 0 and grid[ny][nx]:
#                     return False
#     return True


# def lock_piece(piece):
#     global lines_cleared

#     for y, row in enumerate(piece.shape):
#         for x, cell in enumerate(row):
#             if cell:
#                 grid[piece.y + y][piece.x + x] = 1

#     new_grid = []
#     cleared_this_turn = 0

#     for row in grid:
#         if all(row):
#             lines_cleared += 1
#             cleared_this_turn += 1
#         else:
#             new_grid.append(row)

#     if cleared_this_turn > 0:
#         line_clear_sound.play()

#     while len(new_grid) < ROWS:
#         new_grid.insert(0, [0] * COLS)

#     for i in range(ROWS):
#         grid[i] = new_grid[i]


# def draw_grid():
#     for y in range(ROWS):
#         for x in range(COLS):
#             if grid[y][x]:
#                 WIN.blit(SANTA, (x * CELL, y * CELL))


# def draw_piece(piece):
#     for y, row in enumerate(piece.shape):
#         for x, cell in enumerate(row):
#             if cell:
#                 WIN.blit(
#                     SANTA,
#                     ((piece.x + x) * CELL, (piece.y + y) * CELL)
#                 )


# def draw_info():
#     font = pygame.font.SysFont(None, 24)
#     text = font.render(f"Reihen: {lines_cleared}/{REIHEN_ZUM_SIEG}", True, (255, 255, 255))
#     WIN.blit(text, (10, 10))


# def win_animation():
#     font = pygame.font.SysFont(None, 36)  # kleinerer Text
#     sled_x = WIDTH // 2 - 60  # Schlitten fixiert in der Mitte
#     WIN.fill((20, 120, 40))

#     text = font.render("🎉 Du hast gewonnen! 🎄", True, (255, 255, 255))
#     WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

#     WIN.blit(SLEIGH, (sled_x, HEIGHT // 2))
#     WIN.blit(REINDEER, (sled_x + 30, HEIGHT // 2 - 20))  # nur ein Rentier

#     pygame.display.update()
#     win_sound.play()
#     pygame.time.wait(4000)
#     pygame.quit()
#     sys.exit()


# # ------------------ HAUPTSCHLEIFE ------------------
# piece = Piece()
# fall_timer = 0

# print("Steuerung:")
# print("← / → : nach links/rechts")
# print("↓ : schneller fallen")
# print("↑ : Figur drehen")

# while True:
#     WIN.fill((0, 0, 0))
#     fall_timer += CLOCK.get_time()

#     if fall_timer > 500:
#         if valid(piece, dy=1):
#             piece.y += 1
#         else:
#             lock_piece(piece)
#             piece = Piece()
#             if lines_cleared >= REIHEN_ZUM_SIEG:
#                 win_animation()
#         fall_timer = 0

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT and valid(piece, dx=-1):
#                 piece.x -= 1
#             if event.key == pygame.K_RIGHT and valid(piece, dx=1):
#                 piece.x += 1
#             if event.key == pygame.K_DOWN and valid(piece, dy=1):
#                 piece.y += 1
#             if event.key == pygame.K_UP:
#                 old = piece.shape
#                 piece.rotate()
#                 if not valid(piece):
#                     piece.shape = old
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()

#     draw_grid()
#     draw_piece(piece)
#     draw_info()
#     pygame.display.update()
#     CLOCK.tick(FPS)
