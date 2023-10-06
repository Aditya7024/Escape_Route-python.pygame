# Importing all important files and library
import pygame ,sys,time,random
from pygame.locals import *
from DodgeCar import *


# Initializing pygame
pygame.init()


# Diclaring variables for color ,height and width
width, height, FPS = 800, 600, 40
white = (255,255,255)
l_red = (255,0,0)
red = (150,0,0)
l_green = (0,255,0)
green = (0,250,0)
yellow = (255,229,10)
l_yellow = (212,255,10)
black = (0,0,0)
road_color = (47,47,47)


# Display the game screen and import imortant images
Display = pygame.display.set_mode([width,height])
pygame.display.set_caption("Escape Route")
clock = pygame.time.Clock()

car_img = pygame.image.load("images/racecar.png")
road_img = pygame.image.load("images/road1.jpg")
forest_img = pygame.image.load("images/longtree1.jpg")
river_img = pygame.image.load("images/longtree2.jpg")

inst = pygame.image.load("images/instruction.png")
instback_img = pygame.image.load("images/building.png")
my_car = pygame.image.load("images/olaa.jpg")
game_icon = pygame.image.load("images/icons.png")
pygame.display.set_icon(game_icon)


# Number of lifes a player have
life = 2
Previous_score = DodgeCars(Display)
Previous_score.prev_score()

End_game = False
Game_paused = False
Just_In = DodgeCars(Display)


# First screen appearence with buttons
def Entry_Screen():
    entry = True
    Display.fill(white)
    while entry:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        color_tuple = (red,yellow,green)
        color = color_tuple[random.randint(0,2)]

        display_message("Escape Route",70,400,100,color)
        display_message("Made By : Aditya Singh",20,650,20,black)

        Just_In.Blit_Image(my_car,40,135)

        Interactive(250,525,20,green,l_green,"Start!!")
        Interactive(400, 525, 20, yellow, l_yellow, "Instructions!!")
        Interactive(550, 525, 20, red, l_red, "Quit!!")

        pygame.display.update()
        clock.tick(FPS)


# Initializing the mouse position capturing variables
mo_x, mo_y = 0,0
click_x, click_y = 0,0
MouseClicked = False


# Assing the functionality for buttons and it options with color and message
def Interactive(center_x,center_y,radius,icolor,acolor,message):
    global mo_x,mo_y
    global click_x,click_y
    global MouseClicked

    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            mo_x, mo_y = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
            MouseClicked = True

        elif event.type == MOUSEBUTTONUP:
            click_x, click_y =event.pos
            MouseClicked = True

    left_x = center_x - radius
    left_y = center_y - radius
    width_c = height_c = 2*radius

    if mo_x > left_x and mo_x < (left_x + width_c) and mo_y > left_y and mo_y < (left_y + height_c):
        Just_In.lights(center_x,center_y,radius,acolor)
        display_message(message,20,center_x,center_y + 50,black)
        
        # When Start button is pressed
        if click_x > 230 and click_x < (230+40) and click_y > 505 and click_y<(505+40) and MouseClicked == True:
            MouseClicked = False
            global  life
            global Game_paused

            if life == -1:
                life = 2
                Enter_game()
                main()

            elif Game_paused == True:
                Game_paused = False
                pygame.mixer.music.unpause()

            else:
                Enter_game()
                main()


        # When the Instruction button is pressed
        elif click_x > 400 and click_x < (400 + 40) and click_y > 505 and click_y < (505 + 40) and MouseClicked == True:
            Instruction_page()


        # When Quit button is pressed
        elif click_x > 530 and click_x  <(530+40) and click_y > 505  and click_y<(505+40) and MouseClicked == True:
            pygame.quit()
            sys.exit()

    else:
        Just_In.lights(center_x,center_y,radius,icolor)
        display_message(message,20,center_x,center_y+50,black)


# Instruction page function and instruction with back button
def Instruction_page():
    Display.fill(white)
    instruct = True
    while instruct:

        Just_In.Blit_Image(instback_img, 0, 0)
        Just_In.Blit_Image(inst, 40, 135)
        display_message("Instructions", 70, 400, 50, black)
        Interactive(400, 525, 20, green, l_green, "Back!!")

        click = pygame.mouse.get_pressed()
        if click == (1,0,0):
            Entry_Screen()
        pygame.display.update()
        clock.tick(30)


