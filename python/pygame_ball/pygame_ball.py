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
speed = [2, 2]
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
ball = pygame.image.load('ball_black.gif')
ball_w = ball_h = 40
ball_sdir = 1
ball_sang = 6
ball_ang = 0
ball = pygame.transform.scale(ball, (ball_w, ball_h))
orig_ball = ball.copy()
ballrect = pygame.Rect(0, 0, ball_w, ball_h)
ball_held = False
prev_mouse_lst = [(0, 0)]

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      ball_held = True
      prev_mouse_lst = [pygame.mouse.get_pos()]
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      ball_held = False
    elif event.type == pygame.KEYUP:
      if event.key == 273:
        ball_sang += 1
      if event.key == 274 and ball_sang > 0:
        ball_sang -= 1

  if ball_held:
    cur_mouse = pygame.mouse.get_pos()
    ballrect.center = cur_mouse
    prev_mouse_lst.append(cur_mouse)
    if len(prev_mouse_lst) > 5:
      del prev_mouse_lst[0]
    speed = [(cur_mouse[0] - prev_mouse_lst[0][0]) / 10.,
        (cur_mouse[1] - prev_mouse_lst[0][1]) / 10.]
  else:
    ballrect = ballrect.move(speed)
    ball_ang = (ball_ang + ball_sdir * ball_sang) % 360
    ball = rot_center(orig_ball, ball_ang)
    if ballrect.left < 0 or ballrect.right > width:
      speed[0] = -speed[0]
      ball_sdir = math.copysign(1, speed[1] * ballrect.left)
    if ballrect.top < 0 or ballrect.bottom > height:
      speed[1] = -speed[1]
      ball_sdir = math.copysign(1, -speed[0] * ballrect.top)

  screen.fill(black)
  screen.blit(ball, ballrect)
  pygame.display.update()
  pygame.time.delay(10)
