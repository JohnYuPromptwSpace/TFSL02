import sys, os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# null = open(os.devnull, 'w')
# sys.stdout = null
# sys.stderr = null
import warnings
# warnings.filterwarnings('ignore') 
import pyautogui
import pygame
from pygame.locals import *
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque
from PIL import Image, ImageDraw
import time as t
import googletrans
import openai
import math
from gtts import gTTS
import tkinter as tk
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

########### SET UP ###########
translator = googletrans.Translator()

pygame.init()
clock=pygame.time.Clock()

pygame.display.set_caption('TFSL')

W,H = pyautogui.size()
W,H = W-400,H-200

WINDOWSIZE = (W,H)

screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE)

display = pygame.Surface(WINDOWSIZE)

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180,180,180)
LIGHTGRAY = (220,220,220)
LIGHTERGRAY = (235,235,235)

LANGFONT = pygame.font.Font(None, 36)
DIALOGFONT = pygame.font.Font(None, 36)
COPYRIGHTFONT = pygame.font.Font(None, 24)
MENUFONT = pygame.font.SysFont(None, 36)
KOREANFONT = pygame.font.SysFont("malgungothic", 36)
KEYBOARDFONT = pygame.font.SysFont(None, 48)

DIALOGON = False

COPYRIGHTMESSAGE = "2023 © PWS, TFSL All Rights Reserved"

TRANSDELAY = 0.1

CTIME = 0

BUTTON_WIDTH = 60
BUTTON_HEIGHT = 60

########### Pre Define Variables ###########
buttonList0 = []
buttonList1 = []
buttonList2 = []
buttonList3 = []
buttonList4 = []
buttonList5 = []
buttonList6 = []
buttonList7 = []
buttonList8 = []
dialogList=[]

transMode = 0
transPos = [7, 20/11]

Slanguages = ["korean SL"]

KoreanSMean = {"people":"여러분", "good":"좋은", "sorry":"미안", "hello":"안녕", "higher":"잘하다", "nicetosee":"반갑다","meet":"만나다"}

languages = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
languagesKeys = ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']
langfonts = {'korean':KOREANFONT, 'english':LANGFONT}


languagesPageMin = 2
languagesPageMax = 8

k = 0

########### DEFINE FUNCTIONS ###########

def get_src(src):
    for x in range(len(src)):
        if x == "\\":
            src[x] = "/"
    return src

### OPEN IMGs ###

swapImg = pygame.image.load(get_src(os.getcwd()+"/img/swap.png"))
swapImg = pygame.transform.scale(swapImg, (50, 50))

closeImg = pygame.image.load(get_src(os.getcwd()+"/img/close.png"))
closeImg = pygame.transform.scale(closeImg, (50, 50))

novideoImg = pygame.image.load(get_src(os.getcwd()+"/img/no-video.png"))
novideoImg = pygame.transform.scale(novideoImg, (50, 50))

# Functional Img #

playImg = pygame.image.load(get_src(os.getcwd()+"/img/play-button.png"))
playImg = pygame.transform.scale(playImg, (100, 100))

stopImg = pygame.image.load(get_src(os.getcwd()+"/img/pause-button.png"))
stopImg = pygame.transform.scale(stopImg, (100, 100))

button1 = [playImg, stopImg]
buttonIndex = 0

backImg = pygame.image.load(get_src(os.getcwd()+"/img/left-arrow.png"))
backImg = pygame.transform.scale(backImg, (100, 100))

ttsImg = pygame.image.load(get_src(os.getcwd()+"/img/speaker-filled-audio-tool.png"))
ttsImg = pygame.transform.scale(ttsImg, (100, 100))

settingImg = pygame.image.load(get_src(os.getcwd()+"/img/setting.png"))
settingImg = pygame.transform.scale(settingImg, (100, 100))

# Scenes Img #

homeImg = pygame.image.load(get_src(os.getcwd()+"/img/back.png"))
homeImg = pygame.transform.scale(homeImg, (50, 50))

logoImg = pygame.image.load(get_src(os.getcwd()+"/img/logo.png"))
logoImg = pygame.transform.scale(logoImg, (50, 50))

