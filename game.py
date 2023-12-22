import pygame
from sys import exit
import math
import textwrap
import random
from pygame import mixer

location = [0,0]
# initial location of spear at the top left corner

pygame.init()
pygame.display.set_caption("Spear Knight") #This names our game

width = 800
length = 600
screen = pygame.display.set_mode((width,length))

mixer.music.load("game_music.mp3")
mixer.music.set_volume(0.3)

background_image = pygame.image.load("Graphics/grassy.jpg")

# This creates our window

clock = pygame.time.Clock()

main_font = pygame.font.Font("Pixeltype.ttf", 50)
small_font = pygame.font.Font("Pixeltype.ttf", 25)

round_counter = 0  # Initialize the round counter

player_surface = pygame.transform.scale_by(pygame.image.load("Graphics/player_pos1.png").convert_alpha(),2)
player_rectangle = player_surface.get_rect(center = (400,300))
player_running =[pygame.image.load("Graphics/player_pos1.png"),
				pygame.image.load("Graphics/player_pos2.png"),
				pygame.image.load("Graphics/player_pos3.png"),
				pygame.image.load("Graphics/player_pos4.png"),
				pygame.image.load("Graphics/player_pos5.png"),
				pygame.image.load("Graphics/player_pos6.png"),
				pygame.image.load("Graphics/player_pos7.png")]

enemy_frame_size = (40, 40)  # Set the desired size for the enemy frames

enemy_frames = [pygame.transform.scale(pygame.image.load("Graphics/Slime1.png"), enemy_frame_size),
                pygame.transform.scale(pygame.image.load("Graphics/Slime2.png"), enemy_frame_size),
                pygame.transform.scale(pygame.image.load("Graphics/Slime3.png"), enemy_frame_size),
                pygame.transform.scale(pygame.image.load("Graphics/Slime4.png"), enemy_frame_size),
                pygame.transform.scale(pygame.image.load("Graphics/Slime5.png"), enemy_frame_size)]

projectle_frame_size = (20, 20)

projectle_frames = [pygame.transform.scale(pygame.image.load("Graphics/Projectle_1.png"), projectle_frame_size),
                    pygame.transform.scale(pygame.image.load("Graphics/Projectle_2.png"), projectle_frame_size),
                    pygame.transform.scale(pygame.image.load("Graphics/Projectle_3.png"), projectle_frame_size),
                    pygame.transform.scale(pygame.image.load("Graphics/Projectle_4.png"), projectle_frame_size)]

projectle_animation_frame = 0
projectle_animation_speed = 0.1  # Adjust this to change the speed of the projectle animation
last_projectle_animation_update = pygame.time.get_ticks()

enemy_animation_frame = 0
last_enemy_animation_update = pygame.time.get_ticks()
enemy_animation_speed = 0.1

current_frame = 0
animation_speed = 0.1  # Adjust this to change the speed of the animation
last_update = pygame.time.get_ticks()

spear = pygame.transform.scale_by(pygame.image.load("Graphics/spear.png").convert_alpha(),1)

hearts = 3
heart_surface = pygame.transform.scale_by(pygame.image.load("Graphics/heart.png").convert_alpha(), 5)

def enemy_goon(enemy_x,enemy_y,collided = False):
    global enemy_animation_frame
    enemy_surface = enemy_frames[enemy_animation_frame]  # Use the current frame
    enemy_rect = enemy_surface.get_rect(center = (enemy_x,enemy_y)) #The position of the enemy, at the centre.
    pos_diff_x = player_rectangle[0] - enemy_rect[0]
    pos_diff_y = player_rectangle[1] - enemy_rect[1]
    # difference between player and enemy position
    pos_vector = math.sqrt(pos_diff_x**2 + pos_diff_y**2)
    # two norm representing distance between player and enemy
    try:
        unit_pos = [pos_diff_x/pos_vector, pos_diff_y/pos_vector] #normalized x and y vector for the distance between the goon and the player
    except ZeroDivisionError:
        unit_pos = [0,0]
    screen.blit(enemy_surface, enemy_rect)
    info = [enemy_x, enemy_y, unit_pos[0], unit_pos[1], collided]
    if enemy_rect.colliderect(spear_rect):
        return info
    if enemy_rect.colliderect(player_rectangle):
        global hearts
        hearts -= 1
        collided = True
        return info
    return [-1,-1, unit_pos[0], unit_pos[1], collided]


def display_text(text, font, colour, x, y):
    text = font.render(text, False, colour)
    text_rect = text.get_rect(center = (x,y))
    screen.blit(text, text_rect)
# function to display text

