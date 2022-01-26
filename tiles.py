import random
import copy
import winsound
import time

# ------ Node Class ------
class Node:
    def __init__(self, board_state, parent=None):
        self.parent = parent
        self.move_tile = [None] * 4
        self.board_state = board_state
        if (self.parent != None):
            self.steps = self.parent.steps + 1
        else:
            self.steps = 0

    def add_node(self, new_node, tile):
        self.move_tile[tile] = new_node

    def go(self, tile):
        return self.move_tile[tile]
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

#        board = [[4,5,6],[3,7,8],[2,1,0]]
#        self.blank = [2,2]

#        board = [[8,7,6],[5,4,3],[2,1,0]]
#        self.blank = [2,2]

#        board = [[4,3,2],[6,1,5],[0,7,8]]
#        self.blank = [2,0]

#        board = [[0,1,2],[3,6,4],[7,8,5]]
#        self.blank = [0,0]

#        board = [[3,1,2],[6,0,4],[7,8,5]]
#        self.blank = [1,1]

#        board = [[1,0,2],[6,4,3],[7,8,5]]
#        self.blank = [0,1]

#        board = [[3,4,5],[2,0,8],[1,6,7]]
#        self.blank = [1,1]

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

def update_search_tree(frontier, current_state, visited, h, g):
    nodes_added = 0
    for tile in range(4):
        new_board_state = copy.deepcopy(current_state.board_state)
        blank_x = new_board_state.blank[X]
        blank_y = new_board_state.blank[Y]
        new_blank_position_x = blank_x + (MOVE[tile])[X]
        new_blank_position_y = blank_y + (MOVE[tile])[Y]
        if (new_blank_position_x >= 0 and new_blank_position_x < BOARD_SIZE):
            if (new_blank_position_y >= 0 and new_blank_position_y < BOARD_SIZE):
                new_board_state.board[blank_x][blank_y] = new_board_state.board[new_blank_position_x][new_blank_position_y]
                new_board_state.board[new_blank_position_x][new_blank_position_y] = BLANK
                new_board_state.blank = [new_blank_position_x,new_blank_position_y]
                # Check if node has already been added
                do_not_add = False
                for visited_node in visited:    
                    if (visited_node.board_state.board == new_board_state.board):
                        do_not_add = True
                        break
                if (do_not_add == False):
                    new_node = Node(new_board_state, current_state)
                    score = h[SCORE_FUNCTION](new_node.board_state.board)
                    if (g == A_STAR):
                        score += new_node.steps
                    h[SCORE_LIST].append(score)
  
                    frontier.append(new_node)
                    current_state.add_node(new_node, tile)
                    nodes_added += 1
    return nodes_added

def update_state(frontier, score_list):
    top_score_locations = []
    new_state = None
    top_score = score_list[0]
    top_score_locations.append(0)

    for index in range(len(score_list)):
        if (score_list[index] == top_score):
            top_score_locations.append(index)
        elif (score_list[index] < top_score):
            top_score = score_list[index]
            top_score_locations = [index]

    new_state_index = 0
    if (len(top_score_locations) > 1):
        new_state_index = random.randrange(len(top_score_locations)-1)
    new_state = frontier[new_state_index]
    del frontier[new_state_index]
    del score_list[new_state_index]
    return new_state, top_score

def run_test(frontier, current_node, visited, moves, heuristic, algorithm):
    solution_path = None
    total_nodes = 0
    while (current_node.board_state.board != GOAL_BOARD.board and moves < MAX_MOVES):      
        failed = True
        moves += 1
        if (moves % REPORT_FREQUENCY == 0):
            print("Visited Nodes: ", moves, "  Node Depth: ", current_node.steps, "  Frontier Nodes: ", len(frontier), "  Total Nodes: ", total_nodes, "  Top Score: ", top_score)
        total_nodes += update_search_tree(frontier, current_node, visited, heuristic, algorithm)
        current_node, top_score = update_state(frontier, heuristic[SCORE_LIST])
        visited.append(current_node)
    if (moves < MAX_MOVES):
        solution_path = path(current_node)
#        for board in solution_path:
#            print(board.board, end='-->')   
#        print()
        print("SOLUTION FOUND! Visited Nodes: ", moves, "  Steps: ", current_node.steps, "  Frontier Nodes: ", len(frontier), "  Total Nodes: ", total_nodes)
        print()
        failed = False
    return solution_path, failed

# ------- MAIN --------
BOARD_SIZE = 3
MAX_MOVES = 50000
REPORT_FREQUENCY = 10000
X = 0
Y = 1
BLANK = 0

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
success = False
total_steps = [ [0]*BOARD_SIZE for i in range(BOARD_SIZE)]
while (success == False):
    state_tree = Node(Board(BOARD_SIZE))
    state_tree.board_state.print_board()
    paths_table = []
    failed = False
    for heuristic in range(H1, H3+1):
        paths = []
        for algorithm in range(GBFS, A_STAR+1):
            scores = []
            h_choice = {
                H1 : [h1_score, scores],
                H2 : [h2_score, scores],
                H3 : [h3_score, scores] 
            }
            moves = 0
            current_node = copy.deepcopy(state_tree)
            visited = [current_node]
            frontier = []
            total_nodes = 1
            print("Heuristic: ", h_name[heuristic], "  Algorithm: ", algorithm_name[algorithm])
            solution_path, failed = run_test(frontier, current_node, visited, moves, h_choice[heuristic], algorithm)
            if (failed == True):
                break
            paths.append(solution_path)
            solution_path = None
        if (failed == True):
            break
        paths_table.append(paths)
    if (failed == False):
        success = True
        print()
        for heuristic in range(H1, H3+1):
            for algorithm in range(GBFS, A_STAR+1):
                solution_path = paths_table[heuristic][algorithm]
                total_steps[heuristic][algorithm] += solution_path[len(solution_path)-1].steps
                print("Heuristic: ", h_name[heuristic], "  Algorithm: ", algorithm_name[algorithm], "  Steps: ", solution_path[len(solution_path)-1].steps)
                for node in solution_path:
                    print(node.board_state.board, end='-->')
                print()
                print()
    else:
        print("Failed to find a solution...")   
        print()             

while (True):
    play_sound(1000, 600)
    time.sleep(1)