# When the car crashes play a sound and display explosion image
def crash(opcar_startx,opcar_starty,count):
    enter_current_score = DodgeCars(Display)
    sound_obj = pygame.mixer.Sound("music/crash.wav")
    sound_obj.play()
    explosion(opcar_startx,opcar_starty)
    enter_current_score.Enter_current_score(count)
    life_count()
    time.sleep(2)
    main()


# Display the explosion image
def explosion(ocar_startx,ocar_starty):
    expimg = pygame.image.load("images/booom.png")
    Display.blit(expimg,(ocar_startx,ocar_starty))
    pygame.display.update()


# Display the messages with the help of build in font formate
def display_message(text,size,x,y,color):
    Text_obj = pygame.font.Font("freesansbold.ttf",size)
    Text_surf = Text_obj.render(text,True,color)
    Rect_surf = Text_surf.get_rect()
    Rect_surf.center = (x,y)
    Display.blit(Text_surf,Rect_surf)
    pygame.display.update()


# Take a track of number of lifes left
def life_count():
    global life
    life -= 1
    if life == -1:
        gameover = DodgeCars(Display)
        gameover.Gameover(width,height)
        while True:
            Restart_page()


# Restart the page after pressing "Restart"
def Restart_page():
    Interactive(250,525,20,green,l_green,"Restart!!")
    Interactive(550,525,20,red,l_red,"Quit!!")
    pygame.display.update()
    clock.tick(15)


# Function to pause the game when "p" is pressed
def Pause():
    global Game_paused
    pygame.mixer.music.pause()
    Game_paused = True
    while Game_paused:
        display_message("Paused",100,width/2,height/2,black)
        Interactive(250,525,20,green,l_green,"Continue!!")
        Interactive(550,525,20,red,l_red,"Quit!!")
        pygame.display.update()
        clock.tick(30)


# The screen which will display the game after the countdown with road,cars,trees etc
def Enter_game():
    Display.fill(road_color)
    roadx = 200
    roady = -5
    treex1 = 0
    treey1 = 0
    treex2 = 605
    treey2 = 0
    start_number = DodgeCars(Display)
    at_start_time = 3
    while at_start_time >=0:
        start_number.Blit_Image(road_img,roadx,roady)
        start_number.Blit_Image(forest_img,treex1,treey1)
        start_number.Blit_Image(river_img, treex2, treey2)
        if at_start_time == 0 :
            display_message("GO!!",150,width/2,height/2,black)
        else:
            display_message(str(at_start_time),150,width/2,height/2,black)
        at_start_time -= 1
        pygame.display.update()
        clock.tick(1)


