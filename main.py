import pygame
from Ball import Ball
from random import randrange


WIDTH = 1920
HEIGHT = 1080
FPS = 60
GAP = 125
PADDING = 50

GRAVITY = 10

TOTAL_COUNT = 100
ELITE_COUNT = 10
ITERATIONS = 30
SPEED = 10

pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT])

timer = pygame.time.Clock()

run = True

# True=test, False=train
test = False

distance = 0

if test:
    ball = Ball(100,400,25)
    #coeficients obtained after the training session
    ball.coefs = [-11.119807132237032, 65.59023137083369, 16.204303936238958, 61.73445380949086]
else:    
    balls = [Ball(100,400,25) for _ in range(TOTAL_COUNT)]
    iters=0

walls = [(0,0), (0,0), (0,0), (0,0)]


def generate_wall():
    walls[0] = walls[1]
    walls[1] = walls[2]
    walls[2] = walls[3]
    min_dist = int(walls[2][1] + 900)
    max_dist = int(walls[2][1] + 1100)
    walls[3] = (randrange(PADDING, HEIGHT - GAP - PADDING + 1), randrange(min_dist, max_dist + 1))

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen,'green',[wall[1] - distance, 0, 50, wall[0]])
        pygame.draw.rect(screen,'green',[wall[1] - distance, wall[0] + GAP, 50, HEIGHT - wall[0]- GAP])

generate_wall(), generate_wall(), generate_wall()

while run:
    timer.tick(FPS)
    screen.fill('black')
    distance+=SPEED
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if test:
                    ball.flapp()    
            elif event.key == pygame.K_ESCAPE:
                run = False    
   
    if walls[1][1] - distance < 0:
        generate_wall()

    if test:
        if ball.check_flapp(walls[1], distance) == True:
            ball.flapp()
        ball.update()
        if ball.check_collision(walls[1], distance) == True:
            run=False
        ball.draw(screen)
    else:
        alive_balls = []
        for index, ball in enumerate(balls):
            ball.update()
            if ball.check_flapp(walls[1], distance) == True:
                ball.flapp()
            ball.draw(screen)
            if ball.check_collision(walls[1], distance) == False or len(balls) - index + len(alive_balls) <= ELITE_COUNT: 
                alive_balls.append(ball)
            

        if len(alive_balls) > ELITE_COUNT:
            balls = alive_balls
        else:
            iters+=1
            new_iter = True
            print(f"Iterations done: {iters}")
            if iters == ITERATIONS:
                print(f"The best ball has:{alive_balls[-1].coefs}")
                run=False
            else:
                #mutations and reproduction    
                balls = []
                for i in range(len(alive_balls)-1):
                    for field in range(randrange(0,4)):
                        alive_balls[i].coefs[field], alive_balls[i + 1].coefs[field] = alive_balls[i].coefs[field], alive_balls[i].coefs[field]
                
                
                for i in range(int(TOTAL_COUNT / len(alive_balls))):
                    for ball in alive_balls:
                        new_ball = Ball(100,400,25)
                        new_ball.coefs = ball.coefs.copy()
                        new_ball.mutate()
                        balls.append(new_ball)
                generate_wall()
    draw_walls()
    
    pygame.display.flip()
    
pygame.quit()