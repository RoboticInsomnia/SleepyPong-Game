import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window dimensions and title
win_width = 500
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("SLEEPYPONG - Robotic Insomnia Co.")

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the font
pygame.font.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 8)

# Set up the ball and paddles
ball_speed = 2
ball_size = 10
ball_color = white
ball = pygame.Rect(win_width/2 - ball_size/2, win_height/2 - ball_size/2, ball_size, ball_size)
ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]

paddle_width = 10
paddle_height = 80
paddle_color = white
player_paddle = pygame.Rect(0, win_height/2 - paddle_height/2, paddle_width, paddle_height)
computer_paddle = pygame.Rect(win_width - paddle_width, win_height/2 - paddle_height/2, paddle_width, paddle_height)

# Set up the game loop
clock = pygame.time.Clock()
game_over = True
score = 0
start_time = 0

# Set up the start screen
start_text = font.render("SLEEPYPONG", True, white)
start_subtext = font.render("Press Space Bar To Start", True, white)
start_rect = start_text.get_rect(center=(win_width/2, win_height/2))
start_subrect = start_subtext.get_rect(center=(win_width/2, win_height/2 + start_text.get_height()))
end_text = font.render("Robotic Insomnia Co.", True, white)
end_rect = end_text.get_rect(center=(win_width/2, win_height/2))

def reset_game():
    global game_over, ball_speed, ball, ball_direction, player_paddle, computer_paddle, score, start_time
    game_over = False
    ball_speed = 2
    ball = pygame.Rect(win_width/2 - ball_size/2, win_height/2 - ball_size/2, ball_size, ball_size)
    ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]
    player_paddle = pygame.Rect(0, win_height/2 - paddle_height/2, paddle_width, paddle_height)
    computer_paddle = pygame.Rect(win_width - paddle_width, win_height/2 - paddle_height/2, paddle_width, paddle_height)
    score = 0
    start_time = pygame.time.get_ticks()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()

    if not game_over:
        # Move the player paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            player_paddle.move_ip(0, 5)

        # Move the computer paddle
        if ball_direction[0] > 0:
            if computer_paddle.centery < ball.centery:
                computer_paddle.move_ip(0, 5)
            elif computer_paddle.centery > ball.centery:
                computer_paddle.move_ip(0, -5)
        
        # Move the ball
        ball.move_ip(ball_speed * ball_direction[0], ball_speed * ball_direction[1])

        # Check for collisions with the walls
        if ball.top <= 0 or ball.bottom >= win_height:
            ball_direction[1] = -ball_direction[1]
        if ball.left <= 0:
            ball_direction[0] = -ball_direction[0]
        if ball.right >= win_width:
            game_over = True

        # Check for collisions with the paddles
        if ball.colliderect(player_paddle):
            ball_direction[0] = -ball_direction[0]
            ball_speed += 0.5
            score += 1
        elif ball.colliderect(computer_paddle):
            ball_direction[0] = -ball_direction[0]

        # Check if the ball was missed by the player
        if ball.left <= 0:
            game_over = True

        # Draw the game objects
        win.fill(black)
        pygame.draw.rect(win, white, player_paddle)
        pygame.draw.rect(win, white, computer_paddle)
        pygame.draw.ellipse(win, ball_color, ball)

        # Display the score and time
        time_elapsed = (pygame.time.get_ticks() - start_time) // 1000
        score_text = font.render("SCORE: " + str(score), True, white)
        time_text = font.render("TIME: " + str(time_elapsed), True, white)
        score_rect = score_text.get_rect(topright=(win_width - 10, 10))
        time_rect = time_text.get_rect(topleft=(10, 10))
        win.blit(score_text, score_rect)
        win.blit(time_text, time_rect)

    else:
        # Draw the start or end screen
        win.fill(black)
        win.blit(start_text, start_rect)
        win.blit(start_subtext, start_subrect)
        if ball.right >= win_width:
            win.blit(end_text, end_rect)
            score_text = font.render("FINAL SCORE: " + str(score), True, white)
            score_rect = score_text.get_rect(center=(win_width/2, win_height/2 + end_text.get_height()))
            win.blit(score_text, score_rect)

    # Update the display
    pygame.display.update()

    # Limit the framerate
    clock.tick(60)