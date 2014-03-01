import Tkinter, turtle, random, time
root = Tkinter.Tk()
root.title("Pong")
screen_w = 700
screen_h = 500
left_x = -screen_w / 2 + 4
right_x = screen_w / 2 - 11
shot_vx = 20
ball_vx = 10
min_ball_vy = 1
max_ball_vy = 15
left_score_x = -screen_w / 2 + 14
right_score_x = screen_w / 2 - 29
score_y = screen_h / 2 - 30
score_font = ('Arial', 16, 'normal')
cv = turtle.ScrolledCanvas(root, screen_w, screen_h)
cv.pack()
screen = turtle.TurtleScreen(cv)

class Ball(turtle.RawTurtle):
  def __init__(self, canvas):
    turtle.RawTurtle.__init__(self, canvas)
    self.hideturtle()
    self.penup()
    self.color('red')
    for i in range(24):
      self.getscreen().register_shape('hface/hface' + str(i) + '.gif')
    self.shape('hface/hface0.gif')
    self.snum = 0
    self.sdir = 1
    self.r = 30
    self.x = 0
    self.y = 0
    self.vx = 0
    self.vy = 0
    self.setpos(self.x, self.y)
    self.showturtle()

  def move(self):
    self.snum = (self.snum + self.sdir) % 24
    self.x += self.vx
    self.y += self.vy
    self.shape('hface/hface' + str(self.snum) + '.gif')
    self.setpos(self.x, self.y)

class Player(turtle.RawTurtle):
  def __init__(self, canvas, x):
    turtle.RawTurtle.__init__(self, canvas)
    self.hideturtle()
    self.penup()
    self.shape('square')
    self.shapesize(5, .5)
    self.x = x
    self.y = 0
    self.w = 10
    self.h = 100
    self.vy = 0
    self.setpos(self.x, self.y)
    self.showturtle()

  def move(self):
    self.y += self.vy
    if self.y > screen_h / 2 - self.h / 2:
      self.y = screen_h / 2 - self.h / 2
    if self.y < -screen_h / 2 + self.h / 2:
      self.y = -screen_h / 2 + self.h / 2
    self.setpos(self.x, self.y)

class Bullet(turtle.RawTurtle):
  def __init__(self, canvas, x, y, vx):
    turtle.RawTurtle.__init__(self, canvas)
    self.hideturtle()
    self.penup()
    self.shape('triangle')
    self.x = x
    self.y = y
    self.vx = vx
    self.setpos(self.x, self.y)
    self.setheading(90 if vx > 0 else 270)
    self.showturtle()

  def move(self):
    self.x += self.vx
    self.setpos(self.x, self.y)

# Setup game
left_score = 0
right_score = 0
bullets = []
ball = Ball(cv)
left_p = Player(cv, left_x)
right_p = Player(cv, right_x)
scribe = turtle.RawTurtle(cv)
scribe.hideturtle()
scribe.penup()

# Define left player movement
def left_up(event):
  left_p.vy = 10
def left_down(event):
  left_p.vy = -10
def left_stop(event):
  left_p.vy = 0
def left_shot(event):
  bullets.append(Bullet(cv, left_p.x, left_p.y, shot_vx))
root.bind('<KeyPress-w>', left_up)
root.bind('<KeyPress-s>', left_down)
# Don't allow shooting because it's too slow
# root.bind('<KeyPress-d>', left_shot)
root.bind('<KeyRelease-w>', left_stop)
root.bind('<KeyRelease-s>', left_stop)

# Define right player movement
def right_up(event):
  right_p.vy = 10
def right_down(event):
  right_p.vy = -10
def right_stop(event):
  right_p.vy = 0
def right_shot(event):
  bullets.append(Bullet(cv, right_p.x, right_p.y, -shot_vx))
root.bind('<KeyPress-i>', right_up)
root.bind('<KeyPress-k>', right_down)
# Don't allow shooting because it's too slow
root.bind('<KeyPress-j>', right_shot)
root.bind('<KeyRelease-i>', right_stop)
root.bind('<KeyRelease-k>', right_stop)

def reset_game():
  ball.x = 0
  ball.y = 0
  ball.vx = ball_vx if random.random() < .5 else -ball_vx
  ball.vy = random.randint(min_ball_vy, max_ball_vy)
  left_p.y = 0
  right_p.y = 0
  # Write scores
  scribe.clear()
  scribe.setpos(left_score_x, score_y)
  scribe.write(left_score, font = score_font)
  scribe.setpos(right_score_x, score_y)
  scribe.write(right_score, font = score_font)

reset_game()
def play():
  global left_score, right_score
  winner = 'none'
  left_p.move()
  right_p.move()
  ball.move()
  i = len(bullets) - 1
  while i >= 0:
    bullets[i].move()
    if bullets[i].x < -screen_w / 2 or bullets[i].x > screen_w / 2:
      bullets[i].clear()
      bullets[i].hideturtle()
      del bullets[i]
    i -= 1

  if ball.x + ball.r >= screen_w / 2 - right_p.w:
    if abs(ball.y - right_p.y) <= right_p.h / 2 + ball.r:
      ball.vx = -ball.vx
      if ball.vy > 0:
        ball.sdir = 1
      else:
        ball.sdir = -1
      if ball.y - right_p.y > right_p.h / 4:
        ball.vy += 10.0 * abs(ball.y - right_p.y) / right_p.h
      if ball.y - right_p.y < - right_p.h / 4:
        ball.vy -= 10.0 * abs(ball.y - right_p.y) / right_p.h
    else:
      winner = 'left'
  if ball.x - ball.r <= - screen_w / 2 + left_p.w:
    if abs(ball.y - left_p.y) <= left_p.h / 2 + ball.r:
      ball.vx = -ball.vx
      if ball.vy > 0:
        ball.sdir = -1
      else:
        ball.sdir = 1
      if ball.y - left_p.y > left_p.h / 4:
        ball.vy += 10.0 * abs(ball.y - left_p.y) / left_p.h
      if ball.y - left_p.y < - left_p.h / 4:
        ball.vy -= 10.0 * abs(ball.y - left_p.y) / left_p.h
    else:
      winner = 'right'
  if ball.y + ball.r >= screen_h / 2:
    ball.vy = -ball.vy
    if ball.vx > 0:
      ball.sdir = -1
    else:
      ball.sdir = 1
  if ball.y - ball.r <= -screen_h / 2:
    ball.vy = -ball.vy
    if ball.vx > 0:
      ball.sdir = 1
    else:
      ball.sdir = -1

  if winner == 'left':
    left_score += 1
    reset_game()
  if winner == 'right':
    right_score += 1
    reset_game()
  screen.ontimer(play, 5)

screen.ontimer(play, 5)
Tkinter.mainloop()

