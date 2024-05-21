from tkinter import *
import math
import time
from random import choice
import random
from random import randint
import threading
root = Tk()
fr = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)
p = 0
def scetch():
    global p
    p += 1
class ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['black','blue'])
        if p % 2 == 1:
            self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                                       fill=self.color)
        else:
            self.id = canv.create_rectangle(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                                            fill=self.color)
        self.live = 30
    def set_coords(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
    def move(self):
        if self.y <= 500:
            self.vy -= 1.2
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            self.set_coords()
        else:
            if self.vx ** 2 + self.vy ** 2 > 10:
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499
            if self.live < 0:
                balls.pop(balls.index(self))
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779

    def hittest(self, ob):
        if abs(ob.x - self.x) <= (self.r + ob.r) and abs(ob.y - self.y) <= (self.r + ob.r):
            return True
        else:
            return False


class gun():
    def __init__(self, x, y, vy):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.y = y
        self.x = x
        self.vy = vy
        self.r = 7
        self.id = canv.create_line(self.x, self.y, self.x + 30, self.y - 30, width=self.r)


    def fire2_start(self, event):
        self.f2_on = 1

    def move1(self, event):
        if self.y < 490:
            self.y += self.vy

    def move2(self, event):
        if self.y > 0:
            self.y -= self.vy
    def move3(self):
        self.y += self.vy
        if self.y >= 600 or self.y <= 0:
            self.vy = -self.vy

    def fire2_end(self, event):
        global balls, bullet_1
        bullet_1 += 1
        new_ball = ball(self.x, self.y + 30)
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, self.y + 30, 20 + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + 30 + max(self.f2_power, 20) * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def hit(self):
        canv.coords(self.id, -10, -10, -10, -10)


class bomb():
    def __init__(self, y=10, x=780):
        self.x = x
        self.y = y
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()
        self.live = 1

    def new_target(self):
        x = self.x = randint(300, 400)
        y = self.y = randint(200, 250)
        r = self.r = 10
        self.vx = 0.3
        self.vy = randint(5, 10)

        color = self.color = 'grey'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self):
        canv.coords(self.id, -10, -10, -10, -10)

    def move(self):
        self.set_coords()
        self.x += self.vx
        self.y += self.vy
        if self.y >= 580 or self.y <= 0:
            self.vy = -self.vy
        if self.x >= 780 or self.x <= 0:
            self.vx = -self.vx

    def set_coords(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)


class target():
    def __init__(self):
        self.points = 0
        self.id = canv.create_oval(0, 0, 0, 0)
        self.vy = 0.3
        self.vx = 0.3
        self.new_target()
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)

    def new_target(self):
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        color = self.color = 'red'
        canv.itemconfig(self.id, fill=color)
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def hit(self, points=1):
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points

    def move1(self):
        if self.y <= 500:
            self.vy -= 1.2
            self.y -= self.vy
            self.x += self.vx
            self.vx *= randint(-5, 5) / 2
        else:
            if self.vx ** 2 + self.vy ** 2 > 10:
                self.vy = -self.vy
                self.vx = self.vx / 2
                self.y -= self.vy
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def move2(self):
        self.vx = 0.4
        self.vy = 0.3
        if self.y >= 0:
            self.vy = -self.vy
        if self.y >= 580:
            self.vy = -self.vy
        if self.x >= 600:
            self.vx = -self.vx
        if self.x <= 300:
            self.vx = -self.vx
        else:
            self.y += self.vy
            self.x += self.vx
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
class Enemy(gun):
    def __init__(self):
        self.x=600
        self.f2_power = 40
        self.f2_on = 0
        self.an = 1
        self.y = random.randint(100,500)
        self.id = canv.create_line(self.x, self.y, self.x-30, self.y, width=7)
        canv.itemconfig(self.id, fill='grey')
        self.vy=5
    def scope(self):
         canv.coords(self.id,self.x, self.y, self.x-30, self.y)
    def move(self):
        self.y+=self.vy
        self.scope()
        if self.y>=490 or self.y<=0:
            self.vy=-self.vy
    def fire(self,event):
        global balls
        new_ball = ball(self.x-30,self.y)
        new_ball.r += 5
        new_ball.vx = -self.f2_power
        new_ball.vy = -self.f2_power
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 80
    def fire2_start(self, event):
        self.f2_on = 1

    def targetting(self, event=0):
        if self.f2_on:
            canv.itemconfig(self.id, fill='yellow')
        else:
            canv.itemconfig(self.id, fill='yellow')
        canv.coords(self.id, self.x, self.y, self.x + max(self.f2_power, self.x),
                    self.y + max(self.f2_power, self.x))
t1 = target()
t2 = target()
t1.id_points = canv.create_text(30, 30, text=t1.points, font='28')
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun(30, 45, 10)
bullet = 0
balls = []
bo1 = bomb()
eg =Enemy()
eg_balls = []
eg_bullet = 0


def new_game(event=''):
    global gun, t1, screen1, balls,bullet_1, t2, bomb,eg_balls,eg_bullet,balls_1,bullet
    t1.new_target()
    t2.new_target()
    bo1.new_target()
    bullet_1 = 0
    bullet=0
    balls = []
    balls_1=[]
    eg_bullet = 0
    eg_balls = []
    root.bind('<space>', lambda event: scetch())
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Button-3>',eg.fire)
    canv.bind('<Down>', g1.move1)
    canv.bind('<Up>', g1.move2)
    t2.live = 1
    t1.live = 1
    bo1.live = 1
    g1.live=1
    while t1.live  or t2.live and bo1.live or  balls  :
        eg.move()

        if bo1.live:
            bo1.move()
        if t1.live != 0:
            t1.move1()
        if t2.live != 0:
            t2.move2()
        for b in balls:
            b.move()
            if b.hittest(g1) and g1.live:
                g1.live=0
                g1.hit()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                canv.itemconfig(t1.id_points, text=t2.points + t1.points)
            if b.hittest(bo1) and bo1.live:
                bo1.live = 0
                bo1.hit()

            if b.hittest(t2) and t2.live:
                t2.live = 0
                t2.hit()
                canv.itemconfig(t1.id_points, text=t2.points + t1.points)
            if t2.live == 0 and t1.live == 0:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='' + str(bullet_1) + '')
            if not bo1.live:
                canv.itemconfig(screen1, text='You Dead!!Get Good ')
            if not g1.live:
                exit()
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game)


new_game()
mainloop()