import pygame
from pygame.locals import *

import gamelib

class Ball(object):

    def __init__(self, radius, color, pos, speed=(0,100)):
        (self.x, self.y) = pos
        (self.vx, self.vy) = speed
        self.radius = radius
        self.color = color
        self.image=pygame.image.load("ball-2.png")

    def bounce_player(self,player):
        if player.x+player.width/2.0-5<self.x<player.x+player.width/2.0+5:
            self.vy = -self.vy # bounce ball back
        if player.x+player.width*3/4.0>self.x>=player.x+player.width/2.0+5:
            self.vy = -self.vy
            self.vx +=0.75
        if player.x+player.width*3/4.0<=self.x:
            self.vy = -self.vy
            self.vx +=1.75
        if player.x+player.width/4.0<self.x<=player.x+player.width/2.0-5:
            self.vy = -self.vy
            self.vx -=0.75
        if player.x+player.width/4.0>=self.x:
            self.vy = -self.vy
            self.vx -=1.75

    def bounce_enemy(self,enemy):
        if enemy.x+enemy.width/2.0-4<self.x<enemy.x+enemy.width/2.0+4:
            self.vy = -self.vy # bounce ball back
        if enemy.x+enemy.width*3/4.0>self.x>=enemy.x+enemy.width/2.0+4:
            self.vy = -self.vy
            self.vx +=0.75
        if enemy.x+enemy.width*3/4.0<=self.x:
            self.vy = -self.vy
            self.vx +=1.75
        if enemy.x+enemy.width/4.0<self.x<=enemy.x+enemy.width/2.0-4:
            self.vy = -self.vy
            self.vx -=0.75
        if enemy.x+enemy.width/4.0>=self.x:
            self.vy = -self.vy
            self.vx -=1.75
    
    def bounce_walls(self,walls):
            self.vy=-self.vy
            if self.x-10==walls.x:
                self.vx=-self.vx

    def move(self, delta_t, display, player):
        global score, game_over
        self.x += self.vx
        self.y += self.vy

        # make ball bounce if hitting wall
        if self.x < self.radius:
            self.vx = abs(self.vx)
            game_over = True # game over when ball hits left wall
        if self.y < self.radius:
            self.vy = abs(self.vy)
        if self.x > display.get_width()-self.radius:
            self.vx = -abs(self.vx)
        if self.y > display.get_height()-self.radius:
            self.vy = -abs(self.vy)

    def score(self):
        if self.y==5:
            return True
        if self.y==475:
            return False

    def render(self, surface):
        pos = (int(self.x),int(self.y))
        #pygame.draw.circle(surface, self.color, pos, self.radius, 0)
        surface.blit(self.image,(pos[0]-10,pos[1]-10))

#########################################
class Player(object):

    THICKNESS = 10

    def __init__(self, pos, color, width=100):
        self.width = width
        (self.x,self.y) = pos
        self.color = color

    def can_hit(self, ball):
        return ball.y==self.y-ball.radius \
            and self.x-10<ball.x <self.x+ self.width+10

    def move(self, ball):
        if ball.x>self.x+50:
            self.x+=2
        if ball.x<self.x+50:
            self.x-=2

    def move_left(self):
        self.x -= 5
        if self.x<-60:
            self.x=580

    def move_right(self):
        self.x += 5
        if self.x > 580:
            self.x=-60

    def move_up(self):
        self.y -= 5

    def move_down(self):
        self.y += 5

    def render(self, surface):
        pygame.draw.rect(surface,
                         self.color,
                         [self.x,
                          self.y,
                          self.width,
                          self.THICKNESS],2)

######################################################
class Walls(object):
    def __init__(self, pos, color, width=60):
        (self.x,self.y) = pos
        self.color = color
        self.width = width

    def draw(self,surface,num):
                pygame.draw.rect(surface, self.color,
                                [100+(100*num),self.y,self.width,10],2)

    def Hit(self, ball, pos):
        x=pos[0]       
        y=pos[1]
        return (y-10<ball.y<y+20) \
                and (x<ball.x <x+ self.width) 

###################################
class Enemy(object):

    THICKNESS = 10

    def __init__(self, pos, color, width=100):
        self.width = width
        (self.x,self.y) = pos
        self.color = color

    def can_hit(self, ball):
        return ball.y==self.y+ball.radius+10 \
            and self.x-10<ball.x <self.x+ self.width+10

    def move(self, ball):
        if ball.x>self.x+50:
            self.x+=1
        if ball.x<self.x+50:
            self.x-=1

    def move_left(self):
        self.x -= 5
        if self.x<-60:
            self.x=580

    def move_right(self):
        self.x += 5
        if self.x > 580:
            self.x=-60

    def render(self, surface):
        pygame.draw.rect(surface,
                         self.color,
                         [self.x,
                          self.y,
                          self.width,
                          self.THICKNESS],2)