# Main head function
def main():
    obj1 = DodgeCars(Display)
    obj2 = DodgeCars(Display)
    objects = (obj1,obj2)
    Life = DodgeCars(Display)
    carx = width * 0.4
    cary = height * 0.8
    car_width = 64
    car_height = 104
    previous_score = DodgeCars(Display)
    

    x_change=y_change = 0

    road_r  = 600
    current_car1,ocar_w1,ocar_h1 = objects[0].opponent_car()
    ocar_startx1,ocar_starty1 = objects[0].opponent_car_coordinates(road_r)
    ocar_speed1 = 7
    ocar_speed2 = 7
    ocar_speed3 = 9

    ocarspeed = [ocar_speed1,ocar_speed2,ocar_speed3]
    add_speed1 = ocarspeed[0]
    add_speed2 = ocarspeed[1]
    add_speed3 = ocarspeed[2]

    ocarspeed_up = 15
    second_car_first_time = 1

    roadx = 200
    roady = -580
    treex1 = 0
    treey1 = -580
    treex2 = 605
    treey2 = -580
    moveroad = 5
    movetree1 = 5
    movetree2 = 5
    temptreespeed1 = 5
    temptreespeed2 = 5
    temproadspeed = 5
    count = 0
    up_press_count = 1

    global Game_paused
    if Game_paused == False:
        while not End_game:
            Display.fill(road_color)
            roady += moveroad
            treey1 += movetree1
            treey2 += movetree2
            if roady > 10:
                roady = -580
            if treey1 > 10:
                treey1 = -580
                treey2 = -580
            objects[0].Blit_Image(road_img,roadx,roady)
            objects[0].Blit_Image(forest_img, treex1, treey1)
            objects[0].Blit_Image(river_img, treex2, treey2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_p:
                        Pause()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -6
                    elif event.key == pygame.K_RIGHT:
                        x_change = 6
                    elif event.key == pygame.K_UP:
                        if  up_press_count == 1:
                            cary += -15
                        up_press_count += 1
                        moveroad = 10
                        movetree1 = 10
                        movetree2 = 10
                        add_speed1 = 14
                        if count >= 10:
                            add_speed2 = 17

                    elif event.key == pygame.K_DOWN:
                        y_change = 5

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                        x_change = 0
                        y_change = 0
                    elif event.key == pygame.K_UP:
                        if up_press_count > 1:
                            cary += 15
                            up_press_count= 1
                        add_speed1 = ocarspeed[0]
                        moveroad = temproadspeed
                        moveroad1 = temptreespeed1
                        moveroad2 = temptreespeed2
                        if count >= 10:
                            add_speed2 = ocarspeed[1]

            carx += x_change
            ocar_starty1 += add_speed1
            objects[0].Blit_Image(car_img,carx,cary)
            objects[0].Blit_Image(current_car1,ocar_startx1,ocar_starty1)
            if count >= 10:
                ocar_starty2 += add_speed2
                objects[0].Blit_Image(current_car2,ocar_startx2,ocar_starty2)

            objects[0].score(count)
            previous_score.prev_score()
            Life.Display_life(life)

            if carx < 200 or carx > (width-car_width-200) or (cary + car_height) > height or cary < 0:
                crash(carx,cary,count)

            if ocar_starty1 > height:
                if count > 10:
                    current_car1,ocar_w1,ocar_h1 = objects[0].opponent_car()
                    ocar_startx1,ocar_starty1 = objects[0].opponent_car_coordinates(road_r)
                    while (ocar_startx1 > ocar_startx2 and ocar_startx1< ocar_startx2 + ocar_w2):
                        current_car1,ocar_w1,ocar_h1 = objects[0].opponent_car()
                        ocar_startx1, ocar_starty1 = objects[0].opponent_car_coordinates(road_r)
                else:
                    current_car1,ocar_w1,ocar_h1 = objects[0].opponent_car()
                    ocar_startx1, ocar_starty1 = objects[0].opponent_car_coordinates(road_r)
                count += 1

                ocarspeed[0] += 0.005
                temproadspeed += 0.004
                moveroad += 0.004
                movetree1 += 0.004
                movetree2 += 0.004
                temptreespeed1 += 0.004
                temptreespeed2 += 0.004
                if count == 10:
                    current_car2, ocar_w2, ocar_h2 = objects[0].opponent_car()
                    ocar_startx2, ocar_starty2 = objects[0].opponent_car_coordinates(road_r)

            if count > 10:
                if ocar_starty2 > height:
                     current_car2, ocar_w2, ocar_h2 = objects[0].opponent_car()
                     ocar_startx2, ocar_starty2 = objects[0].opponent_car_coordinates(road_r)
                     while (ocar_startx2 > ocar_startx1 and ocar_startx2< ocar_startx1 + ocar_w1):
                         ocar_startx2, ocar_starty2 = objects[0].opponent_car_coordinates(road_r)

                     if second_car_first_time == 1:
                         ocarspeed[1] += 0.015
                         second_car_first_time += 1
                     ocarspeed[1] += 0.006
                     count += 1

            if cary <  ocar_starty1+ ocar_h1 and (cary + car_height) > ocar_starty1:
                if (carx > ocar_startx1 and carx < ocar_startx1 + ocar_w1) or (carx + car_width > ocar_startx1 and carx + car_width < ocar_startx1 + ocar_w1):
                    crash(carx,cary-20,count)
            if count > 10 and count <= 20:
                if cary < ocar_starty2 + ocar_h2 and (cary + car_height) > ocar_starty2:
                    if (carx > ocar_startx2 and carx < ocar_startx2 + ocar_w2) or (carx + car_width > ocar_startx2 and carx + car_width < ocar_startx2 + ocar_w2):
                        crash(carx, cary - 20, count)

            pygame.display.update()
            clock.tick(FPS)
Entry_Screen()
pygame.quit()
sys.exit()