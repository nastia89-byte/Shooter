from pygame import *
from random import *
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()

        # if keys[K_w] and self.rect.y > 0:
        #    self.rect.y -= self.speed
        # if keys[K_s] and self.rect.y < win_height - self.rect.height:
        #   self.rect.y += self.speed

        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

        # pos = mouse.get_pos()
        # self.rect.x = pos[0] - self.rect.width/2
        # self.rect.y = pos[1] - self.rect.height/2

        self.reset()

    def fire(self):
        bullet = Bullet("mech.png", self.rect.centerx - 20, self.rect.y - 45, 30, 100, 5)
        Bullets.add(bullet)
        f = mixer.Sound("fire3.ogg")
        f.play()


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height + 50:
            self.rect.y = -100
            self.rect.x = randint(0, win_width - 100)
            self.speed = randint(2, 8)
            global lost
            lost += 1

        self.reset()


class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()
        self.reset()

class Gun(GameSprite):

    def __init__(self, gun_img, bullet_img ,player, size_x,size_y, fire_speed):
        super().__init__(gun_img,player.rect.x, player.rect.y,size_x,size_y,fire_speed)
        self.player = player
        self.bullet_img = bullet_img

    def update(self,shift_x=0,shift_y=0):
        self.reset()
        self.rect.x = self.player.rect.x +shift_x
        self.rect.y = self.player.rect.y+shift_y

    def fire(self):
        bullet = Bullet(self.bullet_img, self.rect.centerx - 10, self.rect.y, 20, 40, self.speed)
        Bullets.add(bullet)
        f = mixer.Sound("fire3.ogg")


win_width = 1000
win_height = 800

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
display.set_icon(image.load('rocket.png'))
background = transform.scale(image.load("cosmos.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("suschestvo-monstr.ogg")
mixer.music.play()


win_sound = mixer.Sound("win_sound.ogg")
lose_sound = mixer.Sound("lose_sound.ogg")

font.init()
font2 = font.Font(None, 60)
font3 = font.SysFont("Georgia", 40)

win = font2.render("Congratulations you won, my friend!", True, (0, 204, 153))
lose = font2.render("You were defeated. A World Under Threat", True, (255, 0, 0))

###

lost = 0
score = 0

startlive = 100
live = startlive

###
run = True
clock = time.Clock()
finish = False

player = Player("hero.png", win_width / 2, win_height - 170, 100, 170, 10)
gun1 = Gun("spus.png","spus2.png", player, 60,160,10)
gun2 = Gun("garmata.png","kulya.png", player, 40,160,10)

Monsters = sprite.Group()
monsters_img = ["monster.png", "monster2.png", "monster3.png", "monster4.png", "monster5.png"]

for i in range(5):
    monster = Enemy(choice(monsters_img), randint(0, win_width - 50), -100, 80, 120, randint(2, 8))
    Monsters.add(monster)

Bullets = sprite.Group()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                gun1.fire()
                gun2.fire()

    if not finish:
        window.blit(background, (0, 0))

        player.update()

        gun1.update(-40,5)
        gun2.update(80, 5)

        Monsters.update()
        Bullets.update()


        collide = sprite.groupcollide(Monsters,Bullets, True,True)
        for c in collide:
            score +=1
            monster = Enemy(choice(monsters_img), randint(0, win_width - 50), -100, 80, 120, randint(2, 8))
            Monsters.add(monster)

        collide = sprite.spritecollide(player,Monsters, True)
        for c in collide:
            live -=10
            monster = Enemy(choice(monsters_img), randint(0, win_width - 50), -100, 80, 120, randint(2, 8))
            Monsters.add(monster)


        text = font3.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))

        text = font3.render("Lost: " + str(lost), True, (255, 255, 255))
        window.blit(text, (10, 70))

        if live > startlive* .6:
            color_live = (0, 204, 153)
        elif live > startlive* .1:
            color_live = (255, 255, 0)
        else:
            color_live = (200, 0, 0)

        text = font3.render("Live: " + str(live), True, (color_live))
        window.blit(text, (10, 120))

        if live <= 0:
            mixer.music.stop()
            lose_sound.play()
            finish = True
            window.blit(lose, (win_width // 2 - lose.get_width() // 2, win_height // 2 - lose.get_height() // 2))

        if score >= 50:
            mixer.music.stop()
            win_sound.play()
            win_sound.set_volume(0.2)
            finish = True
            window.blit(win, (win_width // 2 - win.get_width() // 2, win_height // 2 - win.get_height() // 2))

    display.update()
    clock.tick(60)
