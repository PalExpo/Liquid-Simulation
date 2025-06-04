import pygame
import numpy as np

# Configuration
WIDTH, HEIGHT = 800, 600
NUM_PARTICLES = 10000
PARTICLE_RADIUS = 2
GRAVITY_STRENGTH = 200
DRAG = 0.98
FPS = 60

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Optimized Fluid Simulation")
clock = pygame.time.Clock()

# Initialize particles: [x, y, vx, vy]
particles = np.empty((NUM_PARTICLES, 4), dtype=np.float32)
particles[:, 0] = np.random.rand(NUM_PARTICLES) * WIDTH   # x
particles[:, 1] = np.random.rand(NUM_PARTICLES) * HEIGHT  # y
particles[:, 2:] = 0                                       # vx, vy

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill((10, 10, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse position
    mx, my = pygame.mouse.get_pos()
    mouse_pos = np.array([mx, my], dtype=np.float32)

    # Compute direction vectors from all particles to mouse
    direction = mouse_pos - particles[:, 0:2]
    distance = np.linalg.norm(direction, axis=1).reshape(-1, 1)
    distance = np.clip(distance, 1.0, None)

    gravity = (direction / distance) * GRAVITY_STRENGTH * dt
    particles[:, 2:4] += gravity
    particles[:, 2:4] *= DRAG
    particles[:, 0:2] += particles[:, 2:4] * dt

    # Handle boundaries
    out_left = particles[:, 0] < 0
    out_right = particles[:, 0] > WIDTH
    out_top = particles[:, 1] < 0
    out_bottom = particles[:, 1] > HEIGHT

    particles[out_left, 0] = 0
    particles[out_left, 2] *= -0.7
    particles[out_right, 0] = WIDTH
    particles[out_right, 2] *= -0.7
    particles[out_top, 1] = 0
    particles[out_top, 3] *= -0.7
    particles[out_bottom, 1] = HEIGHT
    particles[out_bottom, 3] *= -0.7

    # Draw all particles using single loop
    positions = particles[:, 0:2].astype(np.int32)
    for x, y in positions:
        pygame.draw.circle(screen, (100, 180, 255), (x, y), PARTICLE_RADIUS)

    pygame.display.flip()

pygame.quit()
