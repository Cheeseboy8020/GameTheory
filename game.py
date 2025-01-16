import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800  # Increased window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Pen")

# Load images
shooter_img = pygame.image.load('p1.png')
dodger_img = pygame.image.load('p2.png')
projectile_img = pygame.image.load('projectile.png')

# Scale images (increased sizes)
shooter_img = pygame.transform.scale(shooter_img, (100, 100))
dodger_img = pygame.transform.scale(dodger_img, (100, 100))
projectile_img = pygame.transform.scale(projectile_img, (40, 40))

# Player settings
shooter_pos = [WIDTH // 2, HEIGHT - 150]
dodger_pos = [WIDTH // 2, 100]

# Projectile settings
projectile_pos = [WIDTH // 2, HEIGHT - 150]
projectile_speed = 20
projectile_direction = None
dodger_direction = None
projectile_angle = 0

# Game settings
clock = pygame.time.Clock()
dodger_moved = False
shooter_moved = False
game_started = False
message = ""
hit_probability = 0.25  # Default hit probability

# Button settings
button_font = pygame.font.Font(None, 36)
button_width, button_height = 100, 40

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = button_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    global hit_probability
                    try:
                        hit_probability = float(self.text) / 100
                    except ValueError:
                        hit_probability = 0.25
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = button_font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def update_buttons():
    global shooter_left_button, shooter_right_button, dodger_left_button, dodger_right_button, start_button, restart_button
    if not shooter_moved:
        shooter_left_button = pygame.Rect(WIDTH // 4 - 150, HEIGHT - 50, button_width, button_height)
        shooter_right_button = pygame.Rect(WIDTH // 4 + 50, HEIGHT - 50, button_width, button_height)
    elif shooter_moved and not dodger_moved:
        dodger_left_button = pygame.Rect(3 * WIDTH // 4 - 150, HEIGHT - 50, button_width, button_height)
        dodger_right_button = pygame.Rect(3 * WIDTH // 4 + 50, HEIGHT - 50, button_width, button_height)
    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40)
    restart_button = pygame.Rect(WIDTH - 150, HEIGHT - 50, 100, 40)

update_buttons()

def reset_game():
    global shooter_pos, dodger_pos, projectile_pos, projectile_direction, dodger_direction, projectile_angle
    global dodger_moved, shooter_moved, game_started, message
    shooter_pos = [WIDTH // 2, HEIGHT - 150]
    dodger_pos = [WIDTH // 2, 100]
    projectile_pos = [WIDTH // 2, HEIGHT - 150]
    projectile_direction = None
    dodger_direction = None
    projectile_angle = 0
    dodger_moved = False
    shooter_moved = False
    game_started = False
    message = ""
    update_buttons()

input_box = InputBox(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if not shooter_moved:
                if shooter_left_button.collidepoint(mouse_pos):
                    projectile_direction = "left"
                    shooter_moved = True
                    update_buttons()
                elif shooter_right_button.collidepoint(mouse_pos):
                    projectile_direction = "right"
                    shooter_moved = True
                    update_buttons()
            elif shooter_moved and not dodger_moved:
                if dodger_left_button.collidepoint(mouse_pos):
                    dodger_direction = "left"
                    dodger_moved = True
                elif dodger_right_button.collidepoint(mouse_pos):
                    dodger_direction = "right"
                    dodger_moved = True
            elif shooter_moved and dodger_moved and start_button.collidepoint(mouse_pos):
                game_started = True
                projectile_pos = [shooter_pos[0], shooter_pos[1]]
                if projectile_direction == "left":
                    projectile_angle = math.atan2(dodger_pos[1] - shooter_pos[1], dodger_pos[0] - 100 - shooter_pos[0])
                elif projectile_direction == "right":
                    if random.random() < hit_probability:
                        projectile_angle = math.atan2(dodger_pos[1] - shooter_pos[1], dodger_pos[0] + 100 - shooter_pos[0])
                    else:
                        projectile_angle = math.atan2(dodger_pos[1] - shooter_pos[1], WIDTH - shooter_pos[0])
                if dodger_direction == "left":
                    dodger_pos[0] -= 100
                elif dodger_direction == "right":
                    dodger_pos[0] += 100
            elif message and restart_button.collidepoint(mouse_pos):
                reset_game()

    if game_started:
        projectile_pos[0] += projectile_speed * math.cos(projectile_angle)
        projectile_pos[1] += projectile_speed * math.sin(projectile_angle)
        if dodger_moved:
            if dodger_pos[0] < 0:
                dodger_pos[0] = 0
            elif dodger_pos[0] > WIDTH - 100:
                dodger_pos[0] = WIDTH - 100

    screen.fill((0, 0, 0))

    screen.blit(shooter_img, shooter_pos)
    screen.blit(dodger_img, dodger_pos)
    screen.blit(projectile_img, projectile_pos)

    if not shooter_moved:
        screen.blit(button_font.render('Choose Launch Direction', True, (255, 255, 255)), (WIDTH // 2 - 100, 20))
        pygame.draw.rect(screen, (255, 0, 0), shooter_left_button)
        pygame.draw.rect(screen, (0, 255, 0), shooter_right_button)
        screen.blit(button_font.render('Left', True, (255, 255, 255)), (WIDTH // 4 - 120, HEIGHT - 40))
        screen.blit(button_font.render('Right', True, (255, 255, 255)), (WIDTH // 4 + 80, HEIGHT - 40))
    elif shooter_moved and not dodger_moved:
        screen.blit(button_font.render('Choose Move Direction', True, (255, 255, 255)), (WIDTH // 2 - 100, 20))
        pygame.draw.rect(screen, (255, 0, 0), dodger_left_button)
        pygame.draw.rect(screen, (0, 255, 0), dodger_right_button)
        screen.blit(button_font.render('Left', True, (255, 255, 255)), (3 * WIDTH // 4 - 120, HEIGHT - 40))
        screen.blit(button_font.render('Right', True, (255, 255, 255)), (3 * WIDTH // 4 + 80, HEIGHT - 40))
    elif shooter_moved and dodger_moved and not game_started and not message:
        pygame.draw.rect(screen, (0, 0, 255), start_button)
        screen.blit(button_font.render('Start', True, (255, 255, 255)), (WIDTH // 2 - 20, HEIGHT // 2 - 10))

    if not shooter_moved and not dodger_moved and not game_started:
        screen.blit(button_font.render('Set Hit Probability (%)', True, (255, 255, 255)), (WIDTH // 2 - 100, HEIGHT // 2 + 20))
        input_box.draw(screen)

    if game_started and (projectile_pos[1] <= 100 or projectile_pos[1] >= HEIGHT):
        if (dodger_pos[0] < projectile_pos[0] < dodger_pos[0] + 100 or
                dodger_pos[0] < projectile_pos[0] + 40 < dodger_pos[0] + 100):
            message = "RIP Aneesh"
        else:
            message = "Aneesh is saved!"
        game_started = False

    if message:
        screen.blit(button_font.render(message, True, (255, 255, 255)), (WIDTH // 2 - 100, HEIGHT // 2 - 10))
        pygame.draw.rect(screen, (0, 0, 255), restart_button)
        screen.blit(button_font.render('Restart', True, (255, 255, 255)), (WIDTH - 140, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()