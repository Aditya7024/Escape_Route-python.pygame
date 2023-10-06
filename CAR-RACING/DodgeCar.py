# Importing all important files and library
import pygame,sys,time,os,random
from pygame.locals import *

# Defining the main class
class DodgeCars:
    def __init__(self, Display):
        self.Display = Display
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.black = (0,0,0)
        self.width = 800
        self.height = 600
        self.GameO_img = pygame.image.load("images/gameover.jpg")
        self.Pscore = []

    # Function for displaying any image on the screen 
    def Blit_Image(self,image,x,y):
        self.Display.blit(image,(x,y))
    
    # Function for opponent cars only appearing on the screen
    def opponent_car(self):
        self.opp_car = [pygame.image.load("images/caropp1.png"),pygame.image.load("images/caropp2.png"),pygame.image.load("images/caropp3.png")]
        self.opp_car_HW = [(65,104),(64,106),(63,104)]
        self.random_number = random.randrange(0,3)
        self.current_car  = self.opp_car[self.random_number]
        self.current_W,self.current_H = self.opp_car_HW[self.random_number]
        return self.current_car,self.current_W,self.current_H

    # Function for opponent car having different coordinates when appearing
    def opponent_car_coordinates(self,road_r):
        self.ocar_sx = random.randrange(200,road_r - 64)
        self.ocar_slist = [-10,-20,-15,-12,-23]
        self.ocar_sy = self.ocar_slist[random.randrange(0,4)]
        return self.ocar_sx,self.ocar_sy
    
    # To display score on the screen 
    def score(self,count):
        self.score_obj = pygame.font.Font("freesansbold.ttf",30)
        self.score_surf = self.score_obj.render("Score : "+ str(count),True,self.black)
        self.Display.blit(self.score_surf,(0,0))

    # Game Over image on the screen
    def Gameover(self,width,height):
        self.Display.blit(self.GameO_img,(40,50))
        pygame.display.update()
        time.sleep(3)

    # Function to update text(high_score.txt) file with current score
    def Enter_current_score(self,c_score):
        write = open("high_score.txt","a")
        write.write("\n")
        write.write(str(c_score))
        write.close()

    # Function to read the text file and give previous high score
    def prev_score(self):
        read = open("high_score.txt","r")
        self.score = read.readlines()
        read.close()
        self.score = [x.rstrip() for x in self.score]
        self.score = [int(x) for  x in self.score]
        self.score.sort()
        DodgeCars.Show_prev_score(self,self.score[len(self.score)-1])

    # Function to show the previous high score
    def Show_prev_score(self,pscore):
        self.Dscore_obj = pygame.font.Font("freesansbold.ttf",20)
        self.Dscore_sur = self.Dscore_obj.render("Last high score "+ str(pscore),True,self.black)
        self.Display.blit(self.Dscore_sur,(0,575))

    # Function to display number of lifes 
    def Display_life(self,life):
        self.score_obj  = pygame.font.Font("freesansbold.ttf",30)
        self.score_surf = self.score_obj.render("Trun left : "+str(life),True,self.black)
        self.Display.blit(self.score_surf,(620,0))

    # Function to generate light when hovered over the buttons
    def lights(self,center_x,center_y,radius,color):
        pygame.draw.circle(self.Display,color,(center_x,center_y),radius)