nextImg = pygame.image.load(get_src(os.getcwd()+"/img/right.png"))
nextImg = pygame.transform.scale(nextImg, (50, 50))
upImg = pygame.transform.rotate(nextImg, 90)
downImg = pygame.transform.rotate(nextImg, 270)
beforeImg = pygame.transform.rotate(nextImg, 180)

class VirtualKeyboard(tk.Tk):
    def __init__(self, cameraNum):
        super().__init__()
        self.cameraNum = cameraNum
        self.title('Settings')
        self.geometry('250x350')

        # Entry widget to show the typed characters
        self.label = tk.Label(text=f"Set Camera(0 ~ {cameraNum-1})")
        self.entry = tk.Entry(self) 
        self.label.pack(pady=10)
        self.entry.pack(pady=10)

        # Keyboard layout
        keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ["↩",'0', '←']
        ]

        # Create buttons for each character and assign a command
        for row in keys:
            button_frame = tk.Frame(self)
            button_frame.pack(pady=5)

            for key in row:
                if key == '←':
                    button = tk.Button(button_frame, text=key, width=4, command=self.backspace)
                elif key == "↩":
                    button = tk.Button(button_frame, text=key, width=4, command=self.enter)
                else:
                    button = tk.Button(button_frame, text=key, width=4, command=lambda key=key: self.add_char(key))
                button.pack(side=tk.LEFT, padx=5, pady=5)
        self.currLabel = tk.Label(text=f"Current Camera:{0}")
        self.currLabel.pack(pady=10)

    def add_char(self, char):
        current_text = self.entry.get()
        updated_text = current_text + char
        self.entry.delete(0, tk.END)
        self.entry.insert(0, updated_text)

    def backspace(self):
        current_text = self.entry.get()
        updated_text = current_text[:-1]  # Remove the last character
        self.entry.delete(0, tk.END)
        self.entry.insert(0, updated_text)
    
    def enter(self):
        global cameraNum
        current_text = self.entry.get()
        self.entry.delete(0,tk.END)
        if int(current_text) <= int(self.cameraNum)-1 and int(current_text) >= 0:
            cameraNum = int(current_text)
            self.currLabel["text"] = f"Current Camera:{int(current_text)}"
    
class SetDelay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Settings')
        self.geometry('250x350')

        # Entry widget to show the typed characters
        self.label = tk.Label(text=f"Set Delay(Default 3s)")
        self.entry = tk.Entry(self)
        self.label.pack(pady=10)
        self.entry.pack(pady=10)

        # Keyboard layout
        keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ["↩",'0', '←']
        ]

        # Create buttons for each character and assign a command
        for row in keys:
            button_frame = tk.Frame(self)
            button_frame.pack(pady=5)

            for key in row:
                if key == '←':
                    button = tk.Button(button_frame, text=key, width=4, command=self.backspace)
                elif key == "↩":
                    button = tk.Button(button_frame, text=key, width=4, command=self.enter)
                else:
                    button = tk.Button(button_frame, text=key, width=4, command=lambda key=key: self.add_char(key))
                button.pack(side=tk.LEFT, padx=5, pady=5)
        self.currLabel = tk.Label(text=f"Current Delay:{3}s")
        self.currLabel.pack(pady=10)

    def add_char(self, char):
        current_text = self.entry.get()
        updated_text = current_text + char
        self.entry.delete(0, tk.END)
        self.entry.insert(0, updated_text)

    def backspace(self):
        current_text = self.entry.get()
        updated_text = current_text[:-1]  # Remove the last character
        self.entry.delete(0, tk.END)
        self.entry.insert(0, updated_text)

    def enter(self):
        global TRANSDELAY
        current_text = self.entry.get()
        TRANSDELAY = int(current_text)
        self.entry.delete(0,tk.END)
        self.currLabel["text"]=f"Current Delay:{int(current_text)}s"
            

def count_cameras():
    count = 0
    while True:
        cap = cv2.VideoCapture(count)
        if not cap.read()[0]:
            break
        else:
            count += 1
        cap.release()
    return count

def openTkinter():
    global cameraNum, cap
    keyboard = VirtualKeyboard(cameraNum=count_cameras())
    keyboard.mainloop()
    cap = checkCameraIdx(cameraNum)
    keyboard = SetDelay()
    keyboard.mainloop()

def backSpace():
    global starting_index, visible_items_count
    if len(menuItems)==0:
        return
    menuItems.pop(-1)
    
    if starting_index > 0:
        starting_index-=1

