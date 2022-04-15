import pygame
from random import randint, randrange

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Datos de altura, ancho, fondo e icono de la ventana
width = 800;
height = 560;

class naveSpacial(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self);
        self.PictureNave = pygame.image.load('assets/player.png').convert();
        self.PictureNave.set_colorkey(BLACK);

        self.rect = self.PictureNave.get_rect();
        self.rect.centerx = width/2;
        self.rect.centery = height-40;

        self.ListMissile = [];
        self.Live = True;
        self.Life = 100;
        self.Speed = 50;
        self.intruction = True;

    def move(self):
        if self.rect.left <= 0:
            self.rect.left = 0;
        elif self.rect.right >= 800:
            self.rect.right = 800;
        elif self.rect.top <= 0:
            self.rect.top = 0;
        elif self.rect.bottom >= 570:
            self.rect.bottom = 570;

    def shoot(self, x, y):
        myMissile = missile(x, y);
        self.ListMissile.append(myMissile);

    def drawNave(self, superfie):
        superfie.blit(self.PictureNave, self.rect);

class missile(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self);
        self.PictureMissile = pygame.image.load('assets/laser1.png').convert();
        self.PictureMissile.set_colorkey(BLACK);

        self.rect = self.PictureMissile.get_rect();
        self.rect.top = posY;
        self.rect.right = posX;

        self.SpeedMissile = 1;

    def trayectoria(self):
        self.rect.top = self.rect.top - self.SpeedMissile;

    def drawMissile(self, superficie):
        superficie.blit(self.PictureMissile, self.rect);

class meteors(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self);
        self.meteor = ['meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big3.png', 
        'meteorGrey_big4.png', 'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png',
        'meteorGrey_small2.png', 'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png'];
        self.numRandom = randint(0,9);
        self.image = pygame.image.load('assets/{}'.format(self.meteor[self.numRandom])).convert();
        self.image.set_colorkey(BLACK);

        self.rect = self.image.get_rect();

        self.rect.x = randrange(width - self.rect.width);
        self.rect.y = randrange(-100,-40);
        self.speedy = 1;
        self.speedx = randrange(-1, 1);

    def update(self):
        self.rect.y += self.speedy;
        self.rect.x += self.speedx;

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.height > width + 25:
            self.rect.x = randrange(width - self.rect.width);
            self.rect.y = randrange(-100,-40);
            self.speedx = randrange(-1, 1);

def drawText(surface , text, size, posX, posY):
    font = pygame.font.SysFont("serif", size);
    text_surface = font.render(text, True, WHITE);
    text_rect = text_surface.get_rect();
    text_rect.midtop = (posX, posY);
    surface.blit(text_surface, text_rect);

all_meteor = pygame.sprite.Group();

def survive():
    pygame.init();
    pygame.mixer.init();
    pygame.display.set_caption('Shoot Badass');
    SCREEN = pygame.display.set_mode((width, height));
    BACKGROUND = pygame.image.load('assets/background.png').convert();

    laser_sound = pygame.mixer.Sound('assets/laser5.ogg');
    laserSound = True;
    explosion_sound = pygame.mixer.Sound('assets/explosion.wav');
    explosionSound = True;
    #music = pygame.mixer.Sound('assets/music.ogg');
    score = 0;
    bestScore = 0;

    player = naveSpacial();
    
    for i in range(8):
        meteoroide = meteors();
        all_meteor.add(meteoroide);

    #Bucle de actualizacion para la ventana creada anteriormente
    while True:
        player.move();

        if player.intruction:
            player.Life = 0;
            player.Live = False;

        if player.Life > 0:
            all_meteor.update();

        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                exit();

            if eventos.type == pygame.KEYDOWN:
                if player.Live:
                    if eventos.key == pygame.K_LEFT:
                        player.rect.left = player.rect.left - player.Speed;
                    elif eventos.key == pygame.K_RIGHT:
                        player.rect.right = player.rect.right + player.Speed;
                    elif eventos.key == pygame.K_DOWN:
                        player.rect.bottom = player.rect.bottom + player.Speed;
                    elif eventos.key == pygame.K_UP:
                        player.rect.top = player.rect.top - player.Speed;
                    elif eventos.key == pygame.K_s:
                        x,y = player.rect.center;
                        player.shoot(x,y);
                        laser_sound.play();
                        if laserSound: 
                            laser_sound.set_volume(0.8);
                        else:
                            laser_sound.stop();
                    elif eventos.key == pygame.K_a:
                        laserSound = False;
                    elif eventos.key == pygame.K_d:
                        explosionSound = False;
                else:
                    if eventos.key == pygame.K_r:
                        player.Life = 100;
                        player.Live = True;
                        score = 0;
                        player.rect.centery = height-40;
                        player.rect.centerx = width/2;
            
                if eventos.key and player.intruction:
                    player.intruction = False;
                    player.Life = 100;
                    player.Live = True;
                               
        SCREEN.blit(BACKGROUND, (0,0));
        player.drawNave(SCREEN);
        all_meteor.draw(SCREEN);

        hits = pygame.sprite.spritecollide(player, all_meteor, True);

        if hits:
            meteoroide = meteors();
            all_meteor.add(meteoroide);
            if player.Life > 0:
                player.Life = player.Life - 10;

        if player.Life == 0 and player.intruction == False:
            SCREEN.fill(BLACK);
            drawText(SCREEN, "La Nave ha sido destruida", 50, width/2, height/2);
            drawText(SCREEN, "Presiona 'r' para repetir", 20, width/2, height/2+50);
            player.Live = False;

            if bestScore < score or bestScore == 0:
                bestScore = score;

        if player.intruction:
            drawText(SCREEN, "Intrucciones", 50, width/2, height/2-60);
            drawText(SCREEN, "Si quieres solo silenciar los sonidos para jugar presiona 'A' y 'D'", 24, width/2, height/2+10);
            drawText(SCREEN, "Disparas con la 'S'", 20, width/2, height/2+50);
            drawText(SCREEN, "Te mueves con las flechas", 20, width/2, height/2+80);
            drawText(SCREEN, "Presiona cualquier tecla para comenzar", 20, width/2, height/2+120);
            drawText(SCREEN, "Nota: Siempre observa la vida, no te confies, ya que nunca sabras cuando puedas morir", 20, width/2, height-30);

        if len(player.ListMissile):
            for x in player.ListMissile:
                hits = pygame.sprite.spritecollide(x, all_meteor, True);
                x.drawMissile(SCREEN);
                x.trayectoria();

                if hits:
                    player.ListMissile.remove(x);
                    score = score + 1;
                    meteoroide = meteors();
                    all_meteor.add(meteoroide);
                    if explosionSound: 
                        explosion_sound.play();
                        explosion_sound.set_volume(0.2);
                    else:
                        explosion_sound.stop();

                if x.rect.top < -50:
                    player.ListMissile.remove(x);

        drawText(SCREEN, str(score), 30, width/2, 10);
        drawText(SCREEN, "Life: " + str(player.Life), 20, 760, 10);
        drawText(SCREEN, "Best Score: " + str(bestScore), 20, 70, 10);
        pygame.display.update();

survive();