def rules():
    full_rules = "Survive as many incoming enemy waves as possible! Controls: Use W, A, S, and D to move the player. Use Left-click to fire your spear."
    screen.fill("Light Pink")
    characters_in_line = 50
    # number of characters in each line
    lines = textwrap.wrap(full_rules, width = characters_in_line)
    # textwrap function creates a list of strings that are each 50 characters long
    line_number = 0
    while line_number < len(lines):
        display_text(lines[line_number], main_font, "Black", width/2, (length/2 - 200) + (line_number*50))
        line_number += 1
    # while loop that displays each line of the rules, and moves the text down by 50 pixels each time
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    return
        pygame.display.update()

def level_list(number):
    enemy_list = []
    count = 0
    while count < number:
        rand_num = random.randrange(1,5)
        if rand_num == 1:
            try:
                enemy_list.append(random.randrange(0,player_rectangle[0] - 100))
            except:
                enemy_list.append(random.randrange(player_rectangle[0] + 100, width))
            try:
                enemy_list.append(random.randrange(0,player_rectangle[1] - 100))
            except:
                enemy_list.append(random.randrange(player_rectangle[1] + 100, length))
        elif rand_num == 2:
            try:
                enemy_list.append(random.randrange(player_rectangle[0] + 100, width))
            except:
                enemy_list.append(random.randrange(0,player_rectangle[0] - 100))
            try:
                enemy_list.append(random.randrange(0,player_rectangle[1] - 100))
            except:
                enemy_list.append(random.randrange(player_rectangle[1] + 100, length))
        elif rand_num == 3:
            try:
                enemy_list.append(random.randrange(0,player_rectangle[0] - 100))
            except:
                enemy_list.append(random.randrange(player_rectangle[0] + 100, width))
            try:
                enemy_list.append(random.randrange(player_rectangle[1] + 100, length))
            except:
                enemy_list.append(random.randrange(0,player_rectangle[1] - 100))
        elif rand_num == 4:
            try:
                enemy_list.append(random.randrange(player_rectangle[0] + 100, width))
            except:
                enemy_list.append(random.randrange(0,player_rectangle[0] - 100))
            try:
                enemy_list.append(random.randrange(player_rectangle[1] + 100, length))
            except:
                enemy_list.append(random.randrange(0,player_rectangle[1] - 100))
        count += 1
    return enemy_list

def enemy_fire(enemy_x,enemy_y, player_x, player_y):
    global projectle_animation_frame, last_projectle_animation_update
    now = pygame.time.get_ticks()
    if now - last_projectle_animation_update > projectle_animation_speed * 1000:
        last_projectle_animation_update = now
        projectle_animation_frame = (projectle_animation_frame + 1) % len(projectle_frames)
    x_diff_missile = player_x - enemy_x
    y_diff_missile = player_y - enemy_y
    missile_norm = math.sqrt(x_diff_missile**2 + y_diff_missile**2)
    if (x_diff_missile > 0 and y_diff_missile >0):
        missile_angle = -math.degrees(math.atan2(y_diff_missile,x_diff_missile)) - 90
    elif (x_diff_missile > 0 and y_diff_missile < 0):
        missile_angle = 90 - math.degrees(math.atan2(y_diff_missile,x_diff_missile))
    elif (x_diff_missile < 0 and y_diff_missile < 0):
        missile_angle = 90 - math.degrees(math.atan2(y_diff_missile,x_diff_missile))
    elif (x_diff_missile < 0 and y_diff_missile > 0):
        missile_angle = 90 - math.degrees(math.atan2(y_diff_missile,x_diff_missile))
    #note negative angles from a negative x or y and a positive x or y
    rotated_missile = pygame.transform.rotate(projectle_frames[projectle_animation_frame], missile_angle)
    return [rotated_missile,x_diff_missile/missile_norm, y_diff_missile/missile_norm]

movement_speed = 5  # Default movement speed
attack_speed = 1000  # Default attack speed in milliseconds
last_attack_time = 0
spear_speed = 10

def offer_power_ups(round_counter):
    global hearts, movement_speed, spear_speed
    if round_counter % 3 == 0:
        power_up_text = "Choose a Power-Up: 1 for Movement Speed, 2 for Extra Heart, 3 for Attack Speed"
        characters_in_line = 40  # Number of characters in each line
        lines = textwrap.wrap(power_up_text, width=characters_in_line)  # Wrap the text

        line_number = 0
        while line_number < len(lines):
            display_text(lines[line_number], main_font, "Black", width / 2, (length / 2) + (line_number * 50))
            line_number += 1

        selected = False
        while not selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        movement_speed += 0.3 # Increase movement speed
                        selected = True
                    elif event.key == pygame.K_2:
                        hearts += 1  # Add an extra heart
                        selected = True
                    elif event.key == pygame.K_3:
                        spear_speed += 3
                        selected = True
            pygame.display.update()