def SPTrans():
    global buttonIndex, CTIME
    if buttonIndex == 0:
        buttonIndex = 1
        transButton.imgName = button1[buttonIndex]
        CTIME = t.time()
    else:
        buttonIndex = 0
        transButton.imgName = button1[buttonIndex]

def dialogNotAva():
    global DIALOGON
    swapDialog = Dialog("Not available yet", closeImg)
    dialogList.append(swapDialog)
    DIALOGON = True

def scrollUp():
    global starting_index
    if starting_index > 0:
        starting_index-=1

def scrollDown():
    global starting_index
    starting_index += 1
    if starting_index > len(menuItems) - visible_items_count:
        starting_index -= 1
        
def speak():
    global pLang, k
    
    text = ""
    
    for line in menuItems:
        text = text + ","+line
    
    tts = gTTS(text=text, lang=languages[pLang])
    
    filename=f'voice{k}.mp3'
    
    tts.save(filename)
    
    pygame.mixer.music.load(f'voice{k}.mp3')
    
    try:
        os.remove(f'voice{k-1}.mp3')
    except FileNotFoundError:
        pass
    
    pygame.mixer.music.play()
    
    k+=1

def analyzeButtonF(funcNum):
    global Scene, cameraNum
    if funcNum == 0:
        dialogNotAva()
    elif funcNum == 1:
        Scene = 1
    elif funcNum == 2:
        Scene = 2
    elif funcNum == 3:
        Scene = 0
    elif funcNum == 6:
        if Scene < languagesPageMax:
            Scene += 1
    elif funcNum == 7:
        if Scene > languagesPageMin:
            Scene -= 1
    elif funcNum == 8:
        SPTrans()
    elif funcNum == 9:
        backSpace()
    elif funcNum == 10:
        scrollUp()
    elif funcNum == 11:
        scrollDown()
    elif funcNum == 12:
        speak()
    elif funcNum == 13:
        openTkinter()

def changeKL(lang):
    global sLang, Scene
    sLang = lang
    slButton.text = lang
    Scene = 0
    
def changeLang(lang):
    global pLang, Scene
    pLang = lang
    spButton.text = lang
    Scene = 0

def pil_image_to_pygame_surface(pil_image):
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

def cv2_to_pil(cv2_image):
    # Convert from BGR to RGB
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(rgb_image)
    
    return pil_image

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im



########### DEFINE CLASSES ###########

