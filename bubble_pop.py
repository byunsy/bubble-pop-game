"""----------------------------------------------------------------------------
TITLE       : bubble_pop.py
BY          : Sang Yoon Byun
DESCRIPTION : A classic arcade game recreated using pygame
REFERENCES  : At the bottom of the page
----------------------------------------------------------------------------"""

# Import pygame
import pygame
import random

"""----------------------------------------------------------------------------
0. SET UP REQUIREMENTS
----------------------------------------------------------------------------"""
# Initialize first
pygame.init()

# Set screen size
screen_width  = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set screen title
pygame.display.set_caption("Bubble Pop: The Caveman")

# Initialize clock for setting frames per second (FPS)
clock = pygame.time.Clock()

"""----------------------------------------------------------------------------
1. BACKGROUND + STAGE
----------------------------------------------------------------------------"""

# Set the background
background = pygame.image.load("./Projects/bubble_pop/images/background.png")

# Set the stage
stage        = pygame.image.load("./Projects/bubble_pop/images/ground.png")
stage_size   = stage.get_rect().size
stage_height = stage_size[1]

"""----------------------------------------------------------------------------
2. SET UP PROTAGONIST
----------------------------------------------------------------------------"""

# Set the protagonist
protagonist = (pygame.image
               .load("./Projects/bubble_pop/images/character_left.png"))

protag_size = protagonist.get_rect().size

# Attain width and height of protagonist
protag_width  = protag_size[0]
protag_height = protag_size[1]

# Calculate initial position for protagonist
protag_x_pos = (screen_width / 2) - (protag_width / 2)
protag_y_pos = screen_height - (protag_height + stage_height)

# Repositioning coordinates
protag_to_x = 0
to_y = 0

# Set protagonist speed
protag_speed = 12

"""----------------------------------------------------------------------------
3. SET UP WEAPONS
----------------------------------------------------------------------------"""

# Set up weapons
weapon      = pygame.image.load("./Projects/bubble_pop/images/spear.png")
weapon_size = weapon.get_rect().size

weapon_width  = weapon_size[0]
weapon_height = weapon_size[1]

# Create a list for handling multiple weapons
weapons = []

# Set weapon speed
weapon_speed = 10

# Set weapon count
weapon_cnt = 20

"""----------------------------------------------------------------------------
4. SET UP BUBBLES
----------------------------------------------------------------------------"""

# Load images for different sizes of bubbles
bubble_img = [
    pygame.image.load("./Projects/bubble_pop/images/bubble1.png"),
    pygame.image.load("./Projects/bubble_pop/images/bubble2.png"),
    pygame.image.load("./Projects/bubble_pop/images/bubble3.png"),
    pygame.image.load("./Projects/bubble_pop/images/bubble4.png"),
]

# Different bubble speed for different sizes
bubble_speed_y = [-18, -15, -12, -9]

# Create a list for different sizes of bubbles
bubbles = []

# Creating the original big bubble (as a dictionary)
bubbles.append({
    "pos_x": 50,                          # bubble x coordinate
    "pos_y": 50,                          # bubble y coordinate
    "img_index": 0,                       # Type (size) of bubble
    "to_x": 3,                            # bubble x-movement
    "to_y": -6,                           # bubble y-movement
    "init_spd_y": bubble_speed_y[0]       # Initial y speed
})

# Initial weapons status when collided with bubbles
weapon_removal = -1
bubble_removal = -1

"""----------------------------------------------------------------------------
5. OTHER ADDITIONAL SETUPS
----------------------------------------------------------------------------"""

# Set up text information
game_font_1 = pygame.font.SysFont('impact', 30)
game_font_2 = pygame.font.SysFont('impact', 20)

# Set up game time limit
game_time = 100

# Set up start time for timer
start_ticks = pygame.time.get_ticks()

# Set up game result message
game_result = ""

"""----------------------------------------------------------------------------
6. HANDLING EVENTS
----------------------------------------------------------------------------"""

# Event Loop
running = True   # boolean: is the game running?

