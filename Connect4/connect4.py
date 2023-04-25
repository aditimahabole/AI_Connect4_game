import numpy as np
import pygame as pg
import sys
import math
import random
# --global variables needed---
ROWS = 6
COLS = 7
BLUE =(36, 7, 153)
BLACK =(0, 2, 3)
GREEN = (154, 236, 3)
ORANGE = (250, 159, 0)
PLAYER = 0
AI = 1
PLAYER_BALL = 1
AI_BALL = 2
WINDOW_LEN = 4
EMPTY = 0
# -----creating board-----
def create_board():
    board = np.zeros((6,7))
    return board
board = create_board()
print("--Board--")
print(board)
# -----dropping piece----
def drop_piece(board,row,col,ball):
    board[row][col] = ball
    pass
# -----valid location or not----
def is_valid_location(board, col):
    return board[ROWS-1][col] == 0
# ----get next row-------
def get_next_open_row(board,col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row
# --print board---
def show_board(board):
    print(np.flip(board,0))
    # flipping board upside down
# --winner--
def winning_move(board,ball):
    # horizontal 
    for col in range(COLS-3):
        for row in range(ROWS):
            if board[row][col] == ball and board[row][col+1] == ball and board[row][col+2] == ball and board[row][col+3] == ball:
                return True 
    # vertical
    for col in range(COLS):
        for row in range(ROWS-3):
            if board[row][col] == ball and board[row+1][col] == ball and board[row+2][col] == ball and board[row+3][col] == ball:
                return True
    # right diagonal
    for col in range(COLS-3):
        for row in range(ROWS-3):
            if board[row][col] == ball and board[row+1][col+1] == ball and board[row+2][col+2] == ball and board[row+3][col+3] == ball:
                return True
    # left diagonal
    for col in range(COLS-3):
        for row in range(3,ROWS):
            if board[row][col] == ball and board[row-1][col+1] == ball and board[row-2][col+2] == ball and board[row-3][col+3] == ball:
                return True
# --------------------------------------------------------------------------
# evaluate window
def evaluate_window(window,ball):
    score = 0
    opponent_ball  = PLAYER_BALL
    if ball == PLAYER_BALL:
        opponent_ball  = AI_BALL 
    if window.count(ball) == 4:
        score+=100
    elif window.count(ball) == 3 and window.count(EMPTY) == 1:
        score+=5
    elif window.count(ball) == 2 and window.count(EMPTY) == 2:
        score+=2
    if window.count(opponent_ball) == 3 and window.count(EMPTY) == 1:
        score -= 4
        # if AI gets 3 in a row then it will block
    return score
# score piece 
def score_position(board,ball):
    
    score = 0
    # score center col 
    center_array = [int(i) for i in list(board[:,COLS//2])] #middle col
    
    center_count = center_array.count(ball)
    score+= center_count*3
    # preferencing center

    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS-3):
            window = row_array[c : c + WINDOW_LEN]
            
            score += evaluate_window(window,ball)
    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+WINDOW_LEN]
            
            score += evaluate_window(window,ball)
    # score right diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LEN)]
            
            score += evaluate_window(window,ball)
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LEN)]
            
            score += evaluate_window(window,ball)
    return score
def is_terminal_node(board):
    return winning_move(board,PLAYER_BALL)or winning_move(board,AI_BALL) or len(get_valid_locations(board)) == 0

# min-max algorithm
def minimax(board,depth,alpha,beta,maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth ==0 or is_terminal:
        if is_terminal:
            if winning_move(board,AI_BALL):
                return (None,100000000000000)
            elif winning_move(board,PLAYER_BALL):
                return (None,-10000000000000)
            else: #GAME OVER
                return ( None,0 )
        else: #depth is zero 
            return (None,score_position(board,AI_BALL))
    if maximizing_player:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            board_copy = board.copy()
            drop_piece(board_copy,row,col,AI_BALL)
            new_score = minimax(board_copy,depth-1,alpha,beta,False)[1]
            if new_score>value:
                value = new_score
                column = col
            alpha = max(value,alpha)
            if alpha >=beta:
                break
        return column,value
    else: #minimizing player 
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            board_copy = board.copy()
            drop_piece(board_copy,row,col,PLAYER_BALL)
            new_score = minimax(board_copy,depth-1,alpha,beta,True)[1]
            if new_score<value:
                value = new_score
                column = col
            beta = min(beta,value)
            if alpha>=beta:
                break

        return column,value


# get valid locations 
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board,col):
            valid_locations.append(col)
    # here we are finding valid locations for AI
    return valid_locations
