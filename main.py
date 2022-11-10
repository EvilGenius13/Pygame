import random
import pygame
from pygame import mixer
pygame.init()
pygame.font.init()

mixer.init()
mixer.music.load('above-the-clouds.wav')
mixer.music.play()
background = pygame.image.load('bg.gif')
pygame.display.set_caption("EAT YOUR FRUIT")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
#pygame clock
clock = pygame.time.Clock()
#Screen size setup
screen = pygame.display.set_mode([500, 500])

lanes = [93, 218, 343]

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(GameObject, self).__init__()
        self.surf = pygame.image.load(image)
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect()

    def render(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.surf, (self.x, self.y))

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__(0, 0, 'player.png')
        self.dx = 0
        self.dy = 0
        self.pos_x = 1
        self.pos_y = 1
        self.reset()
    
    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1
            self.update_dx_dy()
    
    def right(self):
        if self.pos_x < len(lanes) -1:
            self.pos_x += 1
            self.update_dx_dy()
    
    def up(self):
        if self.pos_y > 0:
            self.pos_y -= 1
            self.update_dx_dy()
    
    def down(self):
        if self.pos_y < len(lanes) -1:
            self.pos_y += 1
            self.update_dx_dy()
    
    def move(self):
        self.x -= (self.x - self.dx) * 0.25
        self.y -= (self.y - self.dy) * 0.25
    
    def update_dx_dy(self):
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]

    def reset(self):
        self.x = lanes[self.pos_x]
        self.y = lanes[self.pos_y]
        self.dx = self.x
        self.dy = self.y


class Apple(GameObject):
    def __init__(self):
        x = random.choice(lanes)
        super(Apple, self).__init__(x, 0, 'apple.png')
        self.dy = (random.randint(0, 200) / 100) + 1
    
    def move(self):
        self.y += self.dy
        if self.y > 500 or self.y < -64:
            self.reset()

    def reset(self):
        direction = random.randint(1, 2)
        if direction == 1: # down
            self.x = random.choice(lanes)
            self.y = -64
            self.dx = 0
            self.dy = (random.randint(0, 200) / 100) + 1
        else:
            self.x = random.choice(lanes)
            self.y = 500
            self.dx = 0
            self.dy = ((random.randint(0, 200) / 100) + 1) * -1

class Strawberry(GameObject):
    def __init__(self):
        y = random.choice(lanes)
        super(Strawberry, self).__init__(0, y, 'strawberry.png')
        self.dx = (random.randint(0, 200) / 100) + 1
    
    def move(self):
        self.x += self.dx
        if self.x > 500 or self.x < - 64:
            self.reset()

    def reset(self):
        direction = random.randint(1, 2)
        if direction == 1 : #left
            self.x = -64
            self.y = random.choice(lanes)
            self.dx = (random.randint(0, 200) / 100) + 1
            self.dy = 0
        elif direction == 2: # right
            self.x = 500
            self.y = random.choice(lanes)
            self.dx = ((random.randint(0, 200) / 100) + 1) * -1
            self.dy = 0

class Bomb(GameObject):
    def __init__(self):
        super(Bomb,self).__init__(0, 0, 'bomb.png')
        self.dx = 0
        self.dy = 0
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x > 500 or self.x < -64 or self.y > 500 or self.y < -64:
            self.reset()
    def reset(self):
        direction = random.randint(1, 4)
        if direction == 1 : #left
            self.x = -64
            self.y = random.choice(lanes)
            self.dx = (random.randint(0, 200) / 100) + 1
            self.dy = 0
        elif direction == 2: # right
            self.x = 500
            self.y = random.choice(lanes)
            self.dx = ((random.randint(0, 200) / 100) + 1) * -1
            self.dy = 0
        elif direction == 3: # down
            self.x = random.choice(lanes)
            self.y = -64
            self.dx = 0
            self.dy = (random.randint(0, 200) / 100) + 1
        else:
            self.x = random.choice(lanes)
            self.y = 500
            self.dx = 0
            self.dy = ((random.randint(0, 200) / 100) + 1) * -1

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, x, y, score):
        super(ScoreBoard, self).__init__()
        self.score = score
        self.show_score = score
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.surf = self.font.render(f"{self.score}", False, (0, 0, 0))
        self.dx = 0
        self.dy = 0
        self.x = x
        self.y = y

    def update(self, points):
        self.score += points
    
    def move(self):
        self.x += self.dx
        self.y += self.dy

    def render(self, screen):
        if self.score < self.show_score:
            self.show_score -= 1
        elif self.score > self.show_score:
            self.show_score += 1
        self.surf = self.font.render(f"{self.show_score}", False, (0, 0, 0))
        screen.blit(self.surf, (self.x, self.y))
    
    def reset(self):
        self.score = 0

class Cloud(GameObject):
  def __init__(self):
    super(Cloud, self).__init__(0, 0, 'cloud-1.png')
    self.dx = 0
    self.reset()

  def move(self):
    self.x += self.dx
    if self.x > 500:
      self.reset()

  def get_cloud_image(self):
    return f"cloud-{random.randint(1, 3)}.png"

  def reset(self):
    self.x = -64
    self.y = random.randint(0, 500 - 64)
    self.dx = (random.randint(0, 200) / 100)
    self.surf = self.surf = pygame.image.load(self.get_cloud_image())



apple = Apple()
apple2 = Apple()
apple3 = Apple()
strawberry = Strawberry()
strawberry2 = Strawberry()
strawberry3 = Strawberry()
bomb = Bomb()
player = Player()
score = ScoreBoard(30, 30, 0)
cloud = Cloud()
cloud2 = Cloud()
cloud3 = Cloud()

all_sprites = pygame.sprite.Group()
#add sprites to group
all_sprites.add(player, bomb, score, cloud, cloud2, cloud3)
all_sprites.add(apple, apple2, apple3)
all_sprites.add(strawberry, strawberry2, strawberry3)

#fruits Group
fruit_sprites = pygame.sprite.Group()
fruit_sprites.add(apple, apple2, apple3, strawberry, strawberry2, strawberry3)


#Game Loop
running = True
while running:
    #looks for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()
    #Clear screen
    screen.fill((255, 255, 255))
    #bg
    screen.blit(background, (0, 0))
    #move and render sprites
    for entity in all_sprites:
        entity.move()
        entity.render(screen)
    
    #collisions
    fruit = pygame.sprite.spritecollideany(player, fruit_sprites)
    if fruit:
        score.update(100)
        fruit.reset()
    
    # bomb collision
    if pygame.sprite.collide_rect(player, bomb):
        running = False
    
    #Update the window
    pygame.display.flip()
    
    #tick the clock
    clock.tick(60)
   