class ButtonImg():   
    def __init__(self, x = 0, y = 0, imgName = "", size = [], buttonCol = [], hoverCol = [], clickCol = [], funcNum = -1, adjPos=[0,0]):
        self.x = x
        self.y = y
        self.imgName = imgName
        self.size = size
        self.buttonColor = buttonCol
        self.hoverColor = hoverCol
        self.clickColor = clickCol
        self.funcNum = funcNum
        self.adjPos = adjPos
    
    def drawButton(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos()
        
        button_rect = Rect(W/self.x - self.size[0]/2+self.adjPos[0], H/self.y - self.size[1]/2+self.adjPos[1], self.size[0], self.size[1])
        
        if button_rect.collidepoint(pos) and DIALOGON == False:
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(display, self.clickColor, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
                analyzeButtonF(self.funcNum)
            else:
                pygame.draw.rect(display, self.hoverColor, button_rect)
        else:
            pygame.draw.rect(display, self.buttonColor, button_rect)
        
        display.blit(self.imgName, (W/self.x - self.size[0]/2+self.adjPos[0], H/self.y - self.size[1]/2+self.adjPos[1]))
        return action

class ButtonText():   
    def __init__(self, x = 0, y = 0, text = "", size = 0, buttonCol = [], hoverCol = [], clickCol = [], funcNum = 0, adjPos=[0,0]):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.buttonColor = buttonCol
        self.hoverColor = hoverCol
        self.clickColor = clickCol
        self.funcNum = funcNum
        self.adjPos = adjPos
    
    def drawButton(self):
        global clicked
        action = False
        
        pos = pygame.mouse.get_pos()
        
        button_rect = Rect(W/self.x+self.adjPos[0], H/self.y+self.adjPos[1], W/self.size, 20)
        
        if button_rect.collidepoint(pos) and DIALOGON == False:
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(display, self.clickColor, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
                if self.funcNum == 4:
                    changeKL(self.text)
                elif self.funcNum == 5:
                    changeLang(self.text)
                else:
                    analyzeButtonF(self.funcNum)
            else:
                pygame.draw.rect(display, self.hoverColor, button_rect)
        else:
            pygame.draw.rect(display, self.buttonColor, button_rect)
        
        text = LANGFONT.render(self.text, True, BLACK)
        display.blit(text, (W/self.x+self.adjPos[0], H/self.y+self.adjPos[1]))
        return action

class Dialog:
    def __init__(self, text, imgName):
        self.text = text
        self.imgName = imgName
    
    def drawDialog(self):
        pygame.draw.rect(display, LIGHTGRAY, (W/3, H/8*3,W/3,H/4), border_radius=15)
        text = DIALOGFONT.render(self.text, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H/2 - text.get_height()/2+50))
        display.blit(self.imgName, (W/2-25, H/2-50))

########### DEFINE VARIABLE ###########

Scene = 0

clicked = False

sLang = 'korean SL'
pLang = 'korean'

swapButton = ButtonImg(2, 9, swapImg, (50,50), WHITE, LIGHTGRAY, GRAY, 0)
buttonList0.append(swapButton)

slButton = ButtonText(transPos[transMode], 9, sLang, 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=1)
buttonList0.append(slButton)

spButton = ButtonText(transPos[transMode*(-1)+1], 9, pLang, 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=2)
buttonList0.append(spButton)

menuItems = []
visible_items_count = 8
starting_index = 0

# Functional Button #

transButton = ButtonImg(9/3, 4/3, button1[buttonIndex], (100,100), WHITE, LIGHTGRAY, GRAY, 8)
buttonList0.append(transButton)

backButton = ButtonImg(9/4, 4/3, backImg, (100,100), WHITE, LIGHTGRAY, GRAY, 9)
buttonList0.append(backButton)

ttsButton = ButtonImg(9/5, 4/3, ttsImg, (100,100), WHITE, LIGHTGRAY, GRAY, 12)
buttonList0.append(ttsButton)

settingButton = ButtonImg(9/6, 4/3, settingImg, (100,100), WHITE, LIGHTGRAY, GRAY, 13)
buttonList0.append(settingButton)

upButton = ButtonImg(40/35, 40/20, upImg, (50,50), WHITE, LIGHTGRAY, GRAY,10)
buttonList0.append(upButton)

downButton = ButtonImg(40/35, 40/22, downImg, (50,50), WHITE, LIGHTGRAY, GRAY,11)
buttonList0.append(downButton)

for x in range(1):
    languagesButton = ButtonText(7, 20/(x+1), Slanguages[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=4)
    buttonList1.append(languagesButton)

for x in range(17):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList2.append(languagesButton)

for x in range(17, 34):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList3.append(languagesButton)

for x in range(34, 51):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList4.append(languagesButton)

for x in range(51, 68):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList5.append(languagesButton)

for x in range(68, 85):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList6.append(languagesButton)

for x in range(85, 102):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList7.append(languagesButton)

for x in range(102, 104):
    languagesButton = ButtonText(7, 20/((x%17)+1), languagesKeys[x], 24/7, WHITE, LIGHTGRAY, GRAY, adjPos=[10,-10], funcNum=5)
    buttonList8.append(languagesButton)

# Scene 1 Button #

homeButton = ButtonImg(1, 20/1, homeImg, (50,50), WHITE, LIGHTGRAY, GRAY, adjPos=[-200,0], funcNum=3)
buttonList1.append(homeButton)
buttonList2.append(homeButton)
buttonList3.append(homeButton)
buttonList4.append(homeButton)
buttonList5.append(homeButton)
buttonList6.append(homeButton)
buttonList7.append(homeButton)
buttonList8.append(homeButton)

nextButton = ButtonImg(1, 2, nextImg, (50,50), WHITE, LIGHTGRAY, GRAY, adjPos=[-200, -25], funcNum=6)
buttonList2.append(nextButton)
buttonList3.append(nextButton)
buttonList4.append(nextButton)
buttonList5.append(nextButton)
buttonList6.append(nextButton)
buttonList7.append(nextButton)
buttonList8.append(nextButton)
beforeButton = ButtonImg(1, 2, beforeImg, (50,50), WHITE, LIGHTGRAY, GRAY, adjPos=[-200, 25], funcNum=7)
buttonList2.append(beforeButton)
buttonList3.append(beforeButton)
buttonList4.append(beforeButton)
buttonList5.append(beforeButton)
buttonList6.append(beforeButton)
buttonList7.append(beforeButton)
buttonList8.append(beforeButton)

########## Real Time ###########

actions = [['sorry', 'people','good'],
           ['hello', 'higher', 'meet', 'nicetosee']]

points = [[5,6,66],
          [5,6,296]]

seq_length = 30

modelMono = load_model('models/model_tfslMono02.h5')
modelDuo = load_model('models/model_tfslDuo02.h5')

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

seq_left = []
action_seq_left = []
left_this_act = None

seq_right = []
action_seq_right = []
right_this_act = None

final_action = ""

mp_drawing = mp.solutions.drawing_utils

action_seq_left = deque(action_seq_left)
action_seq_right = deque(action_seq_right)

def checkCameraIdx(index):
    global cameraNum
    try:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            cameraNum = -1
            raise ValueError(f"Camera at index {index} not available")
        return cap
    except (cv2.error, ValueError) as e:
        cameraNum = -1
        return None

cameraNum= 0

cap = checkCameraIdx(cameraNum)

def gradient(pt1,pt2):
    try:
        return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
    except ZeroDivisionError:
        return 0
 
#3점이 있을 때 점 사이의 각도를 구하는 코드
def getAngle(pt1, pt2, pt3):
    m1 = gradient(pt1,pt2)
    m2 = gradient(pt1,pt3)
    try:
        angR = math.atan((m2-m1)/(1+(m2*m1))) #atan = arctan(3번 과정)
        return math.degrees(angR)
    except ZeroDivisionError: # 오류 예외 처리(0으로 나눌 경우)
        return 0

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def predict_left(result, handCount):
    global seq_length
    res = result.left_hand_landmarks

    joint = np.zeros((21, 4))
    for j, lm in enumerate(res.landmark):
        joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3]
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3]
    v = v2 - v1
    
    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
    
    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))

    angle = np.degrees(angle)

    d = np.concatenate([joint.flatten(), angle])
    
    seq_left.append(d)

    if len(seq_left) < seq_length:
        return None

    input_data = np.expand_dims(np.array(seq_left[-seq_length:], dtype=np.float32), axis=0)

    if handCount == 1:
        y_pred = modelMono.predict(input_data,verbose=None).squeeze()
    else:
        y_pred = modelDuo.predict(input_data,verbose=None).squeeze()

    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < 0.9:
        return None
    
    action = actions[handCount-1][i_pred]
    action_seq_left.append(action)

    if len(action_seq_left) < 3:
        return None

    left_this_act = None
    if action_seq_left[-1] == action_seq_left[-2] == action_seq_left[-3]:
        left_this_act = action
        action_seq_left.popleft()
    return left_this_act

