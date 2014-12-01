import pygame
from pygame.locals import *

import gamelib
from elements import Ball, Player, Walls, Enemy

class SquashGame(gamelib.SimpleGame):
    BLACK = pygame.Color('black')
    GREEN = pygame.Color('green')
    RED = pygame.Color('red')
    YELLOW = pygame.Color('yellow')
    WHITE = pygame.Color('white')
    BLUE = pygame.Color('blue')
    PINK = pygame.Color('pink')
    
    def __init__(self):
        super(SquashGame, self).__init__('Game', SquashGame.BLACK)
        self.ball = Ball(radius=10,
                         color=SquashGame.GREEN,
                         pos=(self.window_size[0]/2,
                              self.window_size[1]/2),
                         speed=(1.5,5))
        self.player = Player(pos=(250,460),
                             color=SquashGame.BLUE)
        self.walls = [Walls(pos=(50,225),color=SquashGame.PINK)]
        self.enemy = Enemy(pos=(250,0),
                            color=SquashGame.RED)
        self.score = 0
        self.score1 = 0


    def init(self):
        super(SquashGame, self).init()
        self.render_score()
        self.EtoP=False
        for num in range(5):
            newWall = Walls(pos=(100+(num*100),225),color=SquashGame.PINK)
            self.walls.append(newWall)

    def update(self):
            self.ball.move(1./self.fps, self.surface, self.player)
            self.EnemyToPlayer()
            self.PlayerMove()
            #self.player.move(self.ball)
            if self.EtoP==False:
                self.enemy.move(self.ball)
            else:
                    self.EnemyMove()

            for i in range(5):
                if self.walls[i].Hit(self.ball,pos=(100+(i*100),225)):
                    self.ball.bounce_walls(self.walls[i])

            if self.enemy.can_hit(self.ball):
                self.ball.bounce_enemy(self.enemy)

            if self.player.can_hit(self.ball):
                self.ball.bounce_player(self.player)

            if self.ball.score():
                self.score1+=1
                self.render_score()
                self.ball = Ball(radius=10,
                                color=SquashGame.YELLOW,
                                pos=(self.window_size[0]/2,
                                450),
                                speed=(1.5,-5))
            elif self.ball.score()==False:
                self.score+=1
                self.render_score()
                self.ball = Ball(radius=10,
                                color=SquashGame.WHITE,
                                pos=(self.window_size[0]/2,
                                50),
                                speed=(-1.5,5))

            
    def render_score(self):
        self.score_image = self.font.render("Score = %d" % self.score, 0, SquashGame.WHITE)
        self.score_image1 = self.font.render("Score = %d" % self.score1, 0, SquashGame.WHITE)


    def EnemyToPlayer(self):
        if self.is_key_pressed(K_SPACE):
            self.EtoP=True
        if self.is_key_pressed(K_5):   
            self.EtoP=False

    def PlayerMove(self):
        if self.is_key_pressed(K_LEFT):
                self.player.move_left()
        if self.is_key_pressed(K_RIGHT):
                self.player.move_right()

    def EnemyMove(self):
        if self.is_key_pressed(K_1):
                self.enemy.move_left()
        if self.is_key_pressed(K_2):
                self.enemy.move_right()

    def render(self, surface):
        self.init_render(surface)
        for num in range(5):
            self.walls[num].draw(surface,num)
        surface.blit(self.score_image, (10,10))
        surface.blit(self.score_image1, (10,460))

    def init_render(self,surface):
        self.ball.render(surface)
        self.player.render(surface)
        self.enemy.render(surface)

def main():
    game = SquashGame()
    game.run()

if __name__ == '__main__':
    main()
