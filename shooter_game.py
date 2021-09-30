
from pygame import *
from random import randint

window = display.set_mode((700,500))
background = transform.scale(image.load("galaxy.jpg"),(700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,x,y,size_x,size_y,speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def render(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx , self.rect.top,15,20,10)
        bullets.add(bullet)

killed = 0
lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > 500:
            lost += 1
            print(lost)
            self.rect.y = 0
            self.rect.x = randint(40, 660)

player = player("rocket.png", 250, 400, 80, 100, 10)

enemies = sprite.Group()
bullets = sprite.Group()
for i in range(1 , 6):
    enemy1 = Enemy("ufo.png", randint(40, 660) , 0 , 80, 50, randint(1,3))
    enemies.add(enemy1)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()

game = True
clock = time.Clock()

font.init()
font_1 = font.Font(None, 24)
font_2 = font.Font(None, 80)
font_3 = font.Font(None, 48)
font_4 = font.Font(None, 48)

win = font_2.render("ТЫ ПОБЕДИЛ" , True, (255,255,255))
lose = font_2.render("ТЫ ПРОИГРАЛ", True, (180, 0, 0))
#player = player("rocket.png", 250, 400, 80, 100, 10)
restart_button = GameSprite("restart.png",210,250,200,100,0)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    collide = sprite.groupcollide(enemies, bullets, True, True)
    for c in collide:
        enemy1 = Enemy("ufo.png", randint(40, 660) , 0 , 80, 50, randint(1,3))
        enemies.add(enemy1)
        killed += 1
        
    window.blit(background,(0,0))

    lost_text = font_3.render(str(lost), False, (255,255,255))
    killed_text = font_3.render(str(killed), False, (255,255,255))

    window.blit(lost_text, (10, 10))
    window.blit(killed_text, (10, 40))

    if lost >= 10:
        window.blit(lose, (150,200))
        restart_button.render()
        for e in enemies:
            e.kill()

        if sprite.spritecollide(restart_button,bullets,True):
            lost = 0
            killed = 0
            time.delay(500)
            for i in range(1 , 6):
                enemy1 = Enemy("ufo.png", randint(40, 660) , 0 , 80, 50, randint(1,3))
                enemies.add(enemy1)

    if killed >= 100:
        window.blit(win, (150,200))
        restart_button.render()
        for e in enemies:
            e.kill()

        if sprite.spritecollide(restart_button,bullets,True):
            lost = 0
            killed = 0
            time.delay(500)
            for i in range(1 , 6):
                enemy1 = Enemy("ufo.png", randint(40, 660) , 0 , 80, 50, randint(1,3))
                enemies.add(enemy1)


    player.update()
    player.render()
    enemies.update()
    enemies.draw(window)
    bullets.draw(window)
    bullets.update()
    display.update()
    clock.tick(48)