while running:

    dt = clock.tick(30)

    # checking every individual event
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:     # if type is quit (eg. clicking X)
            running = False               # then quit.

        # if certain keys are pressed
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                protagonist = pygame.image.load("./Projects/bubble_pop/images/character_left.png")
                protag_to_x -= protag_speed

            elif event.key == pygame.K_RIGHT:
                protagonist = pygame.image.load("./Projects/bubble_pop/images/character_right.png")
                protag_to_x += protag_speed

            elif event.key == pygame.K_SPACE:
                if weapon_cnt != 0:
                    weapon_x_pos = (protag_x_pos +
                                (protag_width / 2) - (weapon_width / 2))
                    weapon_y_pos = protag_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])
                    weapon_cnt -= 1

        # if arrow keys are un-pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                protag_to_x = 0

    """----------------------
    PROTAGONIST 
    ----------------------"""
    # Reposition the protagonist with updated positions
    protag_x_pos += protag_to_x

    # Make sure the protagonist stays within the screen
    if protag_x_pos < 0:
        protag_x_pos = 0

    if protag_x_pos > screen_width - protag_width:
        protag_x_pos = screen_width - protag_width

    # Updating element position
    protag_rect      = protagonist.get_rect()  # get rect information
    protag_rect.left = protag_x_pos            # put in x position
    protag_rect.top  = protag_y_pos            # put in y position

    """----------------------
    WEAPONS
    ----------------------"""
    # For every weapon in weapons, only change y_pos by weapon_speed
    # w[0]: weapon_x_pos remains unchanged 
    # w[1]: weapon_y_pos - weapon_speed
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ]

    # When a weapon touches the ceiling, it disappears
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0 ]

    """----------------------
    BubbleS
    ----------------------"""
    # Set bubble position for each bubble
    for bubble_index, bubble_val in enumerate(bubbles):

        # get bubble initial values
        bubble_x_pos   = bubble_val["pos_x"]
        bubble_y_pos   = bubble_val["pos_y"]
        bubble_img_idx = bubble_val["img_index"]

        # get bubble size
        bubble_size   = bubble_img[bubble_img_idx].get_rect().size
        bubble_width  = bubble_size[0]
        bubble_height = bubble_size[1]

        # bubbles bounce off the walls
        if bubble_x_pos < 0 or bubble_x_pos > screen_width - bubble_width:
            bubble_val["to_x"] = bubble_val["to_x"] * -1

        # bubbles bounce on the floor (stage)
        if bubble_y_pos > screen_height - stage_height - bubble_height:
            bubble_val["to_y"] = bubble_val["init_spd_y"]
        else:
            bubble_val["to_y"] += 0.5

        bubble_val["pos_x"] += bubble_val["to_x"]
        bubble_val["pos_y"] += bubble_val["to_y"]

    """----------------------
    COLLISIONS
    ----------------------"""
    # Update protagonist rect information
    protag_rect      = protagonist.get_rect()
    protag_rect.left = protag_x_pos
    protag_rect.top  = protag_y_pos

     # Looking at each bubble
    for bubble_index, bubble_val in enumerate(bubbles):

        # get bubble initial values
        bubble_x_pos   = bubble_val["pos_x"]
        bubble_y_pos   = bubble_val["pos_y"]
        bubble_img_idx = bubble_val["img_index"]

        # update bubble rect information
        bubble_rect      = bubble_img[bubble_img_idx].get_rect()
        bubble_rect.left = bubble_x_pos
        bubble_rect.top  = bubble_y_pos

        # if protagonist collide with bubbles
        if protag_rect.colliderect(bubble_rect):
            game_result = "GAME OVER"
            running = False
            break

        # Looking at each existing weapon
        for weapon_index, weapon_val in enumerate(weapons):

            # get weapon initial values
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            # update weapon rect information
            weapon_rect      = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top  = weapon_y_pos

            # if weapons collide with bubbles
            if weapon_rect.colliderect(bubble_rect):

                # set which weapon/bubble to remove (by index)
                weapon_removal  = weapon_index
                bubble_removal = bubble_index

                # if not the smallest bubble
                if bubble_img_idx < 3:

                    # get current bubble information
                    bubble_width  = bubble_rect.size[0]
                    bubble_height = bubble_rect.size[1]

                    # split bubble information
                    s_bble_rect = bubble_img[bubble_img_idx + 1].get_rect()
                    s_bble_width = s_bble_rect.size[0]
                    s_bble_height = s_bble_rect.size[1]

                    # bubble split to the left
                    bubbles.append({
                        "pos_x": (bubble_x_pos + (bubble_width / 2)
                                                - (s_bble_width / 2)),
                        "pos_y": (bubble_y_pos + (bubble_height / 2)
                                                - (s_bble_height / 2)),
                        "img_index": bubble_img_idx + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_spd_y": bubble_speed_y[bubble_img_idx + 1]
                    })

                    # bubble split to the right
                    bubbles.append({
                        "pos_x": (bubble_x_pos + (bubble_width / 2)
                                                - (s_bble_width / 2)),
                        "pos_y": (bubble_y_pos + (bubble_height / 2)
                                                - (s_bble_height / 2)),
                        "img_index": bubble_img_idx + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_spd_y": bubble_speed_y[bubble_img_idx + 1]
                    })
                break
        else:
            continue
        
        break

    # Remove any bubbles or weapons if collided
    if bubble_removal > -1:
        del bubbles[bubble_removal]
        bubble_removal = -1

    if weapon_removal > -1:
        del weapons[weapon_removal]
        weapon_removal = -1

    # If all bubbles are eliminated
    if len(bubbles) == 0:
        game_result = "MISSION COMPLETE"
        running = False


    """----------------------
    BLITTING
    ----------------------"""

    # copy background to screen (0,0
    screen.blit(background, (0, 0))

    # Copy weapon to screen
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    # Copy bubbles to screen
    for idx, val in enumerate(bubbles):
        bubble_x_pos = val["pos_x"]
        bubble_y_pos = val["pos_y"]
        bubble_img_idx =val["img_index"]

        screen.blit(bubble_img[bubble_img_idx], 
                    (bubble_x_pos, bubble_y_pos))

    # Copy protagonist to screen
    screen.blit(protagonist, (protag_x_pos, protag_y_pos))

    # Copy stage to screen
    screen.blit(stage, (0, screen_height - stage_height))

    # Show the number of weapons left
    count = game_font_2.render(
        "Weapons : %d" % weapon_cnt, True, (80, 80, 80))

    screen.blit(count, (30, 70))

    """----------------------
    TIMER
    ----------------------"""

    # Calculate elapsed time
    # "/1000" because ticks are in milliseconds: convert to seconds
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    # Show the number of seconds left
    # Render on screen: render(text, True, color)
    timer = game_font_1.render(
        "Time : %d" % (int(game_time - elapsed_time)), True, (0, 0, 0))

    screen.blit(timer, (30, 30))

    if (game_time - elapsed_time) <= 0:
        game_result = "GAME OVER"
        running = False

    # Need to keep updating
    pygame.display.update()


