from ppnetwork import Network
import pygame
import sys
import pickle

pygame.init()

screen = pygame.display.set_mode((500, 500))


class Player:

    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
        self.vel = 5

    def move(self):

        keys = pygame.key.get_pressed()  # This is different from event

        if keys[pygame.K_UP]:
            if self.rect.top - self.vel >= 0:
                self.y -= self.vel
            else:
                self.y = 0

        if keys[pygame.K_DOWN]:
            if self.rect.bottom + self.vel <= 500:
                self.y += self.vel
            else:
                self.bottom = 500

        self.update()

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)


ball = pygame.Rect(250, 250, 10, 10)
ball.center = 300, 250

clock = pygame.time.Clock()

ballvelx = 3
ballvely = 3


def ball_move(ball):
    global ballvelx, ballvely

    ball.x += ballvelx
    ball.y += ballvely

    if ball.left <= 0:
        ballvelx *= -1

    if ball.right >= 500:
        ballvelx *= -1

    if ball.colliderect(p1) or ball.colliderect(p2):
        ballvelx *= -1

    if ball.bottom >= 500:
        ballvely *= -1
        #ball.y = 500

    if ball.top <= 0:
        ballvely *= -1
        #ball.y = 0


text_font = pygame.font.SysFont('comicsans', 50)
n = Network()
pos = n.getP()[0]
print(pos)
#pos = int(pos[1])
p1 = Player(pos[0], pos[1], 15, 100)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    x = (p1.x, p1.y)
    p2y = n.send(x)  # problem code p1 is empty nothing to send
    print(p2y)
    p2 = Player(int(p2y[0][0]), int(p2y[0][1]), 15, 100)
    screen.fill((0, 0, 0))
    # p2.update()
    p1.move()
    p1.draw()
    p2.draw()  # No movement is required as p2 Rect is constantly being updated
    # if p2y[1] == 1:
    # ball_move(ball)  # if moved second player move ball
    pygame.draw.rect(screen, (255, 255, 255), p2y[2])
    p1t = text_font.render(str(p2y[1][0]), True, (255, 255, 255))
    p2t = text_font.render(str(p2y[1][1]), True, (255, 255, 255))
    p1tt = p1t.get_rect(center=(50, 50))
    p2tt = p2t.get_rect(center=(450, 50))
    screen.blit(p1t, p1tt)
    screen.blit(p2t, p2tt)
    pygame.display.update()