x_diff = 0
y_diff = 0
angle = 0

vector = 0
pressed = False
airborne = False
firing = False
original_pos = [0,0]
missileTimer = 0
locationOfEnemies = []
missileAirborne = False
missileSpawnRate = 50
isLost = False
round_counter = 0
nullifiedMissiles = []
EnemiesNow = 0
# variables

game_active = False

direction = "east"

inLevel1 = 0

level1 = False

while True:

    if game_active == True:

        if level1 == False:
            round_counter += 1  # Increment round counter
            offer_power_ups(round_counter)  # Offer power-ups based on the round
            level1 = True

        now = pygame.time.get_ticks()

        screen.blit(background_image, (0, 0))
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_rectangle.top -= movement_speed
        if keys[pygame.K_a]:
            player_rectangle.left -= movement_speed
        if keys[pygame.K_d]:
            player_rectangle.right += movement_speed
        if keys[pygame.K_s]:
            player_rectangle.bottom += movement_speed
        # movement controls

        if player_rectangle.top <= 0:
            player_rectangle.top = 0
        if player_rectangle.left <= 0:
            player_rectangle.left = 0
        if player_rectangle.right >= width:
            player_rectangle.right = width
        if player_rectangle.bottom >= length:
            player_rectangle.bottom = length
            
        if now - last_update > animation_speed * 1000:
            last_update = now
            current_frame = (current_frame + 1) % len(player_running)
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_w]:
                player_surface = pygame.transform.scale(player_running[current_frame], (40, 40))
            else:
                # Reset to default image when not moving
                player_surface = pygame.transform.scale(pygame.image.load("Graphics/player_pos1.png"), (40, 40))
        if now - last_enemy_animation_update > enemy_animation_speed * 1000:
            last_enemy_animation_update = now
            enemy_animation_frame = (enemy_animation_frame + 1) % len(enemy_frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   #uninitializes pygame when you press x on the screen
                exit() #exits the while loop to end the script
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
        if level1 == False:
            round_counter += 1
            level1 = True

        mouse = pygame.mouse.get_pos()
        # gets position of mouse
        
        if pygame.mouse.get_pressed()[0] and airborne == False:
            x_diff = -(player_rectangle[0]+32 - mouse[0])
            # checks the x-axis difference between your mouse and the location of player
            y_diff = player_rectangle[1]+32 - mouse[1]
            # checks the y-axis difference between your mouse and the location of player
            airborne = True
            # stops spear from moving after you've clicked once
            location = [player_rectangle[0]+32, player_rectangle[1]+32]
            # resets location of spear to player's center
            original_pos = [player_rectangle[0]+32, player_rectangle[1]+32]
            # resets original thrown position of spear to player's center
            
        if(hearts <= 0):
            screen.fill("Light Blue")
            lose_text = "You Lost! " + str(round_counter-1) + " Rounds Completed."
            lose_surf = main_font.render(f'{lose_text}', False, "Black")
            lose_rect = lose_surf.get_rect(center = (width/2, length/2))
            screen.blit(lose_surf, lose_rect)
            isLost = True

        angle = math.degrees(math.atan2(y_diff,x_diff))
        # stores the angle between the positive x-axis and your mouse
        rotated_spear = pygame.transform.rotate(spear, angle)
        # creates a spear that's rotated to where your mouse is
        spear_rect = rotated_spear.get_rect(center = location)
        # creates a rectangle around the rotated spear
        
        two_norm = math.sqrt(x_diff**2 + y_diff**2)
        # distance between your mouse and the location of the spear
        try:
            unit_x = x_diff / two_norm
        except: 
            unit_x = 0
        try:
            unit_y = y_diff / two_norm
        except:
            unit_y = 0
        # normalizing the spear shot direction vectors to make things consistent

        spear_x = -(original_pos[0] - location[0])
        spear_y = original_pos[1] - location[1]
        # variables containing the x-axis and y-axis distance from the throwing location

        location_vector = math.sqrt(spear_x**2 + spear_y**2)
        # two norm vector representing spear's distance from thrown point

        if airborne == True:
            if location[0] >= 0 and location[0] <= width:
                if location[1] >= 0 and location[1] <= length:
                    location[0] += spear_speed * unit_x
                    location[1] -= spear_speed * unit_y
                    screen.blit(rotated_spear, ((spear_rect[0] + 50*unit_x),(spear_rect[1] - 50*unit_y)))
                    # creates an offset from the center of the player
                # if the spear is within 300 pixels of the player, it will move towards the clicked location

        if mouse[0] > player_rectangle[0]+32:
            direction = "east"
        else:
            direction = "west"
        # changes direction of player when throwing spear

        if direction == "east":
            screen.blit(player_surface, player_rectangle)
        elif direction == "west":
            screen.blit(pygame.transform.flip(player_surface,True,False), player_rectangle)
        # blits player on screen based off which way they are facing


        if location[0] < 0 or location[0] > width or location[1] < 0 or location[1] > length:
                airborne = False
        # allows another click to throw again if the spear is more than 300 pixels away from the player
        
        for i in range(hearts):
            screen.blit(heart_surface, (25 + (i*50),25))

        #this blits the position of the enemy
        if level1 == True and not isLost:
            enemies = 0
            if inLevel1 == 0:
                inLevel1 = 1
                level_1_enemies = level_list(round_counter)
                missileAirborne = False

            while enemies < int(len(level_1_enemies)/2):

                tracker = enemy_goon(level_1_enemies[2*enemies], level_1_enemies[2*enemies+1])
                if tracker[0] in level_1_enemies or tracker[4]: 
                    level_1_enemies.remove(tracker[0])
                if tracker[1] in level_1_enemies or tracker[4]:
                    level_1_enemies.remove(tracker[1])
                try:
                    enemy_goon(level_1_enemies[2*enemies], level_1_enemies[2*enemies+1])
                except:
                    1
                
                if(missileTimer % missileSpawnRate == 0 and missileAirborne == False):
                    locationOfEnemies = level_1_enemies[:]
                    currentPlayerLocation = [player_rectangle[0],player_rectangle[1]]
                    missileAirborne = True  
                    if(len(level_1_enemies) != 0):
                        EnemiesNow = len(level_1_enemies)/2 
                    
                
                try:
                    level_1_enemies[2*enemies] +=  (2 + 0.01 *round_counter) * tracker[2]
                    level_1_enemies[2*enemies+1] +=  (2 + 0.01 *round_counter) * tracker[3]
                    #goons go toward the player by a speed of 2, on the next loop, this will be displayed
                except:
                    1    

                enemies +=1
                
                
            if(len(locationOfEnemies) == 0 and len(nullifiedMissiles) == 0 and len(level_1_enemies) == 0):
                missileAirborne = False
                missileTimer = 0
                level1 = False
                inLevel1 = 0                        
                
            if(level1):
                for enemy in range(0,len(locationOfEnemies),2):
                    missile_data = enemy_fire(locationOfEnemies[enemy],locationOfEnemies[enemy+1],currentPlayerLocation[0],currentPlayerLocation[1])
                    missile = missile_data[0]
                    missile_direction_x = missile_data[1] *(2 + 0.13 * round_counter)
                    missile_direction_y = missile_data[2] *(2 + 0.13 * round_counter)
                    missile_rect = missile.get_rect(center = (locationOfEnemies[enemy] + (missileTimer-missileSpawnRate)*1.3*missile_direction_x, locationOfEnemies[enemy+1]+ (missileTimer-missileSpawnRate)*1.3*missile_direction_y))
                    if(enemy in nullifiedMissiles): None
                    elif(0<missile_rect.x and missile_rect.x <800 and 0<missile_rect.y and missile_rect.y<600):
                        if(missile_rect.colliderect(player_rectangle)):
                            hearts -= 1
                            nullifiedMissiles.append(enemy)
        
                        else: screen.blit(missile, missile_rect)
                    else:
                        nullifiedMissiles.append(enemy)
                        
            if(len(nullifiedMissiles) == EnemiesNow):
                if len(level_1_enemies) == 0:
                    level1 = False
                    inLevel1 = 0
                locationOfEnemies = []
                missileAirborne = False
                nullifiedMissiles = []
                missileTimer = 0
                numberEnemiesOnScreen = 0
            
        
        display_text(f"Wave: {round_counter}", main_font, "Black", width - 110, 70)
        display_text("Health: " + str(hearts), small_font, "Black", width - 110, 100)
        display_text("Speed: " + str(movement_speed), small_font, "Black", width - 110, 130)
        display_text("Attack Speed: " + str(spear_speed), small_font, "Black", width - 110,  160)

        pygame.display.update() 
        #displays surface that we blit

        clock.tick(60) 
        #frames per second
        missileTimer+=1

    else:
        screen.fill("Light Blue")
        play_text = "Press SPACE to Play"
        rules_text = "Press TAB to View Rules"
        play_surf = main_font.render(f'{play_text}',False,"Black")
        play_rect = play_surf.get_rect(center = (width/2,length/2))
        rules_surf = main_font.render(f'{rules_text}',False,"Black")
        rules_rect = rules_surf.get_rect(midtop = (width/2,((length/2) +50 )))
        screen.blit(play_surf, play_rect)
        screen.blit(rules_surf, rules_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    mixer.music.play(-1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    rules()
                
        pygame.display.update()