def predict_right(result, handCount):
    res = result.right_hand_landmarks

    joint = np.zeros((21, 4))
    for j, lm in enumerate(res.landmark):
        joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3]
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3]
    v = v2 - v1

    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))

    angle = np.degrees(angle)

    d = np.concatenate([joint.flatten(), angle])

    seq_right.append(d)

    if len(seq_right) < seq_length:
        return None

    input_data = np.expand_dims(np.array(seq_right[-seq_length:], dtype=np.float32), axis=0)

    if handCount == 1:
        y_pred = modelMono.predict(input_data,verbose=None).squeeze()
    else:
        y_pred = modelDuo.predict(input_data,verbose=None).squeeze()

    i_pred = int(np.argmax(y_pred))
    conf = y_pred[i_pred]

    if conf < 0.9:
        return None
            
    action = actions[handCount-1][i_pred]
    action_seq_right.append(action)

    if len(action_seq_right) < 3:
        return None

    right_this_act = None
    if action_seq_right[-1] == action_seq_right[-2] == action_seq_right[-3]:
        right_this_act = action
        action_seq_right.popleft()
    return right_this_act

def cv2_image_to_pygame_surface(cv2_image):
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    return pygame.surfarray.make_surface(rgb_image)

########### Main Loop ###########

while True:
    if Scene == 0:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    starting_index -= 1
                    if starting_index < 0:
                        starting_index = 0
                elif event.button == 5:  # Scroll down
                    starting_index += 1
                    # Prevent scrolling past the last item
                    
                    if starting_index > len(menuItems) - visible_items_count:
                        starting_index -=1
            
        pygame.draw.rect(display, GRAY, [W/7-1, H/9-25-1, W/13*4+2, 50+2], width=0, border_radius=15)
        pygame.draw.rect(display, WHITE, [W/7, H/9-25, W/13*4, 50], width=0, border_radius=15)
        
        pygame.draw.rect(display, GRAY, [W/20*11-1, H/9-25-1, W/13*4+2, 50+2], width=0, border_radius=15)
        pygame.draw.rect(display, WHITE, [W/20*11, H/9-25, W/13*4, 50], width=0, border_radius=15)
        
        pygame.draw.rect(display, LIGHTERGRAY, [W/20*11-1, H/6, W/13*4+2, (W/13*4+2)*3/4], width=0, border_radius=15)
        
        # if 1==0:
        #     pass
        
        if cap != None:
            ret, img = cap.read()

            img = cv2.flip(img, 1)
            
            if buttonIndex == 1:
                img, result = mediapipe_detection(img, holistic)
                final_action = None
                
                leftPrediction = None
                rightPrediction = None
                
                try:
                    if result.left_hand_landmarks or result.right_hand_landmarks:
                        if result.left_hand_landmarks and result.right_hand_landmarks:
                            leftPrediction = predict_left(result,2)
                            rightPrediction = predict_right(result,2)
                            print(leftPrediction,rightPrediction)
                            if leftPrediction == rightPrediction:
                                final_action = leftPrediction
                        else:
                            if result.left_hand_landmarks:
                                final_action = predict_left(result,1)
                            else:
                                final_action = predict_right(result,1)
                except IndexError:
                    pass
                
                if result.face_landmarks:
                    lm_return = result.face_landmarks.landmark
                
                    left = abs(math.floor(getAngle((lm_return[6].x,lm_return[6].y), (lm_return[5].x,lm_return[5].y), (lm_return[66].x,lm_return[66].y))))-20
                    right = abs(math.floor(getAngle((lm_return[6].x,lm_return[6].y), (lm_return[5].x,lm_return[5].y), (lm_return[296].x,lm_return[296].y)))-20)
                    lip = getAngle((lm_return[212].x,lm_return[212].y), (lm_return[13].x,lm_return[13].y), (lm_return[14].x,lm_return[14].y))
                    
                    fin_data = math.floor(left+right+lip)
            
            imagePIL = cv2_to_pil(img)
            imagePIL = add_corners(imagePIL, 17)
            
            imagePygame = pil_image_to_pygame_surface(imagePIL)
            imagePygame = pygame.transform.scale(imagePygame, (W/13*4+2, (W/13*4+2)*3/4))
            
            display.blit(imagePygame, (W/7-1, H/6))
        else:
            pygame.draw.rect(display, BLACK, [W/7-1, H/6, W/13*4+2, (W/13*4+2)*3/4], width=0, border_radius=15)
            display.blit(novideoImg, (W/7-1+(W/13*4+2)/2-25, H/6+((W/13*4+2)*3/4)/2-25))
        
        
        
        if buttonIndex == 1:
            if t.time()-CTIME > 3:
                if final_action != None:
                    if final_action == "nicetosee":
                        if not fin_data > 65:
                            if len(menuItems)>0:
                                message = f"{menuItems[-1]}와(과) {KoreanSMean[final_action]}을(를) 합쳐줘. 합친 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                transOutput=translator.translate(reply, dest=pLang).text
                                menuItems[-1] = transOutput
                            else:
                                transOutput=translator.translate(KoreanSMean[final_action], dest=pLang).text
                                menuItems.append(transOutput)
                                if len(menuItems) > visible_items_count:
                                    starting_index+=1
                        else:
                            if len(menuItems)>0:
                                message = f"{menuItems[-1]}와(과) {KoreanSMean[final_action]}을(를) 합쳐줘. 합친 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                
                                message = f"{reply}을(를) 의문문으로 바꿔줘. 의문문으로 바뀐 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                transOutput=translator.translate(reply, dest=pLang).text
                                menuItems[-1] = transOutput
                            else:
                                message = f"{KoreanSMean[final_action]}을(를) 의문문으로 바꿔줘. 의문문으로 바뀐 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                transOutput=translator.translate(reply, dest=pLang).text
                                menuItems.append(transOutput)
                                if len(menuItems) > visible_items_count:
                                    starting_index+=1
                    elif fin_data > 65:
                        if final_action == "higher":
                            if len(menuItems)>0:
                                message = f"{menuItems[-1]}을(를) 의문문으로 바꿔줘. 의문문으로 바뀐 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                
                                
                                message = f"{reply}을(를) 높임말로 바꿔줘. 높임말로 바뀐 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                
                                transOutput=translator.translate(reply, dest=pLang).text
                                menuItems[-1] = transOutput
                                
                        else:
                            message = f"{KoreanSMean[final_action]}을(를) 의문문으로 바꿔줘. 의문문으로 바뀐 문장만 말해. 단어 자체는 바꾸지마"
                            messages = [{"role": "user", "content": message}]
                            chat = openai.ChatCompletion.create(
                            model="gpt-4", messages=messages
                            )
                            reply = chat.choices[0].message.content
                            transOutput=translator.translate(reply, dest=pLang).text
                            menuItems.append(transOutput)
                            
                            if len(menuItems) > visible_items_count:
                                starting_index+=1
                    else:
                        if final_action == "higher":
                            if len(menuItems)>0:
                                transOutput=translator.translate(final_action, dest=pLang).text
                                message = f"{menuItems[-1]}을(를) 높임말로 바꿔줘. 높임말로 바뀐 문장만 말해. 단어 자체는 바꾸지마"
                                messages = [{"role": "user", "content": message}]
                                chat = openai.ChatCompletion.create(
                                model="gpt-4", messages=messages
                                )
                                reply = chat.choices[0].message.content
                                transOutput=translator.translate(reply, dest=pLang).text
                                menuItems[-1] = transOutput
                        else:
                            transOutput=translator.translate(KoreanSMean[final_action], dest=pLang).text
                            menuItems.append(transOutput)
                            if len(menuItems) > visible_items_count:
                                starting_index+=1
                                
                CTIME = t.time()
        
        for button in buttonList0:
            button.drawButton()
        
        try:
            for i in range(visible_items_count):
                if starting_index + i < len(menuItems):
                    if pLang in langfonts:
                        text_surface = langfonts[pLang].render(menuItems[starting_index + i], True, BLACK)
                    else:
                        text_surface = LANGFONT.render(menuItems[starting_index + i], True, BLACK)
                    y_position = i * 40  # Adjust for desired spacing
                    display.blit(text_surface, (W/20*11-1+25, H/6+25+y_position))
        except IndexError:
            pass
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    
    if Scene == 1:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList1:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    if Scene == 2:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList2:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    if Scene == 3:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList3:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    if Scene == 4:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList4:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    if Scene == 5:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList5:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    if Scene == 6:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList6:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
    if Scene == 7:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList7:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()
        
    if Scene == 8:        
        display.fill(WHITE)
        
        text = COPYRIGHTFONT.render(COPYRIGHTMESSAGE, True, BLACK)
        display.blit(text, (W/2 - text.get_width()/2, H-text.get_height()-10))
        
        display.blit(logoImg, (W/2 - 25, H-25-36-30))
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                try:
                    os.remove(f'voice{i}.mp3')
                except FileNotFoundError:
                    pass
                pygame.quit() # stop pygame
                sys.exit() # stop script
            
            if event.type == VIDEORESIZE:
                W, H = event.w,event.h
                WINDOWSIZE = (W, H)
                screen = pygame.display.set_mode(WINDOWSIZE,pygame.RESIZABLE) # initiate screen
                display = pygame.Surface(WINDOWSIZE)
        
        for button in buttonList8:
            button.drawButton()
        
        for dialog in dialogList:
            dialog.drawDialog()
            if pygame.mouse.get_pressed()[0] == 1:
                dialogList.clear()
                DIALOGON = False
        
        surf = pygame.transform.scale(display, WINDOWSIZE)
        screen.blit(surf, (0, 0))
        clock.tick(60)
        pygame.display.update()