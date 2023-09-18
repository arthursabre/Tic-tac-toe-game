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


class globe():
    def __init__(self):
        self.N = 3

        self.SIZE = self.N ** 2

#   INITIALIZING DIMENSIONS OF THE GAME SCREEN
        self.width= 400
        self.height=400

#   LIST CONTAINING COORDINATES OF THE CENTRE OF EACH SQUARE ON THE GRID
        self.POSITIONS = list(zip([30, self.width / 3 + 30, self.width / 3 * 2 + 30] * 3, [30] * 3 + [self.height / 3 + 30] * 3 + [self.height / 3 * 2 + 30] * 3))

#   LIST CONTAINING THE COORDINATES OF THE EXTREMITIES (BOTTOM RIGHT CORNER) OF EACH SQUARE ON THE GRID
        self.LIMITS = list(zip([self.width / 3, self.width / 3 * 2, self.width] * 3, [self.height / 3] * 3 + [self.height / 3 * 2] * 3 + [self.height] * 3))
                
        self.ROW1 = (0, 1, 2)
        self.ROW2 = (3, 4, 5)
        self.ROW3 = (6, 7, 8)

        self.COL1 = (0, 3, 6)
        self.COL2 = (1, 4, 7)
        self.COL3 = (2, 5, 8)

        self.LDIAG = (0, 4, 8)
        self.RDIAG = (2, 4, 6)
 
        self.CHECK = [self.ROW1, self.ROW2, self.ROW3, self.COL1, self.COL2, self.COL3, self.LDIAG, self.RDIAG]
               
        self.white = (255, 255, 255) 
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

        self.line_color = self.black 

        self.CROSS = 'X'
        self.NOUGHT = 'O'
        self.EMPTY = '-'

# INITIALIZNG PYGAME
        pg.init() 

        self.fps = 30

        self.CLOCK = pg.time.Clock() 

        self.screen = None

        pg.display.set_caption("Tic Tac Toe") 

# DICTIONARY STORING LINES IN THE GRID AS KEYS AND PARAMETERS REQUIRED TO DRAW THE RED LINE THROUGH THEM ON WINNING

        self.LINEARGS = {
    self.ROW1 : (self.screen, self.red, (20, self.height / 6), (self.width - 20, self.height / 6), 4),
    self.ROW2 : (self.screen, self.red, (20, self.height / 2), (self.width - 20, self.height / 2), 4),
    self.ROW3 : (self.screen, self.red, (20, self.height / 6 * 5), (self.width - 20, self.height / 6 * 5), 4),
    self.COL1 : (self.screen, self.red, (self.width / 6, 20), (self.width / 6, self.height - 20), 4),
    self.COL2 : (self.screen, self.red, (self.width / 2, 20), (self.width / 2, self.height - 20), 4),
    self.COL3 : (self.screen, self.red, (self.width / 6 * 5, 20), (self.width / 6 * 5, self.height - 20), 4),
    self.LDIAG: (self.screen, self.red, (50, 50), (350, 350), 4),
    self.RDIAG: (self.screen, self.red, (350, 50), (50, 350), 4)
    }


        self.initiating_window = pg.image.load("bg1.png") 
        self.x_img = pg.image.load("cross.png") 
        self.y_img = pg.image.load("nought.png") 

        self.initiating_window = pg.transform.scale(self.initiating_window, (self.width, self.height + 100)) 
        self.x_img = pg.transform.scale(self.x_img, (80, 80)) 
        self.o_img = pg.transform.scale(self.y_img, (80, 80)) 

        self.ICON = {self.CROSS : self.x_img, self.NOUGHT : self.o_img}


#Music sounds 
        self.computer_play=pg.mixer.Sound("computer_play.wav")
        self.choice=pg.mixer.Sound("option_choice.wav")
        self.user_play=pg.mixer.Sound("user_play.wav")
        self.winner_ai=pg.mixer.Sound("winner_ai.wav")
        self.winner_user=pg.mixer.Sound("winner_user.wav")
        self.draw=pg.mixer.Sound("draw.wav")
        self.filename='q_values.csv'


    



class TicTacToe():

    def __init__(self):
        self.globe=globe()
        self.change()
        self.player = CROSS
        self.winner = None
        self.draw = False
        self.board = [EMPTY] * SIZE
    def change(self):
        global screen
        global width
        global height
        global EMPTY
        global SIZE
        global CROSS
        global NOUGHT
        global ICON
        global LIMITS
        global CHECK
        global LINEARGS
        global draw
        global white
        global black
        global red
        global initiating_window
        global filename
        global line_color
        global POSITIONS
        screen=self.globe.screen
        width=self.globe.width
        height=self.globe.height
        EMPTY=self.globe.EMPTY
        SIZE=self.globe.SIZE
        CROSS=self.globe.CROSS
        NOUGHT=self.globe.NOUGHT
        ICON=self.globe.ICON
        LIMITS=self.globe.LIMITS
        CHECK=self.globe.CHECK
        LINEARGS=self.globe.LINEARGS
        draw=self.globe.draw
        white=self.globe.white
        black=self.globe.black
        red=self.globe.red
        initiating_window=self.globe.initiating_window
        filename=self.globe.filename
        line_color=self.globe.line_color
        POSITIONS=self.globe.POSITIONS
    
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
    
    def _playable(self):
        self._check_win()
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





