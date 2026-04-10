import pygame
import sys
import random

# --- CONSTANTS ---
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20

# Directions
UP = (0, -BLOCK_SIZE)
DOWN = (0, BLOCK_SIZE)
LEFT = (-BLOCK_SIZE, 0)
RIGHT = (BLOCK_SIZE, 0)

# Game states
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAMEOVER = "GAMEOVER"

# Menu and speed settings
MENU_OPTIONS = ["START GAME", "QUIT"]
SPEED_OPTIONS = [("Slow", 8), ("Normal", 12), ("Fast", 16)]

# Colors
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_SNAKE = (50, 200, 50)
COLOR_HEAD = (50, 255, 50)
COLOR_FOOD = (200, 50, 50)
COLOR_TEXT = (255, 255, 255)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake : Moe Htet PRO Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_main = pygame.font.SysFont("arial", 25)
        self.font_title = pygame.font.SysFont("arial", 50, bold=True)
        
        self.state = STATE_MENU
        self.menu_index = 0
        self.settings_index = 1
        self.base_speed = SPEED_OPTIONS[self.settings_index][1]
        
        self.direction_lock = False # Prevents multiple turns in one frame
        self.reset_game()

    def reset_game(self):
        self.snake_body = [[100, 100], [80, 100], [60, 100]]
        self.direction = RIGHT
        self.score = 0
        self.current_speed = self.base_speed
        self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            self.food_pos = [x, y]
            # Ensure food doesn't spawn inside the snake
            if self.food_pos not in self.snake_body:
                break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.KEYDOWN:
                # Global Toggle for Pause and Menu Return
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING: 
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED: 
                        self.state = STATE_PLAYING
                    elif self.state == STATE_GAMEOVER:
                        self.state = STATE_MENU

                if self.state == STATE_MENU:
                    if event.key == pygame.K_UP: 
                        self.menu_index = (self.menu_index - 1) % len(MENU_OPTIONS)
                    elif event.key == pygame.K_DOWN: 
                        self.menu_index = (self.menu_index + 1) % len(MENU_OPTIONS)
                    elif event.key == pygame.K_RETURN: 
                        self.select_menu_option()
                
                elif self.state == STATE_PLAYING and not self.direction_lock:
                    if event.key == pygame.K_UP and self.direction != DOWN: 
                        self.direction = UP
                        self.direction_lock = True
                    elif event.key == pygame.K_DOWN and self.direction != UP: 
                        self.direction = DOWN
                        self.direction_lock = True
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT: 
                        self.direction = LEFT
                        self.direction_lock = True
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT: 
                        self.direction = RIGHT
                        self.direction_lock = True

    def select_menu_option(self):
        selection = MENU_OPTIONS[self.menu_index]
        if selection == "START GAME":
            self.reset_game()
            self.state = STATE_PLAYING
        elif selection == "QUIT":
            self.quit_game()

    def draw_grid(self):
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WIDTH, y))

    def draw_snake(self):
        for i, segment in enumerate(self.snake_body):
            color = COLOR_HEAD if i == 0 else COLOR_SNAKE
            rect = (segment[0], segment[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            
            # Dynamic Eye Positioning
            if i == 0:
                self.draw_eyes(segment)

    def draw_eyes(self, head):
        eye_color = (0, 0, 0)
        eye_size = 3
        # Adjust eye placement based on direction
        if self.direction == RIGHT or self.direction == LEFT:
            pygame.draw.circle(self.screen, eye_color, (head[0]+10, head[1]+6), eye_size)
            pygame.draw.circle(self.screen, eye_color, (head[0]+10, head[1]+14), eye_size)
        else: # UP or DOWN
            pygame.draw.circle(self.screen, eye_color, (head[0]+6, head[1]+10), eye_size)
            pygame.draw.circle(self.screen, eye_color, (head[0]+14, head[1]+10), eye_size)

    def update(self):
        if self.state == STATE_PLAYING:
            self.direction_lock = False # Reset lock after movement
            new_head = [self.snake_body[0][0] + self.direction[0], 
                        self.snake_body[0][1] + self.direction[1]]

            # Collision Logic
            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in self.snake_body):
                self.state = STATE_GAMEOVER
                return

            self.snake_body.insert(0, new_head)
            
            # Eating Logic
            if self.snake_body[0] == self.food_pos:
                self.score += 10
                if self.score % 30 == 0:
                    self.current_speed += 1
                self.spawn_food()
            else:
                self.snake_body.pop()

    def draw_overlay(self, text, subtext=""):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))
        
        main_surf = self.font_title.render(text, True, COLOR_TEXT)
        self.screen.blit(main_surf, (WIDTH//2 - main_surf.get_width()//2, HEIGHT//2 - 40))
        
        if subtext:
            sub_surf = self.font_main.render(subtext, True, (200, 200, 200))
            self.screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 30))

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_grid()
        
        if self.state == STATE_MENU:
            self.draw_overlay("SNAKE PRO", "Use Arrows & Enter to Start")
        
        elif self.state in [STATE_PLAYING, STATE_PAUSED, STATE_GAMEOVER]:
            # Draw Food
            pygame.draw.rect(self.screen, COLOR_FOOD, (self.food_pos[0], self.food_pos[1], BLOCK_SIZE-2, BLOCK_SIZE-2), border_radius=8)
            self.draw_snake()
            
            # Score UI
            score_surf = self.font_main.render(f"Score: {self.score} | Speed: {self.current_speed}", True, COLOR_TEXT)
            self.screen.blit(score_surf, (10, 10))

            if self.state == STATE_PAUSED:
                self.draw_overlay("PAUSED", "Press 'P' to Resume")
            elif self.state == STATE_GAMEOVER:
                self.draw_overlay("GAME OVER", f"Score: {self.score} | ESC for Menu")

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.current_speed)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()