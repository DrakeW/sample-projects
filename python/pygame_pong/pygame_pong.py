import sys, pygame, random, math
pygame.init()

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect().copy()
    rot_image = pygame.transform.rotate(image, angle)
    orig_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(orig_rect).copy()
    return rot_image

size = (width, height) = (640, 480)
screen = pygame.display.set_mode(size)
left_score = right_score = 0
player_v = 3
ball_sang = 6
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

class Ball():
  def __init__(self):
    w = h = 40
    self.sdir = 1
    self.ang = 0
    self.image = pygame.image.load('ball_black.gif')
    self.image = pygame.transform.scale(self.image, (w, h))
    (self.vx, self.vy) = self.gen_speed()
    self.orig_image = self.image.copy()
    self.rect = pygame.Rect(0, 0, w, h)
    self.rect.center = (width / 2, height / 2)

  def move(self):
    self.rect = self.rect.move(self.vx, self.vy)
    self.ang = (self.ang + self.sdir * ball_sang) % 360
    self.image = rot_center(self.orig_image, self.ang)

  def gen_speed(self):
    vx = -3 if random.random() < 5 else 3
    vy = random.randint(1, 5)
    return (vx, vy)

class Player():
  def __init__(self, side):
    w = 10
    h = 100
    x = 0 if side == 'left' else width - w
    y = width / 2 - h / 2
    self.side = side
    self.rect = pygame.Rect(x, y, w, h)
    self.vy = 0
    self.bulletrect = None
    self.bulletvx = 0
    self.shooting = False
    self.color = blue

  def move(self):
    if not self.shooting:
      self.rect = self.rect.move(0, self.vy)
      if self.rect.top < 0:
        self.rect.top = 0
      if self.rect.bottom > height:
        self.rect.bottom = height
    else:
      self.bulletrect = self.bulletrect.move(self.bulletvx, 0)

  def shoot(self):
    if not self.shooting:
      self.color = yellow
      self.bulletrect = pygame.Rect(0, 0, 10, 10)
      if self.side == 'left':
        self.bulletrect.midleft = self.rect.midright
        self.bulletvx = 6
      else:
        self.bulletrect.midright = self.rect.midleft
        self.bulletvx = -6
      self.shooting = True

  def end_shot(self):
    self.color = blue
    self.bulletrect = None
    self.shooting = False

left_p = Player('left')
right_p = Player('right')
ball = Ball()

def reset_game():
  left_p.rect.midleft = (0, height / 2)
  right_p.rect.midright = (width, height / 2)
  left_p.end_shot()
  right_p.end_shot()
  (ball.vx, ball.vy) = ball.gen_speed()
  ball.rect.center = (width / 2, height / 2)
  pygame.time.delay(1000)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == 119: # w
        left_p.vy = -player_v
      if event.key == 115: # s
        left_p.vy = player_v
      if event.key == 105: # i
        right_p.vy = -player_v
      if event.key == 107: # k
        right_p.vy = player_v
    elif event.type == pygame.KEYUP:
      if event.key == 119 or event.key == 115:
        left_p.vy = 0
      if event.key == 105 or event.key == 107:
        right_p.vy = 0
      if event.key == 100: # d
        left_p.shoot()
      if event.key == 106: # j
        right_p.shoot()

  left_p.move()
  right_p.move()
  ball.move()
  for p in [left_p, right_p]:
    if ball.rect.colliderect(p):
      ball.vx = -ball.vx
      ball.sdir = math.copysign(1, ball.vy * (ball.rect.left - 20))
      by = ball.rect.center[1]
      py = p.rect.center[1]
      ball.vy += (by - py) / 50.0

    if p.bulletrect != None:
      if p.bulletrect.left < 0 or p.bulletrect.right > width:
        p.end_shot()
      elif p.bulletrect.colliderect(ball):
        ball.vx += p.bulletvx
        p.end_shot()
      elif p.bulletrect.colliderect(left_p):
        right_score += 1
        reset_game()
      elif p.bulletrect.colliderect(right_p):
        left_score += 1
        reset_game()

  if ball.rect.left < 0:
    right_score += 1
    reset_game()
  if ball.rect.right > width:
    left_score += 1
    reset_game()
  if ball.rect.top < 0 or ball.rect.bottom > height:
    ball.vy = -ball.vy
    ball.sdir = math.copysign(1, -ball.vx * ball.rect.top)
    if ball.rect.top < 0:
      ball.rect.top = 0
    elif ball.rect.bottom > height:
      ball.rect.bottom = height

  screen.fill(black)
  screen.blit(ball.image, ball.rect)
  pygame.draw.rect(screen, left_p.color, left_p.rect)
  pygame.draw.rect(screen, right_p.color, right_p.rect)
  if left_p.bulletrect != None:
    pygame.draw.ellipse(screen, yellow, left_p.bulletrect)
  if right_p.bulletrect != None:
    pygame.draw.ellipse(screen, yellow, right_p.bulletrect)
  font = pygame.font.SysFont('Arial', 16)
  screen.blit(font.render(str(left_score), 1, white), (40, 20))
  screen.blit(font.render(str(right_score), 1, white), (width - 60, 20))
  pygame.display.update()
  pygame.time.delay(10)
