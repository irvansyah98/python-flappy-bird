import pygame
import sys
import random

# Global Variables
WIDTH, HEIGHT = 600, 400
bird_size = 20
bird_x = 100
bird_y = HEIGHT // 2
bird_speed = 5
gravity = 1
jump_force = 10
pipe_width = 50
pipe_height = 300
pipe_gap = 150
pipes = []
score = 0

# Colors
white = (255, 255, 255)
green = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (bird_size, bird_size))

# Load background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Function to draw the bird
def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

# Function to draw the pipes
def draw_pipe(x, height):
    pygame.draw.rect(screen, green, (x, 0, pipe_width, height))
    pygame.draw.rect(screen, green, (x, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap))

# Function to draw the background
def draw_background():
    screen.blit(background_image, (0, 0))

# Function to draw the score
def draw_text(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, (10, 10))

# Main game loop
def run_game():
    global bird_y, bird_speed, pipes, score

    clock = pygame.time.Clock()
    bird_passed_pipe = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_speed = -jump_force

        bird_speed += gravity
        bird_y += bird_speed

        # Spawn pipes every few frames
        if pygame.time.get_ticks() % 60 == 0:
            pipe_height = random.randint(50, HEIGHT - pipe_gap - 50)
            pipes.append((WIDTH, pipe_height))
            bird_passed_pipe = False

        # Update pipe positions
        pipes = [(x - 5, y) for x, y in pipes]

        # Remove pipes that have passed the screen
        pipes = [(x, y) for x, y in pipes if x > 0]

        # Check collision with pipes and update score
        for pipe_x, pipe_height in pipes:
            if (
                bird_x < pipe_x < bird_x + bird_size
                and (bird_y < pipe_height or bird_y + bird_size > pipe_height + pipe_gap)
            ):
                print("Game Over!")
                pygame.quit()
                sys.exit()

            # Jika burung berhasil melewati pipa
            if bird_x == pipe_x:
                score += 1
                bird_passed_pipe = True
                print(f"Score: {score}")

        # Check if bird reaches the bottom or top of the screen
        if bird_y > HEIGHT or bird_y < 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the background
        draw_background()

        # Draw the bird
        draw_bird(bird_x, bird_y)

        # Draw the pipes
        for pipe_x, pipe_height in pipes:
            draw_pipe(pipe_x, pipe_height)

        # Draw the score
        draw_text(score)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(30)

if __name__ == "__main__":
    run_game()
