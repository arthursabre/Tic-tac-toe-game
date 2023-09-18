import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg 
from pygame import mixer
import pygame_menu
import sys 
import csv
import time 
from pygame.locals import *
import qlearning as ql



N = 3

SIZE = N ** 2

#   INITIALIZING DIMENSIONS OF THE GAME SCREEN
width, height = 400, 400

#   LIST CONTAINING COORDINATES OF THE CENTRE OF EACH SQUARE ON THE GRID
POSITIONS = list(zip([30, width / 3 + 30, width / 3 * 2 + 30] * 3, [30] * 3 + [height / 3 + 30] * 3 + [height / 3 * 2 + 30] * 3))

#   LIST CONTAINING THE COORDINATES OF THE EXTREMITIES (BOTTOM RIGHT CORNER) OF EACH SQUARE ON THE GRID
LIMITS = list(zip([width / 3, width / 3 * 2, width] * 3, [height / 3] * 3 + [height / 3 * 2] * 3 + [height] * 3))
                
ROW1 = (0, 1, 2)
ROW2 = (3, 4, 5)
ROW3 = (6, 7, 8)

COL1 = (0, 3, 6)
COL2 = (1, 4, 7)
COL3 = (2, 5, 8)

LDIAG = (0, 4, 8)
RDIAG = (2, 4, 6)
 
CHECK = [ROW1, ROW2, ROW3, COL1, COL2, COL3, LDIAG, RDIAG]
               
white = (255, 255, 255) 
black = (0, 0, 0)
red = (255, 0, 0)

line_color = black 

CROSS = 'X'
NOUGHT = 'O'
EMPTY = '-'

# INITIALIZNG PYGAME
pg.init() 

fps = 30

CLOCK = pg.time.Clock() 

screen = pg.display.set_mode((width, height + 100), 0, 32) 

pg.display.set_caption("Tic Tac Toe") 

# DICTIONARY STORING LINES IN THE GRID AS KEYS AND PARAMETERS REQUIRED TO DRAW THE RED LINE THROUGH THEM ON WINNING

LINEARGS = {
    ROW1 : (screen, red, (20, height / 6), (width - 20, height / 6), 4),
    ROW2 : (screen, red, (20, height / 2), (width - 20, height / 2), 4),
    ROW3 : (screen, red, (20, height / 6 * 5), (width - 20, height / 6 * 5), 4),
    COL1 : (screen, red, (width / 6, 20), (width / 6, height - 20), 4),
    COL2 : (screen, red, (width / 2, 20), (width / 2, height - 20), 4),
    COL3 : (screen, red, (width / 6 * 5, 20), (width / 6 * 5, height - 20), 4),
    LDIAG: (screen, red, (50, 50), (350, 350), 4),
    RDIAG: (screen, red, (350, 50), (50, 350), 4)
    }

start_image=pg.image.load("start_image.jpeg")
loading_image=pg.image.load("loading2.jpg")
initiating_window = pg.image.load("bg1.png") 
x_img = pg.image.load("cross.png") 
y_img = pg.image.load("nought.png") 


loading_image=pg.transform.scale(loading_image,(300,300))
start_image=pg.transform.scale(start_image, (width, height + 100))
initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

ICON = {CROSS : x_img, NOUGHT : o_img}


#Music sounds 
computer_play=pg.mixer.Sound("computer_play.wav")
choice=pg.mixer.Sound("option_choice.wav")
user_play=pg.mixer.Sound("user_play.wav")
winner_ai=pg.mixer.Sound("winner_ai.wav")
winner_user=pg.mixer.Sound("winner_user.wav")
draw=pg.mixer.Sound("draw.wav")

#open game
screen.blit(start_image,(0,0))
for event in pg.event.get():
    if event.type==QUIT:
        pg.quit()
        sys.exit()
        
pg.display.update()
time.sleep(2)
pg.mixer.music.load('game_start.mp3')
pg.mixer.music.play()
time.sleep(3)

#loading


def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pg.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pg.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    

pos=(screen.get_width()/2,screen.get_height()/2)
w,h=loading_image.get_size()
angle=0
percent=0
screen.fill(white)
while (True and percent<100):
    for event in pg.event.get():
        if event.type==QUIT:
            pg.quit()
            sys.exit()
    percent+=1
    angle+=30
    blitRotate(screen,loading_image,pos,(w/2,h/2),angle)
    pg.display.update()
    message="Loading files ..."+str(percent)+"%"
    font = pg.font.Font(pg.font.get_default_font(), 30) 
    text = font.render(message, 1, black) 
    screen.fill(white,(0,400,500,100))
    text_rect=text.get_rect(center=(width/2,500-50))
    screen.blit(text,text_rect)
    pg.display.update()
    time.sleep(0.1)

time.sleep(0.5)
filename = 'q_values.csv'



