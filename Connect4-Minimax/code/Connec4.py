#!/usr/bin/env python
# coding: utf-8

# Game Assignment
# 
# Ali Pakdel Samadi
# 
# 810198368

# In[6]:


from random import random
from random import shuffle
import copy
import time
from tqdm import tqdm
import numpy as np


# In[7]:


class ConnectSin:
    YOU = 1
    CPU = -1
    EMPTY = 0
    DRAW = 0
    __CONNECT_NUMBER = 4
    board = None
    INFINITY = 9999999

    def __init__(self, board_size=(6, 7), silent=False):
        """
        The main class for the connect4 game

        Inputs
        ----------
        board_size : a tuple representing the board size in format: (rows, columns)
        silent     : whether the game prints outputs or not
        """
        assert len(board_size) == 2, "board size should be a 1*2 tuple"
        assert board_size[0] > 4 and board_size[1] > 4, "board size should be at least 5*5"

        self.columns = board_size[1]
        self.rows = board_size[0]
        self.silent = silent
        self.board_size = self.rows * self.columns
        
        self.depth = 1
        self.pruning = False
        self.nodes_visited = 0
        
    def set_depth(self, d):
        self.depth = d
        
    def enable_pruning(self):
        self.pruning = True
    
    def get_nodes_visited(self):
        return self.nodes_visited

    def run(self, starter=None):
        """
        runs the game!

        Inputs
        ----------
        starter : either -1,1 or None. -1 if cpu starts the game, 1 if you start the game. None if you want the starter
            to be assigned randomly 

        Output
        ----------
        (int) either 1,0,-1. 1 meaning you have won, -1 meaning the player has won and 0 means that the game has drawn
        """
        if (not starter):
            starter = self.__get_random_starter()
        assert starter in [self.YOU, self.CPU], "starter value can only be 1,-1 or None"
        
        self.__init_board()
        turns_played = 0
        current_player = starter
        while(turns_played < self.board_size):
            
            if (current_player == self.YOU):
                self.__print_board()
                player_input = self.get_your_input()
            elif (current_player == self.CPU):
                player_input = self.__get_cpu_input()
            else:
                raise Exception("A problem has happend! contact no one, there is no fix!")
            if (not self.register_input(player_input, current_player)):
                self.__print("this move is invalid!")
                continue
            current_player = self.__change_turn(current_player)
            potential_winner = self.check_for_winners()
            turns_played += 1
            if (potential_winner != 0):
                self.__print_board()
                self.__print_winner_message(potential_winner)
                return potential_winner
        self.__print_board()
        self.__print("The game has ended in a draw!")
        return self.DRAW

    def get_your_input(self):
        """
        gets your input

        Output
        ----------
        (int) an integer between 1 and column count. the column to put a piece in
        """
        temp_board = copy.deepcopy(self.board)
        alpha = -self.INFINITY
        beta = self.INFINITY
        best_col = self.__minimax(self.depth, self.YOU, alpha, beta)[1]
        self.board = temp_board
        return best_col

    
    def __minimax(self, depth, player_id, alpha, beta):
        self.nodes_visited += 1
        valid_moves = self.get_possible_moves()
       
        y_counts = sum(row.count(self.YOU) for row in self.board)
        c_counts = sum(row.count(self.CPU) for row in self.board)
        if y_counts >= self.__CONNECT_NUMBER or c_counts >= self.__CONNECT_NUMBER:            
            winner = self.check_for_winners()
            if winner == self.YOU:
                return (self.INFINITY, None)
            elif winner == self.CPU:
                return (-self.INFINITY, None)
            elif len(valid_moves) == 0:
                return (0, None)
    
        if depth <= 0:
            return (self.__heuristic(self.YOU), None)
        
        if self.pruning:
            shuffle(valid_moves)
            
        col = valid_moves[0]
        best_value = self.INFINITY
        if player_id == self.YOU:
            best_value = -self.INFINITY
        
        
        board_temp = copy.deepcopy(self.board)
        for move in valid_moves:
            self.register_input(move, player_id)

            new_value = self.__minimax(depth - 1, -1 * player_id, alpha, beta)[0]
            
            if player_id == self.YOU:
                if new_value > best_value:
                    best_value = new_value
                    col = move
                    
                if self.pruning:
                    alpha = max(alpha, best_value)
                    if alpha >= beta:
                        break
            else:
                if new_value < best_value:
                    best_value = new_value
                    col = move
                    
                if self.pruning:
                    beta = min(beta, best_value)
                if beta <= alpha:
                    break
                    
            self.board = copy.deepcopy(board_temp)
                            
        return (best_value, col)
                      
    def __heuristic(self, player_id):
        value = 0
        
        opp_id = self.CPU
        if player_id == self.CPU:
            opp_id = self.YOU
        
        
        value += self.__center_values(player_id, value)
        value += self.__horizental_values(player_id, opp_id, value)
        value += self.__vertical_values(player_id, opp_id, value)
        value += self.__pos_diagonal_values(player_id, opp_id, value)
        value += self.__neg_diagonal_values(player_id, opp_id, value)
        
        return value

    def __center_values(self, player_id, value):
        board = np.array(self.board)
        center_array = [int(i) for i in list(board[:, self.columns // 2])]
        value += center_array.count(player_id) * 3
        return value
        
    def __horizental_values(self, player_id, opp_id, value):
        
        for i in range(self.rows):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                player_pieces = 0
                opp_pieces = 0
                empty_pieces = 0
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i][j + x] == player_id:
                        player_pieces += 1
                    elif self.board[i][j + x] == opp_id:
                        opp_pieces += 1
                    else:
                        empty_pieces += 1
                value += self.__calculate_value(player_pieces, opp_pieces, empty_pieces)
        return value
    
    def __vertical_values(self, player_id, opp_id, value):
        
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns):
                player_pieces = 0
                opp_pieces = 0
                empty_pieces = 0
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j] == player_id:
                        player_pieces += 1
                    elif self.board[i + x][j] == opp_id:
                        opp_pieces += 1
                    else:
                        empty_pieces += 1
                value += self.__calculate_value(player_pieces, opp_pieces, empty_pieces)
        return value
    
    def __pos_diagonal_values(self, player_id, opp_id, value):
        
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                player_pieces = 0
                opp_pieces = 0
                empty_pieces = 0
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j + x] == player_id:
                        player_pieces += 1
                    elif self.board[i + x][j + x] == opp_id:
                        opp_pieces += 1
                    else:
                        empty_pieces += 1
                value += self.__calculate_value(player_pieces, opp_pieces, empty_pieces)
        return value 
    
    def __neg_diagonal_values(self, player_id, opp_id, value):

        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                player_pieces = 0
                opp_pieces = 0
                empty_pieces = 0
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + self.__CONNECT_NUMBER - 1 - x][j + x] == player_id:
                        player_pieces += 1
                    elif self.board[i + self.__CONNECT_NUMBER - 1 - x][j + x] == opp_id:
                        opp_pieces += 1
                    else:
                        empty_pieces += 1
                value += self.__calculate_value(player_pieces, opp_pieces, empty_pieces)
        return value 
        
    def __calculate_value(self, player_pieces, opp_pieces, empty_pieces):
        
        value = 0
        
        if opp_pieces == self.__CONNECT_NUMBER - 1 and empty_pieces == self.__CONNECT_NUMBER - 3:
            value -= 7
        
        if player_pieces == self.__CONNECT_NUMBER:
            value += 100
        elif player_pieces == self.__CONNECT_NUMBER - 1 and empty_pieces == self.__CONNECT_NUMBER - 3:
            value += 10
        elif player_pieces == self.__CONNECT_NUMBER - 2 and empty_pieces == self.__CONNECT_NUMBER - 2:
            value += 5
            
        return value
    
    def check_for_winners(self):
        """
        checks if anyone has won in this position

        Output
        ----------
        (int) either 1,0,-1. 1 meaning you have won, -1 meaning the player has won and 0 means that nothing has happened
        """
        have_you_won = self.check_if_player_has_won(self.YOU)
        if have_you_won:
            return self.YOU
        has_cpu_won = self.check_if_player_has_won(self.CPU)
        if has_cpu_won:
            return self.CPU
        return self.EMPTY

    def check_if_player_has_won(self, player_id):
        """
        checks if player with player_id has won

        Inputs
        ----------
        player_id : the id for the player to check

        Output
        ----------
        (boolean) true if the player has won in this position
        """
        return (
            self.__has_player_won_diagonally(player_id)
            or self.__has_player_won_horizentally(player_id)
            or self.__has_player_won_vertically(player_id)
        )
    
    def is_move_valid(self, move):
        """
        checks if this move can be played

        Inputs
        ----------
        move : the column to place a piece in, in range [1, column count]

        Output
        ----------
        (boolean) true if the move can be played
        """
        if (move < 1 or move > self.columns):
            return False
        column_index = move - 1
        return self.board[0][column_index] == 0
    
    def get_possible_moves(self):
        """
        returns a list of possible moves for the next move

        Output
        ----------
        (list) a list of numbers of columns that a piece can be placed in
        """
        possible_moves = []
        for i in range(self.columns):
            move = i + 1
            if (self.is_move_valid(move)):
                possible_moves.append(move)
        return possible_moves
    
    def register_input(self, player_input, current_player):
        """
        registers move to board, remember that this function changes the board

        Inputs
        ----------
        player_input : the column to place a piece in, in range [1, column count]
        current_player: ID of the current player, either self.YOU or self.CPU

        """
        if (not self.is_move_valid(player_input)):
            return False
        self.__drop_piece_in_column(player_input, current_player)
        return True

    def __init_board(self):
        self.board = []
        for i in range(self.rows):
            self.board.append([self.EMPTY] * self.columns)

    def __print(self, message: str):
        if not self.silent:
            print(message)

    def __has_player_won_horizentally(self, player_id):
        for i in range(self.rows):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_vertically(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_diagonally(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + self.__CONNECT_NUMBER - 1 - x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __get_random_starter(self):
        players = [self.YOU, self.CPU]
        return players[int(random() * len(players))]
    
    def __get_cpu_input(self):
        """
        This is where clean code goes to die.
        """
        bb = copy.deepcopy(self.board)
        pm = self.get_possible_moves()
        for m in pm:
            self.register_input(m, self.CPU)
            if (self.check_if_player_has_won(self.CPU)):
                self.board = bb
                return m
            self.board = copy.deepcopy(bb)
        if (self.is_move_valid((self.columns // 2) + 1)):
            c = 0
            cl = (self.columns // 2) + 1
            for x in range(self.rows):
                if (self.board[x][cl] == self.CPU):
                    c += 1
            if (random() < 0.65):
                return cl
        return pm[int(random() * len(pm))]
    
    def __drop_piece_in_column(self, move, current_player):
        last_empty_space = 0
        column_index = move - 1
        for i in range(self.rows):
            if (self.board[i][column_index] == 0):
                last_empty_space = i
        self.board[last_empty_space][column_index] = current_player
        return True
        
    def __print_winner_message(self, winner):
        if (winner == self.YOU):
            self.__print("congrats! you have won!")
        else:
            self.__print("gg. CPU has won!")
    
    def __change_turn(self, turn):
        if (turn == self.YOU): 
            return self.CPU
        else:
            return self.YOU

    def __print_board(self):
        if (self.silent): return
        print("Y: you, C: CPU")
        for i in range(self.rows):
            for j in range(self.columns):
                house_char = "O"
                if (self.board[i][j] == self.YOU):
                    house_char = "Y"
                elif (self.board[i][j] == self.CPU):
                    house_char = "C"
                    
                print(f"{house_char}", end=" ")
            print()


# In[4]:


board_sizes_to_check = [(6,7), 
                        (7,8), 
                        (7,10)]
runs = 200


# In[45]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()

print("Depth 1:")
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[5]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,8),silent=True)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()

print("Depth 1:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[79]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,10),silent=True)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()

print("Depth 1:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[7]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    game.set_depth(3)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()

print("Depth 3")    
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")  


# In[8]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,8),silent=True)
    game.set_depth(3)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("Depth 3:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[9]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,10),silent=True)
    game.set_depth(3)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("Depth 3:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[37]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    game.set_depth(5)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("Depth 5:")
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[63]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,8),silent=True)
    game.set_depth(5)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("Depth 5:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[73]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in range(runs):
    game = ConnectSin(board_size=(7,10),silent=True)
    game.set_depth(5)
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("Depth 5:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[10]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    game.set_depth(1)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 1:")
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[11]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    game.set_depth(3)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 3:")
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[13]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    game.set_depth(5)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 5:")
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[64]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(6,7),silent=True)
    game.set_depth(7)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 7:")
print("\tBoard Size 6x7")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[14]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,8),silent=True)
    game.set_depth(1)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 1:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[12]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,8),silent=True)
    game.set_depth(3)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 3:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[38]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,8),silent=True)
    game.set_depth(5)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 5:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[74]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in range(runs):
    game = ConnectSin(board_size=(7,8),silent=True)
    game.set_depth(7)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()

print("With alpha beta pruning, Depth 7:")
print("\tBoard Size 7x8")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[16]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,10),silent=True)
    game.set_depth(1)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 1:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[13]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,10),silent=True)
    game.set_depth(3)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 3:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[ ]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,10),silent=True)
    game.set_depth(5)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 5:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")


# In[ ]:


wins = 0
time_taken = 0
nodes_visited = 0
for i in tqdm(range(runs)):
    game = ConnectSin(board_size=(7,10),silent=True)
    game.set_depth(7)
    game.enable_pruning()
    start_time = time.time()
    if game.run() == 1:
        wins += 1
    time_taken += (time.time() - start_time)
    nodes_visited += game.get_nodes_visited()
    
print("With alpha beta pruning, Depth 7:")
print("\tBoard Size 7x10")
print("\t\tAverage time taken: ", time_taken / runs)
print("\t\tAverage count of visited nodes: ", nodes_visited / runs)
print("\t\tChance of winning: ", wins / runs, "\n")