"""----------------------------------------------------------------------------
7. QUITTING GAME
----------------------------------------------------------------------------"""

# Display game over message at the center of screen
msg = game_font_1.render(game_result, True, (0, 0, 0))
msg_rect   = msg.get_rect()
msg_width  = msg_rect.size[0]
msg_height = msg_rect.size[1]

screen.blit(msg, ( int((screen_width / 2) - (msg_width / 2)), 
                   int((screen_height / 2) - (msg_height / 2)) ))

if game_result == "MISSION COMPLETE":
    record_time = "Record: %d seconds" % elapsed_time
    record = game_font_2.render(record_time, True, (80, 80, 80))
    record_rect   = record.get_rect()
    record_width  = record_rect.size[0]
    record_height = record_rect.size[1]

    screen.blit(record, ( int((screen_width / 2) - (record_width / 2)), 
                        int((screen_height / 2) - (record_height / 2)) + 40 ))

pygame.display.update()

# Game over delay (for two seconds)
pygame.time.delay(2000)

# Ending pygame
pygame.quit()



"""
REFERENCES

Original background image and ground:
https://www.freepik.com/search?dates=any&format=search&page=1&query=valley-cross-section-soil-wiyh-fossils
Created by upklyak, uploaded at www.freepik.com

Weapon (spear) image:
https://www.hiclipart.com/free-transparent-background-png-clipart-zoldp

Protagonist image:
https://www.hiclipart.com/free-transparent-background-png-clipart-dpsig

Bubble imge:
https://www.hiclipart.com/free-transparent-background-png-clipart-isieg

"""