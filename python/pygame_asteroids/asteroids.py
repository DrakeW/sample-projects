import sys, pygame, random, math
pygame.init()

size = (width, height) = (640, 480)
black = (0, 0, 0)
white = (255, 255, 255)
ship_accel = .1
ship_turndeg = 3

def rot_center(image, angle, rect):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect().copy()
    rot_rect.center = rect.center
    return rot_image, rot_rect

class Ship():
  def __init__(self):
    self.w = self.h = 50
    self.image = pygame.image.load('img/ship_blast.png')
    self.image = pygame.transform.scale(self.image, (self.w, self.h))
    self.orig_image = self.image
    self.rect = pygame.Rect(0, 0, self.w, self.h)
    self.rect.center = (width / 2, height / 2)
    self.vx = self.vy = 0
    self.accel = self.turnv = 0
    self.dir = 0

  def move(self):
    self.rect = self.rect.move(round(self.vx), round(self.vy))
    if self.rect.right < 0:
      self.rect = self.rect.move(width + self.w, 0)
    if self.rect.left > width:
      self.rect = self.rect.move(-width - self.w, 0)
    if self.rect.bottom < 0:
      self.rect = self.rect.move(0, height + self.h)
    if self.rect.top > height:
      self.rect = self.rect.move(0, -height - self.h)

    ship.vx += ship.accel * math.cos(math.radians(ship.dir))
    ship.vy += ship.accel * math.sin(math.radians(ship.dir))
    ship.dir += ship.turnv

    self.image, self.rect = rot_center(self.orig_image, -self.dir, self.rect)

class Asteroid():
  def __init__(self):
    self.w = self.h = 50
    self.image = pygame.image.load('img/asteroid_cropped.jpg')
    self.image = pygame.transform.scale(self.image, (self.w, self.h))
    self.rect = pygame.Rect(0, 0, self.w, self.h)
    self.vx = self.vy = 2

  def move(self):
    self.rect = self.rect.move(round(self.vx), round(self.vy))
    if self.rect.right < 0:
      self.rect = self.rect.move(width + self.w, 0)
    if self.rect.left > width:
      self.rect = self.rect.move(-width - self.w, 0)
    if self.rect.bottom < 0:
      self.rect = self.rect.move(0, height + self.h)
    if self.rect.top > height:
      self.rect = self.rect.move(0, -height - self.h)

screen = pygame.display.set_mode(size)
ship = Ship()
asteroids = [Asteroid()]

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == 273:
        # Up arrow
        ship.accel = ship_accel
      elif event.key == 275:
        # Right arrow
        ship.turnv = ship_turndeg
      elif event.key == 276:
        # Left arrow
        ship.turnv = -ship_turndeg
    elif event.type == pygame.KEYUP:
      if event.key == 273:
        # Up arrow
        ship.accel = 0
      elif event.key == 275 or event.key == 276:
        # Right arrow or Left arrow
        ship.turnv = 0

  ship.move()
  for asteroid in asteroids:
    asteroid.move()

  screen.fill(black)
  screen.blit(ship.image, ship.rect)
  for asteroid in asteroids:
    screen.blit(asteroid.image, asteroid.rect)
  pygame.display.update()
  pygame.time.delay(10)
