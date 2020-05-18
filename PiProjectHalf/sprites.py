import pygame as pg
from settings import *
vec2 = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (screenWidth/2,screenHeight/2)
        self.pos = vec2(25,100)
        self.vel = vec2(0,0)
        self.acc = vec2(0,0)
        self.walking = False
        self.jumping = False
        self.punching = False
        self.healthchange = False
        self.scorechange = False
        self.ptimer = 0
        self.health = 0
        self.current_frame = 0
        self.last_update = 0
        self.punchsfx = pg.mixer.Sound('assets/sounds/punchsfx.mp3')
        self.deathsfx = pg.mixer.Sound('assets/sounds/jawadeath.mp3')

        

    def jump(self):
            self.vel.y = -(screenHeight/25)

    def load_images(self):
        self.standing_frames = [pg.image.load('assets/sprites/P1/Idle/standing.png'),
                                pg.image.load('assets/sprites/P1/Idle/standing2.png')]
        self.walk_frames_r = [pg.image.load('assets/sprites/P1/RWalk/R1.png'), pg.image.load('assets/sprites/P1/RWalk/R2.png'),
                              pg.image.load('assets/sprites/P1/RWalk/R3.png'),pg.image.load('assets/sprites/P1/RWalk/R4.png'),
                              pg.image.load('assets/sprites/P1/RWalk/R5.png')]
        self.walk_frames_l = [pg.image.load('assets/sprites/P1/LWalk/L1.png'), pg.image.load('assets/sprites/P1/LWalk/L2.png'),
                              pg.image.load('assets/sprites/P1/LWalk/L3.png'), pg.image.load('assets/sprites/P1/LWalk/L4.png'),
                              pg.image.load('assets/sprites/P1/LWalk/L5.png')]
        self.jump_frames = [pg.image.load('assets/sprites/P1/Jump/J1.png'),pg.image.load('assets/sprites/P1/Jump/J2.png')]
        self.punch_frames_l = [pg.image.load('assets/sprites/p1/punch.png')]
        self.punch_frames_r = [pg.image.load('assets/sprites/p1/punch2.png')]



    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #show walk animation
        if self.walking:
            if now - self.last_update > 250:
                self.last_update - now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.punching:
            if self.vel.x > 0:
                self.image = self.punch_frames_r[0]
                self.punchsfx.play()
            else:
                self.image = self.punch_frames_l[0]
                self.punchsfx.play()
        if not self.jumping and not self.walking and not self.punching:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

        self.mask = pg.mask.from_surface(self.image)

                
                
        

    def update(self):
        self.animate()
        self.acc = vec2(0,0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -p_acc
        if keys[pg.K_d]:
            self.acc.x = p_acc

        self.acc.x += self.vel.x * p_fric
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > screenWidth:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screenWidth

        self.rect.midbottom = self.pos
            


class Platform(pg.sprite.Sprite):
    def __init__(self, imagen, x, y):
        pg.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.plat_images[imagen]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        self.plat_images = [pg.image.load('assets/sprites/plats/rock/rock1.png'),pg.image.load('assets/sprites/plats/rock/rock2.png'),
                        pg.image.load('assets/sprites/plats/rock/rock3.png')]

class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load('assets/sprites/backgrounds/scene1.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class playerHp(pg.sprite.Sprite):
    def __init__(self,imageNum, x,y):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.load_images()
        self.image = self.p1health[imageNum]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        self.p1health = [pg.image.load('assets/sprites/p1/Hp/0.png'),pg.image.load('assets/sprites/p1/Hp/5.png'),
                         pg.image.load('assets/sprites/p1/Hp/10.png'),pg.image.load('assets/sprites/p1/Hp/15.png')
                         ,pg.image.load('assets/sprites/p1/Hp/20.png'),pg.image.load('assets/sprites/p1/Hp/25.png'),
                         pg.image.load('assets/sprites/p1/Hp/30.png'),pg.image.load('assets/sprites/p1/Hp/35.png'),
                         pg.image.load('assets/sprites/p1/Hp/40.png'),pg.image.load('assets/sprites/p1/Hp/45.png'),
                         pg.image.load('assets/sprites/p1/Hp/50.png'),pg.image.load('assets/sprites/p1/Hp/55.png'),
                         pg.image.load('assets/sprites/p1/Hp/60.png'),pg.image.load('assets/sprites/p1/Hp/65.png'),
                         pg.image.load('assets/sprites/p1/Hp/70.png'),pg.image.load('assets/sprites/p1/Hp/75.png'),
                         pg.image.load('assets/sprites/p1/Hp/80.png'),pg.image.load('assets/sprites/p1/Hp/85.png'),
                         pg.image.load('assets/sprites/p1/Hp/90.png'),pg.image.load('assets/sprites/p1/Hp/95.png')
                         ,pg.image.load('assets/sprites/p1/Hp/100.png')]

class Score(pg.sprite.Sprite):
    def __init__(self, inumber, x, y):
        pg.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.scoreim[inumber]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        self.scoreim = [pg.image.load('assets/sprites/score/dash.png'),pg.image.load('assets/sprites/score/0.png'),
                        pg.image.load('assets/sprites/score/1.png'),pg.image.load('assets/sprites/score/2.png'),
                        pg.image.load('assets/sprites/score/3.png'),pg.image.load('assets/sprites/score/ko.png')]

class Main_Menu(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load('assets/sprites/menus/MainMenu.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class ControlMenu(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load('assets/sprites/menus/controlMenu.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (screenWidth/2,screenHeight/2)
        self.pos = vec2(545,100)
        self.vel = vec2(0,0)
        self.acc = vec2(0,0)
        self.walking = False
        self.jumping = False
        self.punching = False
        self.healthchange = False
        self.scorechange = False
        self.ptimer = 0
        self.health = 0
        self.current_frame = 0
        self.last_update = 0
        self.punchsfx = pg.mixer.Sound('assets/sounds/punchsfx.mp3')
        self.deathsfx = pg.mixer.Sound('assets/sounds/yodadeath.mp3')

        

    def jump(self):
            self.vel.y = -(screenHeight/25)

    def load_images(self):
        self.standing_frames = [pg.image.load('assets/sprites/P2/Idle/standing.png'),
                                pg.image.load('assets/sprites/P2/Idle/standing2.png')]
        self.walk_frames_r = [pg.image.load('assets/sprites/P2/RWalk/R1.png'), pg.image.load('assets/sprites/P2/RWalk/R2.png'),
                              pg.image.load('assets/sprites/P2/RWalk/R3.png'),pg.image.load('assets/sprites/P2/RWalk/R4.png'),
                              pg.image.load('assets/sprites/P2/RWalk/R5.png')]
        self.walk_frames_l = [pg.image.load('assets/sprites/P2/LWalk/L1.png'), pg.image.load('assets/sprites/P2/LWalk/L2.png'),
                              pg.image.load('assets/sprites/P2/LWalk/L3.png'), pg.image.load('assets/sprites/P2/LWalk/L4.png'),
                              pg.image.load('assets/sprites/P2/LWalk/L5.png')]
        self.jump_frames = [pg.image.load('assets/sprites/P2/Jump/J1.png'),pg.image.load('assets/sprites/P2/Jump/J2.png')]
        self.punch_frames_l = [pg.image.load('assets/sprites/p2/punch.png')]
        self.punch_frames_r = [pg.image.load('assets/sprites/p2/punch2.png')]



    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #show walk animation
        if self.walking:
            if now - self.last_update > 250:
                self.last_update - now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.punching:
            if self.vel.x > 0:
                self.image = self.punch_frames_r[0]
                self.punchsfx.play()
            else:
                self.image = self.punch_frames_l[0]
                self.punchsfx.play()

        if not self.jumping and not self.walking and not self.punching:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

        self.mask = pg.mask.from_surface(self.image)

                
                
        

    def update(self):
        self.animate()
        self.acc = vec2(0,0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -p_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = p_acc

        self.acc.x += self.vel.x * p_fric
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > screenWidth:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screenWidth

        self.rect.midbottom = self.pos
