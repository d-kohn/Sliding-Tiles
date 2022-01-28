import random
import copy
import winsound
import time

# ------ Node Class ------
class Node:
    def __init__(self, board_state, parent=None):
        self.board_state = board_state
        self.steps = 0
# ------ End Node Class ------

# ------ Board Class ------
class Board:
    def __init__(self, size, board_type="RANDOM"):
        self.size = size
        self.blank = []
        if (board_type == "GOAL"):
            self.board = self.build_goal()
        else:
            parity = False
            while (parity == False):
                self.board = self.build_initial_board()
                parity = self.check_parity()

    def build_initial_board(self):
#        Test boards:

#        '''
        board = [[0]*BOARD_SIZE for i in range(BOARD_SIZE)]
        tiles = [False] * (self.size*self.size)

        for y in range(self.size):
            row = []
            for x in range(self.size):
                added = False
                while (added == False):
                    tile = random.randrange(self.size*self.size)
                    if (tiles[tile] == False):
                        tiles[tile] = True
                        row.append(tile)
                        board[x][y] = tile
                        added = True
                        if (tile == 0):
                            self.blank = [x, y]
#       '''
        return board

    def build_goal(self):
        board = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(y*self.size + x)
            board.append(row)
        return board

    def check_parity(self):
        correct_order = [i for i in range(1, self.size*self.size)]
        board_order = []
        displacement_count = 0
        for y in range(self.size):
            for x in range(self.size):
                board_order.append(self.board[y][x])
        board_order = list(filter((0).__ne__, board_order))
        for index in range(len(correct_order)):
            for displaced in range(len(correct_order)):
                if (board_order[displaced] > correct_order[index]):
                    displacement_count += 1
                if (board_order[displaced] == correct_order[index]):
                    break
        if (displacement_count % 2 == 0):
            return True
        else:
            return False

    def print_board(self):
        for i in range(self.size):
            print(self.board[i])
# ------ End Board Class ------

def play_sound(duration, frequency):
    winsound.Beep(frequency, duration)

def to_tuple(board):
    board_key = ()
    for row in range(BOARD_SIZE):
        board_key = board_key + tuple(board[row])
#    print(board_key)
    return(board_key)        

# Count number of displaced tiles
def h1_score(board):
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if (board[x][y] != GOAL_BOARD.board[x][y] and board[x][y] != 0):
                score += 1
    return score

def h2_score(board):  
    score = 0
    for goal_y in range(BOARD_SIZE):
        for goal_x in range(BOARD_SIZE):
            found = False
            while (found == False):
                for board_y in range(BOARD_SIZE):
                    for board_x in range(BOARD_SIZE):
                        if (board[board_x][board_y] == GOAL_BOARD.board[goal_x][goal_y]):                          
                            man_distance = abs(board_x - goal_x) + abs(board_y - goal_y)
                            score += man_distance
                            found = True
                            break
                    if (found == True):
                        break
    return score

def h3_score(board):
    return h1_score(board) + h2_score(board)

def path(final_node):
    solution_path = [final_node]
    current_node = final_node
    while(current_node.parent != None):
        current_node = current_node.parent
        solution_path.insert(0, current_node)
    return solution_path

def update_search_tree(frontier, current_node, visited, h, g):
    nodes_added = 0
    for tile in range(4):
        new_board_state = copy.deepcopy(current_node.board_state)
        blank_x = new_board_state.blank[X]
        blank_y = new_board_state.blank[Y]
        new_blank_position_x = blank_x + (MOVE[tile])[X]
        new_blank_position_y = blank_y + (MOVE[tile])[Y]
        if (new_blank_position_x >= 0 and new_blank_position_x < BOARD_SIZE):
            if (new_blank_position_y >= 0 and new_blank_position_y < BOARD_SIZE):
                new_board_state.board[blank_x][blank_y] = new_board_state.board[new_blank_position_x][new_blank_position_y]
                new_board_state.board[new_blank_position_x][new_blank_position_y] = BLANK
                new_board_state.blank = [new_blank_position_x,new_blank_position_y]
                if (visited.get(to_tuple(new_board_state.board)) == None):
                    new_node = Node(new_board_state)
                    new_node.steps = current_node.steps + 1
                    score = h(new_node.board_state.board)
                    if (g == A_STAR):
                        score += new_node.steps
                    frontier[score].append(new_node)
                    nodes_added += 1
    return nodes_added

