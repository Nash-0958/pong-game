import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)

# Paddle settings
paddle_width, paddle_height = 10, 100
ball_size = 20

# Paddle positions
left_paddle = pygame.Rect(30, height // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(width - 30 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball settings
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
ball_speed_x, ball_speed_y = 5, 5

# Initialize scores
left_score, right_score = 0, 0
font = pygame.font.Font(None, 74)
heading_font = pygame.font.Font(None, 50)

# Load sound effects
bounce_sound = pygame.mixer.Sound('assets/sound/bounce.mp3')
score_sound = pygame.mixer.Sound('assets/sound/score.mp3')

def draw_score():
    left_text = font.render(str(left_score), True, white)
    right_text = font.render(str(right_score), True, white)
    
    # Draw headings
    left_heading = heading_font.render("Left Player", True, white)
    right_heading = heading_font.render("Right Player", True, white)
    
    # Draw headings
    screen.blit(left_heading, (width // 4 - left_heading.get_width() // 2, 10))
    screen.blit(right_heading, (width * 3 // 4 - right_heading.get_width() // 2, 10))
    
    # Draw scores
    screen.blit(left_text, (width // 4 - left_text.get_width() // 2, 70))
    screen.blit(right_text, (width * 3 // 4 - right_text.get_width() // 2, 70))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 5
    if keys[pygame.K_s] and left_paddle.bottom < height:
        left_paddle.y += 5
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 5
    if keys[pygame.K_DOWN] and right_paddle.bottom < height:
        right_paddle.y += 5

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y = -ball_speed_y
        bounce_sound.play()  # Play bounce sound

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x
        bounce_sound.play()  # Play bounce sound

    # Ball out of bounds
    if ball.left <= 0:
        right_score += 1
        score_sound.play()  # Play score sound
        ball.x = width // 2 - ball_size // 2
        ball.y = height // 2 - ball_size // 2
        ball_speed_x = -ball_speed_x
    if ball.right >= width:
        left_score += 1
        score_sound.play()  # Play score sound
        ball.x = width // 2 - ball_size // 2
        ball.y = height // 2 - ball_size // 2
        ball_speed_x = -ball_speed_x

    # Clear the screen
    screen.fill(black)

    # Draw paddles, ball, and score
    pygame.draw.rect(screen, white, left_paddle)
    pygame.draw.rect(screen, white, right_paddle)
    pygame.draw.ellipse(screen, white, ball)
    draw_score()

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Cap the frame rate to 60 FPS
