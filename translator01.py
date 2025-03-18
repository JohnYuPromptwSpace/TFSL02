import pygame, sys, os
import pyautogui
import googletrans

from pygame.locals import * # import pygame modules

pygame.init() # initiate pygame
clock=pygame.time.Clock()

pygame.display.set_caption('Game') # set the window name

W,H = pyautogui.size()
WINDOW_SIZE = (W-400,H-200) # set up window size

clicked = False

screen = pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE) # initiate screen

display = pygame.Surface((W,H))

black = (0,0,0)
white = (255,255,255)
gray = (180,180,180)

dialogOn = False

transMode = 0

# 0 trans

Scene = 0

########## Open Img ##########

def get_src(src):
    for x in range(len(src)):
        if x == "\\":
            src[x] = "/"
    return src

swap_img = pygame.image.load(get_src(os.getcwd()+"/img/swap.png"))
swap_img = pygame.transform.scale(swap_img, (50, 50))
close_img = pygame.image.load(get_src(os.getcwd()+"/img/close.png"))
close_img = pygame.transform.scale(close_img, (50, 50))

font = pygame.font.Font(None, 36)

def dialogNotAva():
    global dialogOn
    swapDialog = Dialog("Not available yet", close_img)
    dialogList.append(swapDialog)
    dialogOn = True

def buttonFunc(funcNum):
    global dialogOn
    if funcNum == 0:
        dialogNotAva()

class Button():   
    def __init__(self, x = 0, y = 0, imgName = "", size = [], buttonCol = [], hoverCol = [], clickCol = [], funcNum = 0):
        self.x = x
        self.y = y
        self.imgName = imgName
        self.size = size
        self.buttonColor = buttonCol
        self.hoverColor = hoverCol
        self.clickColor = clickCol
        self.funcNum = funcNum
    
    def draw_button(self):
        global clicked
        action = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #create pygame Rect object for the buttonb
        button_rect = Rect(self.x, self.y, self.size[0], self.size[1])
        
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos) and not dialogOn:
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(display, self.clickColor, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                buttonFunc(self.funcNum)
                clicked = False
                action = True
            else:
                pygame.draw.rect(display, self.hoverColor, button_rect)
        else:
            pygame.draw.rect(display, self.buttonColor, button_rect)
        
        # #add shading to button
        
        #add img to button
        display.blit(self.imgName, (self.x, self.y))
        return action

class ButtonText():   
    def __init__(self, x = 0, y = 0, text = "", size = [], buttonCol = [], hoverCol = [], clickCol = [], funcNum = 0):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.buttonColor = buttonCol
        self.hoverColor = hoverCol
        self.clickColor = clickCol
        self.funcNum = funcNum
    
    def draw_button(self):
        global clicked
        action = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #create pygame Rect object for the buttonb
        button_rect = Rect(self.x, self.y, self.size[0], self.size[1])
        
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos) and not dialogOn:
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(display, self.clickColor, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                buttonFunc(self.funcNum)
                clicked = False
                action = True
            else:
                pygame.draw.rect(display, self.hoverColor, button_rect)
        else:
            pygame.draw.rect(display, self.buttonColor, button_rect)
        
        # #add shading to button
        
        #add img to button
        text = font.render(self.text, True, black)
        display.blit(text, (self.x, self.y))
        return action

class Dialog:
    def __init__(self, text, imgName):
        self.text = text
        self.imgName = imgName
    
    def drawDialog(self):
        pygame.draw.rect(display, (200,200,200), (W/3, H/8*3,W/3,H/4), border_radius=15)
        text = font.render(self.text, True, black)
        display.blit(text, (W/2 - text.get_width()/2, H/2 - text.get_height()/2+50))
        display.blit(self.imgName, (W/2-25, H/2-50))

buttonList = []

swap_button = Button(W/2-25, 70, swap_img, [50,50], [255,255,255], [230,230,230], [230,230,230], 0)
buttonList.append(swap_button)

sign_languageB = ButtonText(W/2-700-50-1+15, 69+15, "Korean Sign Language", [670,20], [255,255,255], [220,220,220], [230,230,230], 0)
buttonList.append(sign_languageB)
dialogList = []

while True: # game loop
    if Scene == 0:
        display.fill(white)
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                pygame.quit() # stop pygame
                sys.exit() # stop script
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOW_SIZE = (W, H)
                screen = pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOW_SIZE)
            # if event.type == KEYDOWN:
                # if event.key == K_SPACE:  # Show/hide dialog with space key
    
        
        langWidth,landHeight = 700, 50
        margin = 50
        pygame.draw.rect(display, gray, [W/2-langWidth-margin-1, 69, langWidth+2, landHeight+2], width=0, border_radius=15)
        pygame.draw.rect(display, white, [W/2-langWidth-margin, 70, langWidth, landHeight], width=0, border_radius=15)
        
        for button in buttonList:
            button.draw_button()
        
        pygame.draw.rect(display, gray, [W/2+margin-1, 69, langWidth+2, landHeight+2], width=0, border_radius=15)
        pygame.draw.rect(display, white, [W/2+margin, 70, langWidth, landHeight], width=0, border_radius=15)
        
        # if transMode == 0:
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                dialogOn = False
        
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()