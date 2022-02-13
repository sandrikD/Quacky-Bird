import pygame
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Quacky Bird')

#main menu
def menu():
    image = pygame.image.load('Game Images\mainmenu.png')
    image = pygame.transform.scale(image, (640,480))

    #game loop
    while True:
        screen.blit(image,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(0,640) and event.pos[1] in range(0,480):
                    chooseYourCharacter()

#character selection
def chooseYourCharacter():
    
    image = pygame.image.load('Game Images\choose_your_fighter.png')
    image = pygame.transform.scale(image, (640,480))

    while True:
        screen.blit(image,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #top left character (psyduck)
                if event.pos[0] in range(0,182) and event.pos[1] in range(0,194):
                    ChooseDifficulty(0)
        
                #top right character (donald duck)
                elif event.pos[0] in range (458,640) and event.pos[1] in range(0,194):
                    ChooseDifficulty(1)
                
                #bottom left character (green duck)
                elif event.pos[0] in range (0,211) and event.pos[1] in range(264,480):
                    ChooseDifficulty(2)
                    
                #bottom right character (farfetch'd)
                elif event.pos[0] in range (458,640) and event.pos[1] in range(264,480):
                    ChooseDifficulty(3)
                
def ChooseDifficulty(character):
    image = pygame.image.load('Game Images\difficulty.png')
    image = pygame.transform.scale(image, (640,480))
    while True:
        screen.blit(image,(0,0))
        pygame.display.update()
        for event in pygame.event.get(): 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #easy difficulty
                if event.pos[0] in range (74,566) and event.pos[1] in range (143,245):
                    game(character,0)

                #medium difficulty
                if event.pos[0] in range (74,566) and event.pos[1] in range (245,347):
                    game(character,1)
                
                #Hard Difficulty
                if event.pos[0] in range (74,566) and event.pos[1] in range (347,449):
                    game(character,2)

def game(character, difficulty):
    #background images
    
    mixer.init()
    mixer.music.load('Sounds/StarSong.wav')
    mixer.music.set_volume(0.05)
    mixer.music.play(-1)

    image = pygame.image.load('Game Images\mtn_background.png') 
    image = pygame.transform.scale(image, (640,480))
    bgx = 0
    print (character)

    #change character image 
    if character == 0:
        player = pygame.image.load('Game Images\Psyduck.png')
        player = pygame.transform.rotozoom(player,0,0.4)
        crate = pygame.image.load('Game Images\pikachu.png') #obstacles photo 
        crate = pygame.transform.rotozoom(crate,0,0.2)

    elif character ==1:
        player = pygame.image.load('Game Images\donald_duck.png')
        player = pygame.transform.rotozoom(player,0,0.25)
        crate = pygame.image.load('Game Images\daffy_duck.png') #obstacles photo 
        crate = pygame.transform.rotozoom(crate,0,0.4)

    elif character ==2:
        player = pygame.image.load('Game Images\green_duck.png')
        player = pygame.transform.rotozoom(player,0,0.4)
        crate = pygame.image.load('Game Images\croc.png') #obstacles photo 
        crate = pygame.transform.rotozoom(crate,0,0.4)
        
    elif character ==3:
        player = pygame.image.load('Game Images\Farfetchd.png')
        player = pygame.transform.rotozoom(player,0,0.4)   
        crate = pygame.image.load('Game Images\zapdos.png') #obstacles photo 
        crate = pygame.transform.rotozoom(crate,0,0.7)

    coin = pygame.image.load('Game Images\coin.png')
    coin = pygame.transform.rotozoom(coin,0,0.2)
    
    #variables begin
    player_y = 350
    gravity = 0.8
    jumpcount = 0
    jump = 0
    crate_x=700
    coin_x = 700
    coin_y=250
    coin_speed = 0.5
    coin_count = 0

    #change diff based on selection
    if difficulty == 0:
        crate_speed = 0.5
    elif difficulty == 1:
        crate_speed = 0.7
    elif difficulty == 2:
        crate_speed = 0.9

    spikes = pygame.image.load('Game Images\spikes.png')
    spikes = pygame.transform.rotozoom(spikes,0,0.5)
    
    #run game
    while True:
        #display background
        
        mixer.init()
        screen.blit(image,(bgx-640,0))
        screen.blit(image,(bgx,0))
        screen.blit(image,(bgx+640,0))

        #side scroll background
        bgx = bgx - 0.5 
        if bgx <= -640:
            bgx = 0

        #player jump
        p_rect = screen.blit(player,(50,player_y))
        
        if player_y < 350:
            player_y  += gravity 
        
        if jump == 1:
            player_y = player_y - 2.5
            jumpcount += 1
            if jumpcount > 50:  
                jumpcount = 0
                jump = 0
                
        #obstacle
        c_rect = screen.blit(crate,(crate_x,350))
        crate_x -= crate_speed
        if crate_x<-50:
            crate_x = random.randint(700,800)
        
        #upper obstacle (spikes)
        spike_rect = screen.blit(spikes,(0,0))
        spike_rect2 = screen.blit(spikes,(366,0))

        if p_rect.colliderect(spike_rect):
             lose()

        #coins
        coin_rect = screen.blit(coin,(coin_x,coin_y))
        coin_x -= coin_speed
        if coin_x<-500:
            coin_x = random.randint(700,800)
            coin_y = random.randint(100,250)
            coin_speed = 0.5
        
        #obstacle collision
        if p_rect.colliderect(c_rect):
            lose() 
            
        #Coin collision
        font = pygame.font.Font('freesansbold.ttf',32)
        if p_rect.colliderect(coin_rect):
            coin_x = random.randint(700,800)
            coin_y = random.randint(100,250)
            coin_count += 1
            print ('Coins collected: ', coin_count)

            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = image.get_rect()

            rec = pygame.image.load('Game Images\Rec.png')
            rec = pygame.transform.rotozoom(rec,0,0.2)

            coinText = font.render("%d"%tuple([coin_count]),1,(10))
            sprite.image.blit(rec,(200,100))
            sprite.image.blit(coinText, (221,106))
        
        #updates display
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                jump = 1
                quack = mixer.Sound('Sounds\DuckSound.wav')
                mixer.Sound.set_volume(quack, 0.1)
                mixer.Sound.play(quack)
                                
def lose():
    image = pygame.image.load('Game Images\loser.jpg')
    image = pygame.transform.scale(image, (640,480))
    wario= mixer.Sound('Sounds\Wario.wav')
    mixer.music.stop()
    mixer.Sound.set_volume(wario, 0.8)
    mixer.Sound.play(wario)

    while True:
        screen.blit(image,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(0,640) and event.pos[1] in range(0,480):               
                    menu()
            
menu()
chooseYourCharacter()
lose()
 