class TicTacToe():

    def __init__(self):
        self.player = CROSS
        self.winner = None
        self.draw = False
        self.board = [EMPTY] * SIZE

    def game_initiating_window(self): 
        ''' This function initialises the game window with the background image for 1.5 seconds
        before showing an empty grid for a new game '''
  
        screen.blit(initiating_window, (0, 0)) 
    
        pg.display.update() 
        time.sleep(1.5)                    
        screen.fill(white) 

        pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
        pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

        pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
        pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 
        
        message=self.player+ "'s Turn"
        
        font = pg.font.Font(pg.font.get_default_font(), 30) 
    
        text = font.render(message, 1, white) 

        screen.fill(black, (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(width / 2, 500-50)) 
        screen.blit(text, text_rect) 
        pg.display.update() 

        
    def check_win(self):
        ''' This functions checks if a winner is determined at the given state of the game '''

        for line in CHECK:
            if self.board[line[0]] == EMPTY:
                continue
            if all(self.board[play] == self.board[line[0]] for play in line[1:]):
                pg.draw.line(*LINEARGS[line])
                self.winner = self.board[line[0]]

    def _check_win(self):
        for line in CHECK:
            if self.board[line[0]] == EMPTY:
                continue
            if all(self.board[play] == self.board[line[0]] for play in line[1:]):
                self.winner = self.board[line[0]]

    def check_draw(self):
        ''' This functions checks if there are no available valid moves for any player (all squares occupied). 
        This is the draw condition if there is no winner '''

        self.draw = all(play != EMPTY for play in self.board)

    def playable(self):
        self.check_win()
        self.check_draw()
        return not self.draw and not self.winner

    def game_status(self): 
        ''' This function prints the status of the game currently by deciding 
        and displaying the message at the bottom of the grid on the game screen '''
 
        if self.winner: 
            message = self.winner + " won !"
        elif self.draw: 
            message = "Game Draw !"
            draw.play()
        else: 
            
            message = self.player + "'s Turn"

        font = pg.font.Font(pg.font.get_default_font(), 30) 
    
        text = font.render(message, 1, white) 

        screen.fill(black, (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(width / 2, 500-50)) 
        screen.blit(text, text_rect) 
        pg.display.update() 
    
    
    def make_move(self, pos):
        ''' This function assigns the value at a particular position on the board and 
        displays the appropriate icon at the required position on the game screen '''

        posx, posy = POSITIONS[pos]
        self.board[pos] = self.player 
        screen.blit(ICON[self.player], (posx, posy))
        pg.display.update() 
        self.flip()
        self.check_win()
        self.check_draw()

    def _make_move(self, pos):
        self.board[pos] = self.player
        self.flip()
        self._check_win()
        self.check_draw()

    def get_square(self):
        ''' This function returns the index of the board 
        depending on where the user has clicked on the game screen '''
        
        x, y = pg.mouse.get_pos() 
        for idx, limit in enumerate(LIMITS):
            xlim, ylim = limit
            if x < xlim and y < ylim:
                return idx
        return None

    def user_click(self):
        ''' This function updates the board and game status on user click on the game screen '''
        pos=None
        while pos==None:
            ev = pg.event.get()
            for event in ev:
                if event.type == pg.MOUSEBUTTONUP:
                    pos =self.get_square()
                    idx=self.get_square()
                    if idx==None:
                        pos=None
                    else:
                        if self.board[idx]==EMPTY:
                            self.make_move(idx)
                        else:
                            pos=None
                        
    def random_play(self):
        move=random.choice(self.valid_moves())
        self.make_move(move)
        self._check_win()
        self.check_draw()
                     
        
    def flip(self):
        ''' This function allows the switching of move control between the two players '''

        if self.player == NOUGHT:
            self.player = CROSS
        else:
            self.player = NOUGHT

    def valid_moves(self):
        ''' This function returns a list of valid moves on the board '''

        return [idx for idx, item in enumerate(self.board) if item == EMPTY]



class minmaxagent():
   
    
    def __init__(self,game_class,value_player='X'):
        self.value_player=value_player
        self.NewGame=game_class
    
    def utility(self,game):
        if game.winner:
            if game.winner==self.value_player:
                return 1
            else:
                return -1
        else:
            return 0

    
    def minimax(self,game):
        if game.playable()==False:
            return None
        elif game.player==self.value_player:
            value,move=self.max_value(game)
            return move
        else:
            value,move=self.min_value(game)
            return move
        
    def max_value(self,game):
        if game.winner or game.draw:
            return self.utility(game),None
        v=float('-inf')
        move=None
        for action in game.valid_moves():
            mygame=self.NewGame()
            mygame.board=game.board.copy()
            mygame.player=game.player
            mygame._make_move(action)
            val,act=self.min_value(mygame)
            if val>v:
                v=val
                move=action
                if v==1:
                    return v,move
        return v,move
    
    def min_value(self,game):
        if game.winner or game.draw:
            return self.utility(game),None
        v=float('inf')
        move=None
        for action in game.valid_moves():
            mygame=self.NewGame()
            mygame.board=game.board.copy()
            mygame.player=game.player
            mygame._make_move(action)
            val,act=self.max_value(mygame)
            if val<v:
                v=val
                move=action
                if v==-1:
                    return v,move
        return v,move

    def interactive(self, agent_player='O'):
        pg.mixer.music.stop()
        game=self.NewGame()
        self.value_player=agent_player
        game.game_initiating_window()
        end=False
        while not end:
            for event in pg.event.get():
                if event.type==QUIT:
                    pg.quit()
                    sys.exit()
            if game.player==agent_player:
                time.sleep(0.1)
                move=self.minimax(game)
                game.make_move(move)
                computer_play.play()
                game.game_status()
            else:
                game.user_click()
                user_play.play()
                game.game_status()
            if game.winner or game.draw:
                time.sleep(1.5)
                if game.winner:
                    if game.winner==agent_player:
                        winner_ai.play()
                    else:
                        winner_user.play()
                time.sleep(1.5)
                end=True
                break
        pg.display.update()
        CLOCK.tick(fps)
        pg.mixer.music.play(-1)


def play_CROSS():
    ''' This function allows interactive play where agent plays second '''
    agent.interactive()

def play_NOUGHT():
    ''' This function allows interactive play where agent plays first '''
    agent.interactive(agent_player = CROSS)

def play_users():
    choice.play()
    def play_CROSS1():
        choice.play()
        mymenu.disable()
        
    def play_NOUGHT1():
        choice.play()
        game.player=NOUGHT
        mymenu.disable()
    
    game=agent.NewGame()     
        
    mymenu = pygame_menu.Menu('Tic Tac Toe',height,width)     
    mymenu.add.text_input("Choose symbol", font_color = white, font_size = 40)
    mymenu.add.button(CROSS,play_CROSS1) 
    mymenu.add.button(NOUGHT, play_NOUGHT1)
    mymenu.mainloop(screen)
    
    
    pg.mixer.music.stop()
    game.game_initiating_window()
    game.game_status
    end=True
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            else:
                game.user_click()
                if game.player==CROSS:
                    user_play.play()
                else:
                    computer_play.play()
                game.game_status()
            if game.winner or game.draw:
                if game.winner:
                    winner_user.play()
                time.sleep(1.5)
                end = False
                break
    pg.display.update()
    CLOCK.tick(fps)
    pg.mixer.music.play()


    
    
def play_AI():
    choice.play()
    def play_CROSS1():
        choice.play()
        mymenu.disable()
        play_CROSS()
    def play_NOUGHT1():
        choice.play()
        mymenu.disable()
        play_NOUGHT()
    mymenu = pygame_menu.Menu('Tic Tac Toe',height,width) 
    mymenu.add.text_input("Choose symbol", font_color = white, font_size = 40)
    mymenu.add.button(CROSS, play_CROSS1) 
    mymenu.add.button(NOUGHT, play_NOUGHT1)
    mymenu.mainloop(screen)
    

def play_ql():
    choice.play()
    def play_CROSS1():
        choice.play()
        mymenu.disable()
        myagent.interactive()
    def play_NOUGHT1():
        choice.play()
        mymenu.disable()
        myagent.interactive(agent_player=CROSS)
    mymenu = pygame_menu.Menu('Tic Tac Toe',height,width) 
    mymenu.add.text_input("Choose symbol", font_color = white, font_size = 40)
    mymenu.add.button(CROSS, play_CROSS1) 
    mymenu.add.button(NOUGHT, play_NOUGHT1)
    mymenu.mainloop(screen)    
  


def vs_AI():
    game=TicTacToe()
    agent.value_player=NOUGHT
    pg.mixer.music.stop()
    game.game_initiating_window()
    game.game_status
    end=True
    while end:
        for event in pg.event.get():
            if event.type==QUIT:
                pg.quit()
                sys.exit()
        if game.player==agent.value_player:
            time.sleep(0.5)
            move=agent.minimax(game)
            game.make_move(move)
            computer_play.play()
            game.game_status()
        else:
            time.sleep(0.5)
            move=myagent.play_select_move(game)
            game.make_move(move)
            user_play.play()
            game.game_status
        if game.winner or game.draw:
            time.sleep(1.5)
            if game.winner:
                winner_user.play()
            time.sleep(1.5)
            end=True
            break
    pg.display.update()
    CLOCK.tick(fps)
    pg.mixer.music.play(-1)




agent = minmaxagent(TicTacToe)
myagent=ql.Agent(TicTacToe)
mytheme = pygame_menu.themes.Theme(title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE, title_background_color = (4, 47, 126), title_font = pygame_menu.font.FONT_OPEN_SANS_ITALIC, background_color = (0, 60, 255, 100) )
n_height=height+99
n_width=width-1
menu = pygame_menu.Menu('Tic Tac Toe',height,width)  #theme = mytheme)
while True:
    pg.mixer.music.load('background.mp3')
    pg.mixer.music.play(-1)
    time.sleep(2)
    menu.add.text_input("Choose player", font_color = white, font_size = 40)
    menu.add.button("p1 vs p2", play_users) # font_size = 60, font_color = white, shadow = True)
    menu.add.button("p1 vs MinMax", play_AI)
    menu.add.button("p1 vs qlearning", play_ql)
    menu.add.button("qlearning vs MinMax", vs_AI)
    # font_size = 60, font_color = white, shadow = True)
    menu.mainloop(screen)