# ----------------------
# Noam Kofman Jan 7 2026
# ----------------------

# import the pygame module
import pygame
import random
pygame.init() 
clock = pygame.time.Clock()
background_colour = (234, 212, 252)
  
# constants 
HEIGHT = 900
WIDTH = 840
JACK_WIDTH = 400
JACK_HEIGHT = 450
LOG_WIDTH = 300
LOG_HEIGHT = 1000
BRANCH_WIDTH = 350
BRANCH_HEIGHT = 230
HIGH_SCORE_FILE = "highscore.txt"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the caption of the screen
pygame.display.set_caption('GAME')

# all the images and their mods
og_bg = pygame.image.load("woods background.jpg")
bg = pygame.transform.scale(og_bg, (WIDTH, HEIGHT))

# Load branch
og_branch = pygame.image.load("branch no bg.png")
branch = pygame.transform.scale(og_branch, (BRANCH_WIDTH, BRANCH_HEIGHT))
branch_right = pygame.transform.flip(branch, True, False)

# Load and prepare log
og_log = pygame.image.load("log no bg.png")
rotate_log = pygame.transform.rotate(og_log, 90)
log = pygame.transform.scale(rotate_log, (LOG_WIDTH, LOG_HEIGHT))

# animation loop
sprite_frames_right = []
sprite_frames_left = []
for i in range(4):
    frame = pygame.image.load(f"tile00{i}.png")
    frame_right = pygame.transform.scale(frame, (JACK_WIDTH, JACK_HEIGHT))
    frame_left = pygame.transform.flip(frame_right, True, False)
    sprite_frames_right.append(frame_right)
    sprite_frames_left.append(frame_left)

# variable to track direction
sprite_facing_right = False
sprite_frame_index = 0
sprite_frame_counter = 0
sprite_animation_speed = 15  # Higher = slower animation

score = 0
# 1. Define the box (rectangle)
# Arguments: (x position, y position, width, height)
box_rect = pygame.Rect(0, 0, 250, 100)

# 2. Prepare the text
big_font = pygame.font.SysFont('freesansbold', 90)
small_font = pygame.font.SysFont('freesansbold', 40)
text_content = "Score: " + str(score)

def display_score(screen, score_value, x, y):
    """Display score on screen with background box."""
    # Draw background box
    box_rect = pygame.Rect(0, 0, 275, 100)
    pygame.draw.rect(screen, BLUE, box_rect)
    # Draw score text
    score_text = big_font.render(f"Score: {score_value}", True, WHITE)
    screen.blit(score_text, (x, y))

def save_high_score(score):
    """Save high score to file."""
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except IOError as e:
        print(f"Error saving high score: {e}")

# game over screen function
def game_over_screen(screen):
    screen.blit(bg, (0, 0))
    over_text = big_font.render("GAME OVER", True, (BLACK))
    hint_text = small_font.render("Press R to restart  |  Close window to quit", True, (BLACK))

    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, 300))
    screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, 420))
    high_text = small_font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_text, (WIDTH//2 - high_text.get_width()//2, 480))

    pygame.display.flip()
     
class Branch:
    """A class to represent a branch obstacle in the game."""
    
    def __init__(self, branch_left_img, branch_right_img):
        """Initialize a branch with starting position."""
        self.branch_left_img = branch_left_img
        self.branch_right_img = branch_right_img
        self.possible_x = [0, 430]  # Two possible x positions
        self.y = -200  # Start above screen
        self.x = random.choice(self.possible_x)  # Random starting side
        self.img = self.branch_right_img if self.x == 430 else self.branch_left_img
    def move(self, speed):
        self.y += speed
    def reset(self):
        self.y = -200
        self.x = random.choice(self.possible_x)
        self.img = self.branch_right_img if self.x == 430 else self.branch_left_img  # Initialize branch_img
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
    def is_off_screen(self, screen_height):
        return self.y >= HEIGHT
    def collides_with(self, sprite_x, sprite_y, distance):
        return abs(sprite_x - self.x) < distance and abs(sprite_y - self.y) < distance

# create branch
branch_obj = Branch(branch, branch_right)
# coordinates
sprite_x = 430
sprite_y = 500
high_score = 0
scroll_y = 0
speed = 5
highest_score = 0

# further favlues
log_h = log.get_height()
x = WIDTH // 2 - log.get_width() // 2
animate = False
distance = 50
running = True
game_over = False

# game loop
while running:
  
# for loop through the event queue  
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # check if game over and if player clicks R to restart
            if game_over and event.key == pygame.K_r:
                # reset game
                game_over = False
                score = 0
                branch_obj.reset()
                speed = 5
                animate = False
                sprite_frame_index = 0
                sprite_frame_counter = 0
                scroll_y = 0
            # animation check
            if event.key == pygame.K_SPACE and (not game_over) and (not animate):
                animate = True
                sprite_frame_index = 0
                sprite_frame_counter = 0

        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
            
    # check for collision if so game over
    if branch_obj.collides_with(sprite_x , sprite_y, distance):
        game_over = True
        # Only save if it's a new high score
        if score > high_score:
            high_score = score
            save_high_score(score)
    # if game over display game over screen
    if game_over:
        game_over_screen(screen)
        continue
    
    keys = pygame.key.get_pressed()
    # put all images on screen
    screen.fill(background_colour)
    screen.blit(bg, (0,0))
    branch_obj.draw(screen)
    pygame.draw.rect(screen, BLUE, box_rect)
   # animation loop
    if animate:
        sprite_frame_counter += 1
        if sprite_frame_counter >= sprite_animation_speed:
            sprite_frame_counter = 0
            sprite_frame_index += 1
            if sprite_frame_index >= len(sprite_frames_right):
                sprite_frame_index = 0
                animate = False
                score += 1
    # check for flipping sprite if left or right
    if sprite_facing_right:
        screen.blit(sprite_frames_right[sprite_frame_index], (sprite_x, sprite_y))
    else:
        screen.blit(sprite_frames_left[sprite_frame_index], (sprite_x, sprite_y))  

    # Blit score
    display_score(screen, score, 0, 10)
    # make branch move according to speed
    branch_obj.move(speed)
    # move tree log 
    scroll_y -= speed
    scroll_y %= log_h  
    speed += 0.001
    
    # scroll log
    y = -scroll_y 
    while y < HEIGHT:
        screen.blit(log, (x, y))
        y += log_h
  
    # move sprite
    if keys[pygame.K_LEFT]:
         sprite_x = 20
         sprite_facing_right = True

    if keys[pygame.K_RIGHT]: 
         sprite_x = 430 
         sprite_facing_right = False 

    if branch_obj.is_off_screen(HEIGHT):
        branch_obj.reset()

    pygame.display.flip()
