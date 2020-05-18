### Smashbros rip-off game ###
import pygame as pg
import random
import sys
from settings import *
from sprites import *
import time


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screenWidth,screenHeight))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        global Inum
        global Inum2
        global Snum
        global Snum2
        Inum = 0
        Inum2 = 0
        Snum = 1
        Snum2 = 1
        self.kosfx = pg.mixer.Sound('kosfx.mp3')
        pg.mixer.music.stop()
        pg.mixer.music.set_volume(.05)
        pg.mixer.music.load('track1.mp3')
        pg.mixer.music.play(-1)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.players2 = pg.sprite.Group()
        self.players1 = pg.sprite.Group()

        self.player_1 = Player()
        self.all_sprites.add(self.player_1)
        self.players1.add(self.player_1)

        self.player_2 = Player2()
        self.all_sprites.add(self.player_2)
        self.players2.add(self.player_2)
        
        #creates platforms
        plat_1 = Platform(0, 0,92)
        plat_2 = Platform(1, 141,156)
        plat_3 = Platform(2, 446,156)
        #adds platforms to groups
        self.all_sprites.add(plat_1)
        self.platforms.add(plat_1)

        self.all_sprites.add(plat_2)
        self.platforms.add(plat_2)

        self.all_sprites.add(plat_3)
        self.platforms.add(plat_3)

        self.Currenthp = playerHp(0, 10, 240)
        self.all_sprites.add(self.Currenthp)
        self.Currenthp2 = playerHp(0, 500, 240)
        self.all_sprites.add(self.Currenthp2)

        self.scoreDash = Score(0,275,10)
        self.all_sprites.add(self.scoreDash)

        self.Currentscore = Score(1,225,10)
        self.all_sprites.add(self.Currentscore)
        self.Currentscore2 = Score(1,325,10)
        self.all_sprites.add(self.Currentscore2)
        

        self.mask = pg.mask.from_surface(plat_1.image)


        # runs run
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        global Inum
        global Inum2
        global Snum
        global Snum2
        
        if self.player_1.healthchange:
            Inum += 1
            self.all_sprites.remove(self.Currenthp)
            self.Currenthp = playerHp(Inum, 10, 240)
            self.all_sprites.add(self.Currenthp)
            self.player_1.healthchange = False

        if self.player_2.healthchange:
            Inum2 += 1
            self.all_sprites.remove(self.Currenthp2)
            self.Currenthp2 = playerHp(Inum2, 500, 240)
            self.all_sprites.add(self.Currenthp2)
            self.player_2.healthchange = False

        if self.player_1.scorechange:
            Snum += 1
            self.all_sprites.remove(self.Currentscore)
            self.Currentscore = Score(Snum, 225,10)
            self.all_sprites.add(self.Currentscore)
            self.player_1.scorechange = False

        if self.player_2.scorechange:
            Snum2 += 1
            self.all_sprites.remove(self.Currentscore2)
            self.Currentscore2 = Score(Snum2, 325,10)
            self.all_sprites.add(self.Currentscore2)
            self.player_2.scorechange = False

        if Snum == -1:
            time.sleep(3)
            pg.mixer.music.load('track3.mp3')
            pg.mixer.music.set_volume(.1)
            pg.mixer.music.play(-1)
            if self.playing:
                self.playing = False
            self.running = False
            
            
        self.death()            

        
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player_1, self.platforms, False, pg.sprite.collide_mask)
        if hits:
            if self.player_1.pos.x < hits[0].rect.left:
                self.player_1.pos.x = hits[0].rect.left
                
            elif self.player_1.pos.x > hits[0].rect.right:
                self.player_1.pos.x = hits[0].rect.right
                
            elif self.player_1.pos.y < hits[0].rect.bottom:
                self.player_1.pos.y = hits[0].rect.top +3
                self.player_1.vel.y = 0

        hits = pg.sprite.spritecollide(self.player_2, self.platforms, False, pg.sprite.collide_mask)
        if hits:
            if self.player_2.pos.x < hits[0].rect.left:
                self.player_2.pos.x = hits[0].rect.left
                
            elif self.player_2.pos.x > hits[0].rect.right:
                self.player_2.pos.x = hits[0].rect.right
                
            elif self.player_2.pos.y < hits[0].rect.bottom:
                self.player_2.pos.y = hits[0].rect.top + 5
                self.player_2.vel.y = 0

        if self.player_1.punching and self.player_1.ptimer == 0:
            hits = pg.sprite.spritecollide(self.player_1, self.players2, False, pg.sprite.collide_mask)
            if hits:
                self.player_2.health += 5
                self.player_2.healthchange = True
                print(self.player_2.health)
                self.player_1.ptimer = 50
            self.player_1.punching = False
        elif self.player_1.punching:
            self.player_1.punching = False
                

        if self.player_2.punching and self.player_2.ptimer == 0:
            hits = pg.sprite.spritecollide(self.player_2, self.players1, False, pg.sprite.collide_mask)
            if hits:
                self.player_1.health += 5
                self.player_1.healthchange = True
                print(self.player_1.health)
                self.player_2.ptimer = 50
            self.player_2.punching = False
        elif self.player_2.punching:
            self.player_2.punching = False

        if self.player_1.ptimer > 0:
            self.player_1.ptimer -= 1
        if self.player_2.ptimer > 0:
            self.player_2.ptimer -= 1
            

    def events(self):
        for event in pg.event.get():
            mPos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                hits = pg.sprite.spritecollide(self.player_1,self.platforms,False)
                hits2 = pg.sprite.spritecollide(self.player_2,self.platforms,False)
                if event.key == pg.K_w and hits:
                    self.player_1.jump()
                if event.key == pg.K_UP and hits2:
                    self.player_2.jump()
                if event.key == pg.K_e:
                    self.player_1.punching = True
                if event.key == pg.K_RCTRL:
                    self.player_2.punching = True
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def draw(self):
        self.screen.fill([255, 255, 255])
        BackGround = Background('backgrounds/scene1.png', [0,0])
        self.screen.blit(BackGround.image, BackGround.rect)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_text(self,text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def death(self):
        global Snum
        global Snum2
        
        if self.player_2.health == 100:
            self.all_sprites.remove(self.player_2)
            self.player_2.deathsfx.play()
            self.all_sprites.remove(self.Currenthp2)
            self.Currenthp2 = playerHp(0, 500, 240)
            self.all_sprites.add(self.Currenthp2)
            self.player_1.scorechange = True
        if self.player_1.health == 100:
            self.all_sprites.remove(self.player_1)
            self.player_1.deathsfx.play()
            self.all_sprites.remove(self.Currenthp)
            self.Currenthp = playerHp(0, 5, 240)
            self.all_sprites.add(self.Currenthp)
            self.player_2.scorechange = True

        if self.player_2.pos.y > 500:
            self.player_2.deathsfx.play()
            self.all_sprites.remove(self.Currenthp2)
            self.Currenthp2 = playerHp(0, 500, 240)
            self.all_sprites.add(self.Currenthp2)
            self.player_2.pos.x = 545
            self.player_2.pos.y = -1000
            self.player_1.scorechange = True
            
        if self.player_1.pos.y > 500:
            self.player_1.deathsfx.play()
            self.all_sprites.remove(self.Currenthp)
            self.Currenthp = playerHp(0, 5, 240)
            self.all_sprites.add(self.Currenthp)
            self.player_1.pos.x = 25
            self.player_1.pos.y = -1000
            self.player_2.scorechange = True
        if Snum == 4:
            self.all_sprites.remove(self.Currentscore)
            self.all_sprites.remove(self.Currentscore2)
            self.all_sprites.remove(self.scoreDash)
            self.kosfx.play()
            Snum = -1
            self.ko = Score(5,275,10)
            self.all_sprites.add(self.ko)
        if Snum2 == 4:
            self.all_sprites.remove(self.Currentscore)
            self.all_sprites.remove(self.Currentscore2)
            self.all_sprites.remove(self.scoreDash)
            self.kosfx.play()
            Snum2 = -1
            self.ko2 = Score(5,275,10)
            self.all_sprites.add(self.ko2)
        
            
            
        
        
            
            
    def MainMenu(self):
        click = False
        while True:
            font = pg.font.SysFont('comicsans',40)
            self.screen.fill(BGCOLOR)
            self.screen.fill([255, 255, 255])
            MainMenu = Main_Menu('menus/MainMenu.png', [0,0])
            self.screen.blit(MainMenu.image, MainMenu.rect)
            
            mx, my = pg.mouse.get_pos()

            sgButton = pg.Rect(329, 108, 225, 50)
            conButton = pg.Rect(298, 175, 264, 35)
            extButton = pg.Rect(424, 238, 130, 32)

            if sgButton.collidepoint((mx,my)):
                if click:
                    self.new()
            if conButton.collidepoint((mx,my)):
                if click:
                    g.controlMenu()
            if extButton.collidepoint((mx,my)):
                if click:
                    pg.quit()
                    sys.exit()

            pg.draw.rect(self.screen,(RED), sgButton,1)
            pg.draw.rect(self.screen,(RED), conButton,1)
            pg.draw.rect(self.screen,(RED), extButton,1)

            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                


            pg.display.update()
            self.clock.tick(FPS)

    def controlMenu(self):
        while True:
            self.screen.fill(BGCOLOR)
            self.screen.fill([255, 255, 255])
            ControlMenu = Control_Menu('menus/controlMenu.png')
            self.screen.blit(ControlMenu.image, ControlMenu.rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()




    

g = Game()
pg.mixer.music.load('track3.mp3')
pg.mixer.music.set_volume(.1)
pg.mixer.music.play(-1)
g.MainMenu()
while g.running:
    g.new()
    g.show_go_screen()

g.MainMenu
