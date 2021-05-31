import pygame
import os
import random
pygame.init()

WIDTH = 600
HEIGHT = 900
BABA_WIDTH = 70
BABA_HEIGHT = 100

FPS = 60
FramePerSec = pygame.time.Clock()
VELOCITY = 5

BACKGROUND_IMAGE = pygame.image.load(os.path.join('assets','background.png'))
# setting the size of the program window
DISP = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("GEIM")
# pretty much all fonts
FONT_ALL = pygame.font.SysFont('comicsans', 70)

# User events - when baba catches a pill or when he gets caught by the police
PILL_CATCH = pygame.USEREVENT + 1
GET_CAUGHT = pygame.USEREVENT + 2


#All images ingame
BABA_IMAGE = pygame.image.load(os.path.join('assets','baba.png'))
BABA = pygame.transform.scale(BABA_IMAGE,(BABA_WIDTH,BABA_HEIGHT))

HANDCUFFS_IMAGE = pygame.image.load(os.path.join('assets','handcuffs.png'))
HANDCUFFS = pygame.transform.scale(HANDCUFFS_IMAGE,(90,55))

PILL_IMAGE = pygame.image.load(os.path.join('assets','pill.png'))
PILL = pygame.transform.scale(PILL_IMAGE,(70,50))



def draw_window(baba,score,pills,handcuffs):
    DISP.blit(BACKGROUND_IMAGE,(0,0))
    DISP.blit(BABA,(baba.x,baba.y)) # drawing a surface on a screen
    
    score_render = FONT_ALL.render(str(score),1,(255,255,255))
    DISP.blit(score_render,(WIDTH-score_render.get_width()-10,10))

    for pill in pills:
        DISP.blit(PILL,(pill.x,pill.y))
    
    for handcuff in handcuffs:
        DISP.blit(HANDCUFFS,(handcuff.x,handcuff.y))

    pygame.display.update()

def get_caught(highscore):
    draw_text = FONT_ALL.render("YOU GOT CAUGHT", 1, (255,255,255))
    highscore_text = FONT_ALL.render("NEW HIGHSCORE: "+ str(highscore),1,(255,255,255))
    DISP.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    DISP.blit(highscore_text,(WIDTH/2 - highscore_text.get_width()/2, HEIGHT/2+draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(7000)

def pills_falling(pills,baba,handcuffs):
    for pill in pills:
        random_vel = random.randint(1,7)
        pill.y += random_vel
        if baba.colliderect(pill):
            pygame.event.post(pygame.event.Event(PILL_CATCH))
            pills.remove(pill)
        elif pill.y > HEIGHT:
            pills.remove(pill)
        
    for handcuff in handcuffs:
        random_vel = random.randint(1,7)
        handcuff.y += random_vel
        if baba.colliderect(handcuff):
            pygame.event.post(pygame.event.Event(GET_CAUGHT))
            handcuffs.remove(handcuff)
        elif handcuff.y > HEIGHT:
            handcuffs.remove(handcuff)



def movement(baba,keys_pressed):
    if keys_pressed[pygame.K_a] and baba.x > 0: # left
        baba.x -= VELOCITY
    elif keys_pressed[pygame.K_d] and baba.x < WIDTH-BABA_WIDTH: # right
        baba.x += VELOCITY


def main():
    baba = pygame.Rect(270,790,55,100)
    pills = []
    score = 0
    handcuffs = []
    run = True
    highscore = 0
    while run:
        FramePerSec.tick(FPS) #refresh rate
        for event in pygame.event.get(): #makes sure that when the user presses X, the program quits working and closes
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            random_x = random.randint(0,WIDTH-70)
            random_y = random.randint(-3000,-50)

            if len(pills) < 20:
                pill = pygame.Rect(random_x,random_y,70,50)
                pills.append(pill)
            if len(handcuffs) < 5:
                random_x = random.randint(0,WIDTH-70)
                random_y = random.randint(-3000,-50)
                handcuff = pygame.Rect(random_x,random_y,90,55)
                handcuffs.append(handcuff)
            if event.type == PILL_CATCH:
                score += 1
            if event.type == GET_CAUGHT:
                if score > highscore:
                    highscore = score
                get_caught(highscore)
                pills =[]
                handcuffs =[]
                score = 0
            pygame.display.update()
        keys_pressed = pygame.key.get_pressed()
        movement(baba,keys_pressed)
        pills_falling(pills,baba,handcuffs)
        draw_window(baba,score,pills,handcuffs)
        

    
    main()


if __name__ == "__main__":
    main()