# choosing best move
def choose_best_move(board,ball):
    
    valid_locations = get_valid_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board,col)
        temp_board = board.copy()
        drop_piece(temp_board,row,col,ball)
        score = score_position(temp_board,ball)
        if score>best_score:
            best_score = score 
            best_col = col 
    return best_col

# draw board 
def draw_board(board):
    # iterate thru every spot
    for col in range(COLS):
        for row in range(ROWS):
            pg.draw.rect(screen,BLUE,(col*SQUARE_SIZE,row*SQUARE_SIZE + SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pg.draw.circle(screen,BLACK,(int(col*SQUARE_SIZE + SQUARE_SIZE/2),int(row*SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)),RADIUS)

        for col in range(COLS):
            for row in range(ROWS):
                if board[row][col] == PLAYER_BALL:
                    pg.draw.circle(screen,GREEN,(int(col*SQUARE_SIZE + SQUARE_SIZE/2),height -int(row*SQUARE_SIZE  + SQUARE_SIZE/2)),RADIUS)
                elif board[row][col] == AI_BALL:
                    pg.draw.circle(screen,ORANGE,(int(col*SQUARE_SIZE + SQUARE_SIZE/2),height -int(row*SQUARE_SIZE  + SQUARE_SIZE/2)),RADIUS)
    pg.display.update()
# -------------------------------------------------------------------
# initializing py-game
pg.init()
SQUARE_SIZE = 100
width = COLS * SQUARE_SIZE
height = (ROWS+1) * SQUARE_SIZE
size = (width,height)
RADIUS = int(SQUARE_SIZE/2 - 5)
screen = pg.display.set_mode(size)
my_font = pg.font.SysFont("monospace",75)
draw_board(board)
pg.display.update()
# --------------------------------------------------------------------------
# -----starting game------
game_over = False
turn = random.randint(PLAYER,AI)
while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEMOTION:
            pg.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
            posx = event.pos[0]
            if(turn == PLAYER):
                pg.draw.circle(screen,GREEN,(posx,int(SQUARE_SIZE/2)),RADIUS)
        pg.display.update()


        if event.type == pg.MOUSEBUTTONDOWN:
            pg.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
            print(event.pos)
            # ask for player 1 input 
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))
                print("Selection made by P1 : ",col)
                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,PLAYER_BALL)

                    if winning_move(board,PLAYER_BALL):
                        label = my_font.render("Player 1 Wins!",1,GREEN)
                        screen.blit(label,(40,10))
                        game_over = True
                    turn+=1
                    turn = turn % 2 # 0 , 1

                    print("---CURRENT BOARD--")
                    show_board(board)
                    draw_board(board)

    # ask for player 2 input
    if turn == AI and not game_over:
        # col = random.randint(0,COLS-1)
        # col = choose_best_move(board,AI_BALL)
        col,minimax_score = minimax(board,5,-math.inf,math.inf,True)
        print("Selection made by AI : ",col)
        if is_valid_location(board,col):
            pg.time.wait(200)
            row = get_next_open_row(board,col)
            drop_piece(board,row,col,AI_BALL)
            if winning_move(board,AI_BALL):
                label = my_font.render("AI Wins!",1,ORANGE)
                screen.blit(label,(40,10))
                game_over = True
                        
            print("---CURRENT BOARD--")
            show_board(board)
            draw_board(board)
            turn+=1
            turn = turn % 2 # 0 , 1
    if game_over:
        pg.time.wait(3000)





