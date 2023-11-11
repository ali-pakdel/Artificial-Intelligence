#!/usr/bin/env python
# coding: utf-8

# Ali Pakdel Samadi
# 810198368
# 
# CA1 - Search Algorithms

# In[160]:


import time
import heapq

#State Defines
POINT = 0
RED_LIMITS = 1
REACHED_ALLIES = 2
ALLY_ID = 3
ORC_ID = 4
REACHED_COUNT = 5

moves = [(1, 0), (0, 1), (0, -1), (-1, 0)]

class Gandalf:
    def __init__(self, test_file):
        self.table = []
        self.read_test_file(test_file)
        
        init_reached_allies = ""
        for i in range(0, self.l):
            init_reached_allies += "N "
        init_reached_allies = init_reached_allies[:-1]
        init_ally = -1
        init_orc = -1
        init_red_limits = 10
        reached_count = 0
        
        self.init_state = (self.start_point, init_red_limits, init_reached_allies, init_ally, init_orc, reached_count)
        
        self.front = [self.init_state]
        self.explored = set()
        self.prev_states = {}
        
    def read_test_file(self, test_file):
        with open(test_file) as f:
            self.n, self.m = [int(x) for x in next(f).split()]
            for i in range(0, self.n):
                temp = []
                for j in range(0, self.m):
                    temp.append([(i, j), "W"])
                self.table.append(temp)
            x_start, y_start = [int(x) for x in next(f).split()]
            self.start_point = (x_start, y_start)

            x_end, y_end = [int(x) for x in next(f).split()]
            self.end_point = (x_end, y_end)

            self.k, self.l = [int(x) for x in next(f).split()]

            self.orcs = []
            self.orcs_lvl = []
            for i in range(0, self.k):
                x, y, c = [int(x) for x in next(f).split()]
                self.orcs.append([(x,y),c])
                if self.table[x][y][1] == "W":
                    self.table[x][y][1] = "O" + str(i)
                else:
                    self.table[x][y].append("O" + str(i))
                self.orcs_lvl.append(c)
                self.mark_reds(x, y, c, "O" + str(i))

            self.allies_s = []
            for i in range(0, self.l):
                x, y = [int(x) for x in next(f).split()]
                self.allies_s.append((x, y))
                if self.table[x][y][1] == "W":
                    self.table[x][y][1] = "AS" + str(i)
                else:
                    self.table[x][y].append("AS" + str(i))

            self.allies_e = []
            for i in range(0, self.l):
                x, y = [int(x) for x in next(f).split()]
                self.allies_e.append((x, y))
                if self.table[x][y][1] == "W":
                    self.table[x][y][1] = "AE" + str(i)
                else:
                    self.table[x][y].append("AE" + str(i))

            self.table[self.start_point[0]][self.start_point[1]][1] = "GS"
            self.table[self.end_point[0]][self.end_point[1]][1] = "GE"

            
    def mark_reds(self, x, y, c, label):
        for i in range(1, c + 1):
            if x + i < self.n:
                self.table[x+i][y][1] = label
            if x - i >= 0:
                self.table[x-i][y][1] = label
            if y + i < self.m:
                self.table[x][y+i][1] = label
            if y - i >= 0:
                self.table[x][y-i][1] = label

            if x - i + 1 >= 0 and y - i + 1 >= 0:
                self.table[x-i+1][y-i+1][1] = label
            if x - i + 1 >= 0 and y + i - 1 < self.m:
                self.table[x-i+1][y+i-1][1] = label
            if x + i - 1 < self.n and y - i + 1 >= 0:
                self.table[x+i-1][y-i+1][1] = label
            if x + i - 1 < self.n and y + i - 1 < self.m:
                self.table[x+i-1][y+i-1][1] = label

                
    def is_move_legal(self, curr_point, move):
        if curr_point[0] + move[0] < self.n and curr_point[0] + move[0] >= 0:
            if curr_point[1] + move[1] < self.m and curr_point[1] + move[1] >= 0:
                return True
        return False



    def make_new_state(self, curr_state, new_point):
        state_list = list(curr_state)
        if self.table[new_point[0]][new_point[1]][1] == "W" or self.table[new_point[0]][new_point[1]][1] == "GS" or self.table[new_point[0]][new_point[1]][1] == "GE":
            state_list[RED_LIMITS] = 10
            state_list[ORC_ID] = -1

        elif self.table[new_point[0]][new_point[1]][1][:-1] == "O":
            if int(self.table[new_point[0]][new_point[1]][1][1]) == state_list[ORC_ID]:
                state_list[RED_LIMITS] -= 1
            else:
                orc_id = int(self.table[new_point[0]][new_point[1]][1][1])
                state_list[RED_LIMITS] = self.orcs_lvl[orc_id]
                state_list[ORC_ID] = int(self.table[new_point[0]][new_point[1]][1][1])

        elif self.table[new_point[0]][new_point[1]][1][:-1] == "AE":
            state_list[RED_LIMITS] = 10
            state_list[ORC_ID] = -1
            if state_list[ALLY_ID] == int(self.table[new_point[0]][new_point[1]][1][2]):
                temp = list(state_list[REACHED_ALLIES])
                temp[state_list[ALLY_ID] * 2] = 'Y'
                state_list[REACHED_COUNT] += 1
                state_list[REACHED_ALLIES] = "".join(temp)
                state_list[ALLY_ID] = -1

        elif len(self.table[new_point[0]][new_point[1]]) == 3 and self.table[new_point[0]][new_point[1]][2][:-1] == "AE":
            state_list[RED_LIMITS] = 10
            state_list[ORC_ID] = -1
            if state_list[ALLY_ID] == int(self.table[new_point[0]][new_point[1]][2][2]):
                temp = list(state_list[REACHED_ALLIES])
                temp[state_list[ALLY_ID] * 2] = 'Y'
                state_list[REACHED_COUNT] += 1
                state_list[REACHED_ALLIES] = "".join(temp)
                state_list[ALLY_ID] = -1

        if self.table[new_point[0]][new_point[1]][1][:-1] == "AS" and state_list[ALLY_ID] == -1:
            state_list[RED_LIMITS] = 10
            state_list[ORC_ID] = -1
            if state_list[REACHED_ALLIES][int(self.table[new_point[0]][new_point[1]][1][2]) * 2] == "N":
                state_list[ALLY_ID] = int(self.table[new_point[0]][new_point[1]][1][2])

        state_list[POINT] = new_point
        return tuple(state_list)
       

    def is_it_end(self, state):
        if state[POINT] == self.end_point and state[REACHED_COUNT] == self.l:
            return True
        return False

    def which_direction(self, delta_x, delta_y):
        if delta_x == 1:
            return "U"
        elif delta_x == -1:
            return "D"          
        elif delta_y == 1:
            return "L"
        elif delta_y == -1:
            return "R"
    
    def print_moves(self, state):
        path_directions = ""
        curr_state = state
        while True:
            if curr_state == self.init_state:
                break
            next_state = self.prev_states[curr_state]
            
            delta_x = next_state[POINT][0] - curr_state[POINT][0] 
            delta_y = next_state[POINT][1] - curr_state[POINT][1]

            path_directions += self.which_direction(delta_x, delta_y)    
            curr_state = next_state

        print("\tPath directions:", path_directions[::-1])
        print("\tPath lenght:", len(path_directions))
        print("\tStates explored:", len(self.prev_states)) 


    def BFS(self):
        front_set = set()
        front_set.add(self.front[0])
        while len(self.front) > 0:
            
            curr_state = self.front.pop(0)
            self.explored.add(curr_state)
            
            for i in range(0, 4):
                if self.is_move_legal(curr_state[POINT], moves[i]) == True:
                    
                    new_point = (curr_state[POINT][0] + moves[i][0], curr_state[POINT][1] + moves[i][1])
                    new_state = self.make_new_state(curr_state, new_point)
                    
                    if new_state[RED_LIMITS] == 0:
                        continue
                    
                    if new_state not in front_set and new_state not in self.explored:
                        self.prev_states[new_state] = curr_state
                        self.front.append(new_state)
                        front_set.add(new_state)
                        
                        if self.is_it_end(new_state):
                            return new_state
                        

                        
    def IDS(self):
        depth = 0
        while True:
            
            self.front = [self.init_state]
            self.explored.clear()
            self.explored.add(self.init_state)
            self.prev_states.clear()
            depth_limits = {}
            depth_limits[self.init_state] = 1
            
            while len(self.front) > 0:
                curr_state = self.front.pop()
                if depth_limits[curr_state] < depth:
                    for i in range(0, 4):
                        if self.is_move_legal(curr_state[POINT], moves[i]) == True:
                            
                            new_point = (curr_state[POINT][0] + moves[i][0], curr_state[POINT][1] + moves[i][1])
                            new_state = self.make_new_state(curr_state, new_point)
                            
                            if new_state[RED_LIMITS] == 0:
                                continue
                            
                            if new_state not in self.explored or depth_limits[new_state] > depth_limits[curr_state] + 1:
                                self.prev_states[new_state] = curr_state
                                self.explored.add(new_state)
                                depth_limits[new_state] = depth_limits[curr_state] + 1
                                self.front.append(new_state)
                                
                                if self.is_it_end(new_state):
                                    return new_state
            depth += 1
                                

  

    def heuristic_func(self, curr_state):
        if curr_state[REACHED_COUNT] == self.l:
            delta_x = abs(curr_state[POINT][0] - self.end_point[0])
            delta_y = abs(curr_state[POINT][1] - self.end_point[1])
            
            return delta_x + delta_y
        
        elif curr_state[ALLY_ID] == -1:
            max_dis = 0
            for i in range(0, self.l//2 + 1):
                if curr_state[REACHED_ALLIES][i * 2] == 'N':
                    
                    delta_x1 = abs(curr_state[POINT][0] - self.allies_s[i][0])
                    delta_y1 = abs(curr_state[POINT][1] - self.allies_s[i][1])

                    delta_x2 = abs(self.allies_s[i][0] - self.allies_e[i][0])
                    delta_y2 = abs(self.allies_s[i][1] - self.allies_e[i][1])

                    delta_x3 = abs(self.allies_e[i][0] - self.end_point[0])
                    delta_y3 = abs(self.allies_e[i][1] - self.end_point[1])

                    dis = delta_x1 + delta_y1 + delta_x2 + delta_y2 + delta_x3 + delta_y3

                    if dis > max_dis:
                        max_dis = dis
                        
            return max_dis
        
        elif curr_state[ALLY_ID] != -1:
            delta_x1 = abs(curr_state[POINT][0] - self.allies_e[curr_state[ALLY_ID]][0])
            delta_y1 = abs(curr_state[POINT][1] - self.allies_e[curr_state[ALLY_ID]][1])

            delta_x2 = abs(self.allies_e[curr_state[ALLY_ID]][0] - self.end_point[0])
            delta_y2 = abs(self.allies_e[curr_state[ALLY_ID]][1] - self.end_point[1])

            return delta_x1 + delta_y1 + delta_x2 + delta_y2


    def A_star(self, alpha):
        self.explored.add(self.init_state)
        dist_went = {}
        dist_went[self.init_state] = 0
        new_front = [(self.heuristic_func(self.init_state), self.init_state)]
        
        while len(new_front) > 0:
            
            curr_state = heapq.heappop(new_front)[1]
            self.explored.add(curr_state)
            
            for i in range(0, 4):
                if self.is_move_legal(curr_state[POINT], moves[i]) == True:
                    new_point = (curr_state[POINT][0] + moves[i][0], curr_state[POINT][1] + moves[i][1])  
                    new_state = self.make_new_state(curr_state, new_point)

                    if new_state[RED_LIMITS] == 0:
                        continue
                    
                    if new_state not in dist_went or dist_went[new_state] > dist_went[curr_state] + 1:
                        self.prev_states[new_state] = curr_state
                        self.explored.add(new_state)
                        dist_went[new_state] = dist_went[curr_state] + 1
                        heuris_new = alpha * self.heuristic_func(new_state) + dist_went[new_state]
                        heapq.heappush(new_front, (heuris_new, new_state))
                        
                        if self.is_it_end(new_state):
                            return new_state
                        


def avg(times):
    return(times[0] + times[1] + times[2]) / 3

def run_algorithms():
    test = "test_0"
    titles = ["BFS tests \n", "IDS tests \n", "A* tests \n", "Weighted A* tests with alpha = 2 \n", "Weighted A* tests with alpha = 7 \n"]

    for k in range(0, 5):
        print(titles[k])
        for i in range (0, 4):
            times = []
            print("\t"+test + str(i) + ".txt")
            for j in range(3):
                G = Gandalf(test + str(i) + ".txt")

                stime = time.time()
                
                if k == 0:
                    end = G.BFS()
                elif k == 1:
                    end = G.IDS()
                elif k == 2:
                    end = G.A_star(1)
                elif k == 3:
                    end = G.A_star(2)
                elif k == 4:
                    end = G.A_star(7)
                    
                times.append(1000 *(time.time() - stime))

            print("\tTime:", avg(times), "ms")
            G.print_moves(end)
            print("\n")


            
run_algorithms()

