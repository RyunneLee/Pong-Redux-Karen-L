import sys
import pygame
import os
import time
import pdb


os.environ['SDL_VIDEO_CENTERED'] = '1'

WHITE = (255, 255, 255)
pygame.init()

WIN_W = 1100
WIN_H = 700
p_width = 40
p_height = 160
p_speed = 15
FADE_OUT_EASING = lambda x: x  # Linear
FADE_OUT_TIME = 500
last_state_change = time.time()

b_height = 30
b_width = 30
b_speed = (20, 20)

class Game:
    def __init__(self,ball, clock, left_paddle, right_paddle, screen, top_paddle, bottom_paddle):
        self.clock = clock
        self.left = left_paddle
        self.right = right_paddle
        self.top_p = top_paddle
        self.bottom_p = bottom_paddle
        self.ball = ball
        self.intro = True

        self.screen = screen
        self.play = True
        self.left_score = 0
        self.right_score = 0
        self.top_score = 0
        self.bottom_score = 0
        self.done = False
        self.restart = False
        self.round = 100
        self.rules = True

        self.intro_bg = pygame.image.load("image/introBackground.jpg")
        self.intro_bg = pygame.transform.scale(self.intro_bg, (WIN_W, WIN_H))
        self.intro_rect = self.intro_bg.get_rect()

        self.bg = pygame.image.load("image/background.jpg")
        self.bg = pygame.transform.scale(self.bg, (WIN_W, WIN_H))
        self.bg_rect = self.bg.get_rect()

        self.ed_bg = pygame.image.load("image/end.jpg")
        self.ed_bg = pygame.transform.scale(self.ed_bg, (WIN_W, WIN_H))
        self.ed_rect = self.ed_bg.get_rect()

        self.title = Text(125, "Space Pong", WIN_W / 3.9, WIN_H / 3)
        self.subtitle = Text(85, "-- Click Here --", WIN_W / 3.8, WIN_H / 2)

        self.Rule = Text(80, "This is a 4 Player Game", WIN_W / 4.9, WIN_H / 3.7)
        self.Rule1 = Text(70, "Top and Right Paddles = Green Team", WIN_W / 6.1, WIN_H / 2.7)
        self.Rule2 = Text(70, "Bottom and Left Paddles = Red Team", WIN_W / 7.1, WIN_H / 2.2)
        self.Rule3 = Text(70, "The Team Who Gets 3 Points Win", WIN_W / 6.6, WIN_H / 1.8)
        self.start = Text(70, "-- Ready? --", WIN_W / 2.9, WIN_H / 1.5)

        self.l_winner = Text(55, "Green Team Wins!", WIN_W / 2.6, WIN_H/1.5 )
        self.r_winner = Text(55, "Red Team Wins!", WIN_W / 2.6, WIN_H/1.5 )

        self.all_paddles = pygame.sprite.Group()
        self.all_paddles.add(left_paddle)
        self.all_paddles.add(right_paddle)
        self.all_paddles.add(top_paddle)
        self.all_paddles.add(bottom_paddle)


    def run_intro(self):


        while self.intro:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    self.intro = False

            # Sprites on screen
            self.screen.blit(self.intro_bg, self.intro_rect)

            self.screen.blit(self.title.image, self.title.rect)
            if pygame.time.get_ticks() % 1000 < 500:
                self.screen.blit(self.subtitle.image, self.subtitle.rect)

            self.clock.tick(60)
            pygame.display.flip()

    def run_rules(self):
        while self.rules:

            self.screen.blit(self.intro_bg, self.intro_rect)
            self.screen.blit(self.Rule.image, self.Rule.rect)
            self.screen.blit(self.Rule1.image, self.Rule1.rect)
            self.screen.blit(self.Rule2.image, self.Rule2.rect)
            self.screen.blit(self.Rule3.image, self.Rule3.rect)

            if pygame.time.get_ticks() % 1000 < 500:
                self.screen.blit(self.start.image, self.start.rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                        self.rules = False

            self.clock.tick(60)
            pygame.display.flip()


    def run_play(self):
        music_play = pygame.mixer.Sound("sound/maplestory.ogg")
        music_play.play()

        last_state_change = time.time()

        while self.play:

            if self.done == True:
                return
            left_score_text = Text(40, "Green Team:  " + str(self.left_score), WIN_W / 1.6, WIN_H / 10)
            right_score_text = Text(40, "Red Team:  " + str(self.right_score), WIN_W / 5, WIN_H / 10)


            three = Text( 100, "3", WIN_W / 2, WIN_H / 2)
            two = Text( 100, "2", WIN_W / 2, WIN_H / 2)
            one = Text( 100, "1", WIN_W / 2, WIN_H / 2)

            state_time = time.time() - last_state_change


            if state_time >= FADE_OUT_TIME:
                state = 0
                state_time -= FADE_OUT_TIME
                last_state_change = time.time() - state_time

            self.left.update()
            self.right.update()
            self.top_p.update_two()
            self.bottom_p.update_two()

            self.ball.update(self.all_paddles, self.bottom_p, self.left, self.right, self.top_p)


            # round starts from 100
            if self.round >= 75:
                self.screen.blit(self.bg, self.bg_rect)
                self.screen.blit(three.image, three.rect)

                self.round = self.round - 1

            elif self.round >= 50:

                self.screen.blit(self.bg, self.bg_rect)
                self.screen.blit(two.image, two.rect)

                self.round = self.round - 1

            elif self.round >= 25:

                self.screen.blit(self.bg, self.bg_rect)
                self.screen.blit(one.image, one.rect)

                self.round = self.round - 1

            else:
                self.round = 0
                self.screen.blit(self.bg, self.bg_rect)
                self.screen.blit(self.ball.image, self.ball.rect)
                self.ball.move()




            if self.ball.rect.left < 0 - self.ball.rect.width or self.ball.rect.left > WIN_W + self.ball.rect.width or self.ball.rect.bottom < 0  or self.ball.rect.top > WIN_H:
                    if self.ball.rect.left < 0 or self.ball.rect.top <0:
                        self.right_score += 1
                        right_score_text = Text(40, "Red Team:  " + str(self.right_score), WIN_W / 5, WIN_H / 10)
                        self.round = 100
                        last_state_change = time.time()


                        if state_time >= FADE_OUT_TIME:
                            state = 0
                            state_time -= FADE_OUT_TIME
                            last_state_change = time.time() - state_time

                    elif self.ball.rect.left > WIN_W + self.ball.rect.width or self.ball.rect.bottom > WIN_H:
                        self.left_score += 1
                        left_score_text = Text(40, "Green Team:  " + str(self.left_score), WIN_W / 1.6, WIN_H / 10)
                        self.round = 100
                        last_state_change = time.time()


                        if state_time >= FADE_OUT_TIME:
                            state = 0
                            state_time -= FADE_OUT_TIME
                            last_state_change = time.time() - state_time


                    self.ball.rect.y = WIN_H / 2 - (b_height / 2)
                    self.ball.rect.x = WIN_W / 2
                    self.left.y = (WIN_H / 2) - (p_height / 2)
                    self.right.y = (WIN_H / 2) - (p_height / 2)


            if self.right_score == 3:
                self.done = True

            elif self.left_score == 3:
                self.done = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


        # Fade Out the Text
            alpha = 1. - FADE_OUT_EASING(1.0 * state_time / 2)
            left_score_surface = pygame.surface.Surface((left_score_text.rect.width, left_score_text.rect.height))
            left_score_surface.set_alpha(255 * alpha)
            left_score_surface.blit(left_score_text.image, (0,0))
            self.screen.blit(left_score_surface,left_score_text.rect)

            right_score_surface = pygame.surface.Surface((right_score_text.rect.width, right_score_text.rect.height))
            right_score_surface.set_alpha(255 * alpha)
            right_score_surface.blit(right_score_text.image, (0, 0))
            self.screen.blit(right_score_surface, right_score_text.rect)

            self.screen.blit(self.left.image, self.left.rect)
            self.screen.blit(self.right.image, self.right.rect)
            self.screen.blit(self.top_p.image, self.top_p.rect)
            self.screen.blit(self.bottom_p.image, self.bottom_p.rect)

            self.clock.tick(60)
            pygame.display.flip()

    def run_restart(self):

        while not self.restart:

            title1 = Text(120, "Great Game!", WIN_W / 3.9, WIN_H / 4)
            subtitle1 = Text(65, "-- Click Here To Restart --", WIN_W / 4, WIN_H / 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    self.restart = True

            # Sprites on screen
            self.screen.blit(self.ed_bg, self.ed_rect)
            self.screen.blit(title1.image, title1.rect)

            if self.left_score > self.right_score:
                self.screen.blit(self.l_winner.image, self.l_winner.rect)
            else:
                self.screen.blit(self.r_winner.image, self.r_winner.rect)

            if pygame.time.get_ticks() % 1000 < 500:
                self.screen.blit(subtitle1.image, subtitle1.rect)

            self.clock.tick(60)
            pygame.display.flip()


class Text:
    def __init__(self, size, text, xpos, ypos):
        self.font = pygame.font.SysFont("Comic Sans", size)
        self.image = self.font.render(text, 1, WHITE)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height, xpos, image, where, ypos, player):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.speed = 25
        self.player = player
        self.image = pygame.image.load(image).convert_alpha()
        self.score = 0
        self.where = where
        if self.where == "top_bottom":
            self.rect = pygame.Rect(WIN_W/2, ypos, self.height, self.width)
            self.image = pygame.transform.scale(self.image, (self.height, self.width))

        elif self.where == "sides":
            self.rect = pygame.Rect(xpos, (WIN_H/2.5), self.width, self.height)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        key = pygame.key.get_pressed()

        if self.player == "right":
            if key[pygame.K_UP]:
                self.rect.y -= self.speed
            if key[pygame.K_DOWN]:
                self.rect.y += self.speed

        elif self.player == "left":
            if key[pygame.K_w]:
                self.rect.y -= self.speed
            if key[pygame.K_s]:
                self.rect.y += self.speed

        if self.rect.y < 0 + 100:
            self.rect.y = 0  +100

        if self.rect.bottom > WIN_H - 120:
            self.rect.bottom = WIN_H -120

    def update_two(self):
        key = pygame.key.get_pressed()

        if self.player == "top":
            if key[pygame.K_j]:
                self.rect.x -= self.speed
            if key[pygame.K_k]:
                self.rect.x += self.speed

        elif self.player == "bottom":
            if key[pygame.K_f]:
                self.rect.x -= self.speed
            if key[pygame.K_g]:
                self.rect.x += self.speed

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.bottom > WIN_H:
            self.rect.bottom = WIN_H

        if self.rect.left < 0 + 80:
            self.rect.left = 0 + 80

        if self.rect.right > WIN_W - (p_width*3) - 60:
            self.rect.right = WIN_W - (p_width*3) - 60


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.speed = 20
        self.ball_direction = 8,8
        self.image = pygame.image.load("image/ball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = pygame.Rect(WIN_W / 2 - (self.width / 2), WIN_H / 2 - (self.height / 2), self.width, self.height)

    def move(self):
        self.rect = self.rect.move(self.ball_direction)

    def update(self, all_paddles, bottom_paddle,left_paddle, right_paddle, top_paddle):

        collisions = pygame.sprite.spritecollide(self, all_paddles, False)
        for l in collisions:
            if l == bottom_paddle:
                self.ball_direction = self.ball_direction[0], -self.ball_direction[1]
                self.rect = self.rect.move(self.ball_direction)

            elif l == top_paddle:
                self.ball_direction = self.ball_direction[0], -self.ball_direction[1]
                self.rect = self.rect.move(self.ball_direction)

            elif l == right_paddle:
                self.ball_direction = -self.ball_direction[0], self.ball_direction[1]
                self.rect = self.rect.move(self.ball_direction)

            elif l == left_paddle:
                self.ball_direction = -self.ball_direction[0], self.ball_direction[1]
                self.rect = self.rect.move(self.ball_direction)
def main():

    while True:
        pygame.display.set_caption("Space Pong - Karen Lee")
        screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
        left_paddle = Paddle(40, 150, 40 * 2,"image/paddle_left.png", "sides", 0, "left")
        right_paddle = Paddle(40, 150, WIN_W - (40 * 3),"image/paddle_right.png", "sides", 0, "right" )
        top_paddle = Paddle(40, 140, 0,"image/right_paddle1.png", "top_bottom",WIN_H/8.5, "top")
        bottom_paddle = Paddle(40, 150,0,"image/left_paddle1.png", "top_bottom", 600, "bottom")
        ball = Ball(30, 30)
        clock = pygame.time.Clock()
        run = Game(ball, clock, left_paddle, right_paddle, screen, top_paddle, bottom_paddle)

        run.run_intro()
        run.run_rules()
        run.run_play()
        run.run_restart()

if __name__ == "__main__":
    main()