def update_state(frontier):
    new_state_node = None
    top_score = 0
    index = 0
    for score in range(FRONTIER_MAX_SCORE):
        length = len(frontier[score])
        if (length > 0):
            top_score = score
            if (length > 1):
                index = random.randrange(length-1)
            new_state_node = copy.deepcopy(frontier[top_score][index])
            del frontier[top_score][index]
            break
    return new_state_node, top_score

def run_test(frontier, curr_node, visited, moves, heuristic, algorithm):
    total_nodes = 0
    while (curr_node.board_state.board != GOAL_BOARD.board and moves < MAX_MOVES):      
        failed = True
        moves += 1
        if (moves % REPORT_FREQUENCY == 0):            
            print("Visited Nodes: ", moves, "  Node Depth: ", curr_node.steps, "  Total Nodes: ", total_nodes, "  Top Score: ", top_score, "  Frontier: ", end='')
            for index in range(len(frontier)-1):
                frontier_size = len(frontier[index])
                if (frontier_size > 0):
                    print(f"{index}: {frontier_size} ", end='')
            print()
        total_nodes += update_search_tree(frontier, curr_node, visited, heuristic, algorithm)
        del curr_node.board_state
        del curr_node
        curr_node, top_score = update_state(frontier)
        current_node_key = to_tuple(curr_node.board_state.board)
        visited[current_node_key] = True
    if (moves < MAX_MOVES):
        print("SOLUTION FOUND! Visited Nodes: ", moves, "  Steps: ", curr_node.steps, "  Total Nodes: ", total_nodes, "  Frontier: ", end='')
        for index in range(len(frontier)-1):
            frontier_size = len(frontier[index])
            if (frontier_size > 0):
                print(f"{index}: {frontier_size} ", end='')
        print()
        print()
        failed = False
    return curr_node, failed

# ------- MAIN --------
BOARD_SIZE = 5
MAX_MOVES = 25000000
REPORT_FREQUENCY = 50000
X = 0
Y = 1
BLANK = 0
FRONTIER_MAX_SCORE = 1000

LEFT_TILE = 0
UP_TILE = 1
DOWN_TILE = 2
RIGHT_TILE = 3

GBFS = 0
A_STAR = 1
H1 = 0
H2 = 1
H3 = 2

h_name = {
    H1 : "H1",
    H2 : "H2",
    H3 : "H3"
}

algorithm_name = {
    GBFS : "GBFS",
    A_STAR : "A*"
}

SCORE_FUNCTION = 0
SCORE_LIST = 1

MOVE = {
    LEFT_TILE: [-1, 0],
    UP_TILE: [0, -1],
    DOWN_TILE: [0, 1],
    RIGHT_TILE: [1, 0]
}

GOAL_BOARD = Board(BOARD_SIZE, "GOAL")
successes = 0
visited = {}
total_steps = [ [0]*BOARD_SIZE for i in range(BOARD_SIZE)]
h_choice = {
    H1 : h1_score,
    H2 : h2_score,
    H3 : h3_score
}
while (successes < 1):
    state_tree = Node(Board(BOARD_SIZE))
    state_tree.board_state.print_board()
    failed = False  
    for heuristic in range(H1, H3+1):
        for algorithm in range(GBFS, A_STAR):
#            print(state_tree)
            visited = {}
            moves = 0
            first_node = copy.deepcopy(state_tree)
            first_node.board_state = copy.deepcopy(state_tree.board_state)
#            print(current_node)
            current_node_key = to_tuple(first_node.board_state.board)
            visited[current_node_key] = True
            frontier = [ [] for i in range(FRONTIER_MAX_SCORE) ]
            total_nodes = 1
            print("Heuristic: ", h_name[heuristic], "  Algorithm: ", algorithm_name[algorithm])
            first_node, failed = run_test(frontier, first_node, visited, moves, h_choice[heuristic], algorithm)
            if (failed == True):
                break
        if (failed == True):
            break
    
    if (failed == False):
        successes += 1
        print()
        with open("data.txt", "a") as out:
            out.write(str(state_tree.board_state.board) + "\n")
            for heuristic in range(H1, H3+1):
                for algorithm in range(GBFS, A_STAR):
                    print("Heuristic: ", h_name[heuristic], "  Algorithm: ", algorithm_name[algorithm], "  Steps: ", first_node.steps)
                    line = "Heuristic: " + str(h_name[heuristic]) + "  Algorithm: " + str(algorithm_name[algorithm]) + "  Steps: " + str(first_node.steps) + "\n"
                    out.write(line)
                    out.write("\n\n")
            out.write("\n\n")
            out.close()        
    else:
        print("Failed to find a solution...")   
        print()             

while (True):
    play_sound(1000, 600)
    time.sleep(1)