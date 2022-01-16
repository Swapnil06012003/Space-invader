import random
import threading
import math
import pygame
from pygame import mixer
pygame.init()
pygame.display.set_caption("Space invader")
screen_width=1500
screen_height=800
screen=pygame.display.set_mode((screen_width,screen_height))
background=pygame.image.load("bgimg.jpg")
start_game=1
start_game1=False
pygame.display.update()
white=(255,255,255)
red=(255,0,0)
while not start_game1:
    font = pygame.font.Font(None, 30)
    over_font = pygame.font.Font(None, 50)
    background1 = pygame.image.load("backimg.jpg")
    background1 = pygame.transform.scale(background1, (1500, 800))
    screen.blit(background1, (0, 0))
    over2=over_font.render("Press enter to start the game",True,(255,255,255))
    screen.blit(over2,(450,620))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                if start_game==1:
                    mixer.music.load('background.wav')
                    mixer.music.play(-1)
                    player_img=pygame.image.load('space-invaders.png')
                    player_bullet=pygame.image.load('bullet.png')
                    player_img=pygame.transform.scale(player_img,(80,80))
                    background=pygame.transform.scale(background,(1500,800))
                    player_bullet=pygame.transform.scale(player_bullet,(40,40))
                    clock = pygame.time.Clock()
                    fps = 60
                    x=700
                    y=630
                    bullet_1x=0
                    bullet_1y=630
                    bullet_velocity=-5
                    bullet_state="ready"
                    exit_game=False
                    velocity=0
                    enemy=[]
                    enemy_pic=[]
                    enemy_x=[]
                    enemy_y=[]
                    enemy_velocity=[]
                    num_of_enemies=10
                    game_over_var=False
                    for i in range(num_of_enemies):
                        enemy.append(pygame.image.load('ufo.png'))
                        enemy_pic.append(pygame.transform.scale(enemy[i],(80,80)))
                        enemy_x.append(random.randint(200,1300))
                        enemy_y.append(random.randint(100,200))
                        enemy_velocity.append(2)
                    score_value=0
                    font=pygame.font.Font(None,60)
                    over_font=pygame.font.Font(None,100)
                    textX=10
                    texty=10
                    q=0
                    with open("highscore_space_invader.txt", "r") as f:
                        hiscore = f.read()
                    def show_score(x,y):
                        score=font.render("Score: "+ str(score_value),True,(255,0,0))
                        screen.blit(score,(x,y))

                    def fire_bullet(x,y):
                        global bullet_state
                        bullet_state="fire"
                        screen.blit(player_bullet,(x+20,y-35))

                    def enemy_def(x,y,i):
                        if q==0:
                            screen.blit(enemy_pic[i],(x,y))
                    def player(x,y):
                        screen.blit(player_img,(x,y))
                    def collision(bullet_1x,bullet_1y,enemy_x,enemy_y,i):
                        dis= math.sqrt((math.pow(bullet_1x - enemy_x[i], 2)) + (math.pow(bullet_1y - enemy_y[i], 2)))
                        if dis<50:
                            return True
                        else:
                            return False
                    def game_over():
                        global bullet_state
                        over = over_font.render("        GAME OVER", True, (255, 0, 0))
                        over1=over_font.render("           Score: "+str(score_value),True,(255,255,255))
                        over2=over_font.render("         Hiscore: "+str(hiscore),True,(255,255,255))
                        screen.blit(over2,(400,450))
                        screen.blit(over, (400, 250))
                        screen.blit(over1,(400,350))


                        bullet_state="ready"
                    start_font=pygame.font.Font(None,100)
                    start=start_font.render("Press enter to start",True,(255,0,0))
                    screen.blit(start,(520,400))
                    pygame.display.update()
                    while not exit_game:
                        screen.blit(background, (0, 0))
                        if game_over_var==True:
                            with open("highscore_space_invader.txt", "w") as f:
                                f.write(str(hiscore))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:  # if user press the close key
                                exit_game = True
                            if event.type==pygame.KEYDOWN:
                                if event.key == pygame.K_RIGHT:
                                    velocity=5
                                    pygame.display.update()
                                if event.key==pygame.K_LEFT:
                                    velocity=-5
                                    pygame.display.update()
                                if bullet_state == "ready":
                                    if event.key==pygame.K_SPACE:
                                        bullet_1x=x
                                        fire_bullet(bullet_1x,bullet_1y)
                                        bullet_sound=mixer.Sound("laser.wav")
                                        bullet_sound.play()
                                if event.key==pygame.K_RETURN:
                                    score_value+=50

                        if x<0:
                            x=0
                        elif x>1420:
                            x=1420
                        for i in range(num_of_enemies):
                            if enemy_y[i]>500:
                                for j in range(num_of_enemies):
                                    enemy_y[j]==2000
                                    enemy_x[j]==2000
                                    q=1
                                    x = 700
                                    y = 630
                                game_over_var=True
                                game_over()
                                break
                            if enemy_x[i]<0:
                                enemy_velocity[i]=-enemy_velocity[i]
                                enemy_y[i]+=20
                            elif enemy_x[i]>1450:
                                enemy_velocity[i]=-enemy_velocity[i]
                                enemy_y[i] += 40
                            enemy_x[i]+= enemy_velocity[i]
                            iscollision = collision(bullet_1x, bullet_1y, enemy_x, enemy_y,i)
                            if iscollision is True:
                                fps+=3
                                bullet_state = "ready"
                                collision_sound = mixer.Sound("explosion.wav")
                                collision_sound.play()
                                bullet_1y = y
                                enemy_x[i] = random.randint(200, 1300)
                                enemy_y[i] = random.randint(100, 200)
                                score_value += 10
                            enemy_x[i] +=enemy_velocity[i]
                            enemy_def(enemy_x[i], enemy_y[i],i)
                        if bullet_1y<=0:
                            bullet_1y=630
                            bullet_state="ready"
                        if bullet_state == "fire":
                            fire_bullet(bullet_1x,bullet_1y)
                            bullet_1y+=bullet_velocity
                        x+=velocity
                        player(x,y)
                        show_score(textX,texty)
                        if score_value>int(hiscore):
                            hiscore=score_value
                        pygame.draw.rect(screen, red, [0, 580, 20, 5])
                        pygame.draw.rect(screen, red, [1480, 580, 20, 5])
                        pygame.display.update()
                        clock.tick(fps)

                    pygame.quit()
                    quit()