class Agent():
        def __init__(self, game_class, epsilon = 0.1, alpha = 0.5,gamma=0.9, value_player = 'X',user='O'):
            self.sound()
            self.q_value = dict()
            self.NewGame = game_class
            self.epsilon = epsilon
            self.alpha = alpha
            self.value_player = value_player
            self.user=user
            self.gamma=gamma
            self.stat=0
        def sound(self):
            global var
            var=globe()
        
        def learning_episode(self,n_episodes=1000):
            for episode in range(n_episodes):
                self.learning()
         
                    
        def learning(self): 
            self.retrieve_q_table()
            game=self.NewGame()
            _,move=self.learn_select_move(game)
            while move:
                move=self.learn_from_move(game,move)
            self.save_q_table()
            
        def learn_select_move(self, game):
            ''' donne le prochain move à effectuer selon e-greedy, on suppose
            que celui qui entraine agent veut minimiser sa q value'''
            allowed_moves = self.couple_values(self.form_state(game.board[:]),game.valid_moves())  
            if game.player==self.value_player:
                best_move = self.choose_move(allowed_moves,True)
            else:
                best_move=self.choose_move(allowed_moves,False)
             
            selected_move=best_move
            if random.random() < self.epsilon :
                selected_move = self.__random_q(game.valid_moves())
            return best_move,selected_move
        
        def learn_from_move(self, game, move):
            board=game.board[:]
            current_state=self.form_state(board)
            current_q_value=self.couple_value(current_state,move)
            next_state_q_value=0.0
            selected_next_move=None
            game._make_move(move)
            r = self.__reward(game)
            if game._playable():
                newboard=game.board[:]
                next_state=self.form_state(newboard)
                best_next_move,selected_next_move=self.learn_select_move(game)
                next_state_q_value=self.couple_value(next_state,best_next_move)
            td_target = r + self.gamma*next_state_q_value
            self.q_value[(current_state,move)]=current_q_value + self.alpha * (td_target - current_q_value)
            return selected_next_move


        def couple_values(self,state,moves):
            return dict(((state,move),self.couple_value(state,move)) for move in moves)
        
        def couple_value(self,state,move):
            return self.q_value.get((state,move),0.0)
        
        def choose_move(self,couple_values, is_agent_player):#doit retourner le move qui maximise q(state,move) 
            values=couple_values.values()
            val=max(values) if is_agent_player else min(values)
            chosen_move=random.choice([move for ((state,move),q) in couple_values.items()  if q==val])
            return chosen_move
        
        def form_state(self,board):
            return ''.join(board)
            
        def __reward(self, game):
            ''' récompense associé à un état donné '''
            if game.winner == self.value_player:
                return 1.0
            elif game.winner==self.user:
                return -1.0
            else:
                return 0.0

        def __random_q(self,moves):
            return random.choice(moves)
        
        def interactive(self, agent_player='O',user_player='X'):
            pg.mixer.music.stop()
            self.retrieve_q_table()
            game=self.NewGame()
            game.game_initiating_window()
            end=False
            while not end:
                for event in pg.event.get():
                    if event.type==QUIT:
                        pg.quit()
                        sys.exit()
                if game.player==agent_player:
                    time.sleep(0.5)
                    move=self.play_select_move(game)
                    game.make_move(move)
                    var.computer_play.play()
                    game.game_status()
                else:
                    game.user_click()
                    var.user_play.play()
                    game.game_status()
                if game.winner or game.draw:
                    if game.winner==user_player:
                        var.winner_user.play()
                    if game.winner==agent_player:
                        var.winner_ai.play()
                    time.sleep(1.5)
                    end=True
                    break
            pg.display.update()
            var.CLOCK.tick(var.fps)
            pg.mixer.music.play(-1)
            
            
        def play_select_move(self,game):
            allowed_moves = self.couple_values(self.form_state(game.board[:]),game.valid_moves())
            if game.player==self.value_player:
                return self.choose_move(allowed_moves,True)
            return self.choose_move(allowed_moves,False)

            
                       
        def save_q_table(self):
            '''Cette fonction sauvegarde les q values dans un fichier csv'''
            filename='q_values.csv'
            with open(filename, 'w', newline='') as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(['State,move','QValue'])
                all_states=list(self.q_value.keys())
                all_states.sort()
                for state in all_states:
                    writer.writerow([state,self.q_value[state]])
        
        def retrieve_q_table(self):
            '''récupère la q value d un fichier csv'''
            filename='q_values.csv'
            if os.path.isfile(filename):
                with open(filename,'r') as csvfile:
                    reader=csv.reader(csvfile)
                    for row in reader:
                        if row==['State,move','QValue']:
                            continue
                        self.q_value[(row[0][2:11],int(row[0][14]))]=float(row[1])
                        

        def demo_game(self):
            game=self.NewGame()
            self.retrieve_q_table
            while game._playable():
                move=self.play_select_move(game)
                game._make_move(move)
            if game.winner:
                if game.winner==self.value_player:
                    return 'W'
                else:
                    return 'L'
            return 'D'
            
    

