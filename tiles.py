import random
import copy

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
        board = [[4,5,6],[3,7,8],[2,1,0]]
        self.blank = [2,2]

#        board = [[4,3,2],[6,1,5],[0,7,8]]
#        self.blank = [2,0]
        '''
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
#        print(board)
        '''
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
            if (board_order[index] != correct_order[index]):
                for displaced in range(len(correct_order)):
                    if (board_order[displaced] > correct_order[index]):
                        displacement_count += 1
                    if (board_order[displaced] == correct_order[index]):
                        break
        self.print_board()
#        print(correct_order)
        print(board_order)
        print(displacement_count)
        if (displacement_count % 2 == 0):
            return True
        else:
            return False

    def print_board(self):
        for i in range(self.size):
            print(self.board[i])
# ------ End Board Class ------

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
                        if (board[board_x][board_y] == GOAL_BOARD.board[goal_x][goal_y]): # and board[board_x][board_y] != 0):                            
                            man_distance = abs(board_x - goal_x) + abs(board_y - goal_y)
                            score += man_distance
                            found = True
                            break
                    if (found == True):
                        break
    return score

def path(final_node):
    solution_path = [final_node.board_state]
    parent_node = final_node
    while(parent_node.parent != None):
        solution_path.insert(0, parent_node.board_state)
        parent_node = parent_node.parent
    return solution_path

def update_search_tree(frontier, current_state, visited, h1_scores, h2_scores, h):
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
                new_node = Node(new_board_state, current_state)
                # Check if node has already been added
                do_not_add = False
                for visited_node in visited:    
                    if (visited_node == new_node.board_state.board):
                        do_not_add = True
                        break
                if (do_not_add == False):
                    if (h == H1):
                        h1_scores.append(h1_score(new_node.board_state.board))
                    elif (h == H2):
                        h2_scores.append(h2_score(new_node.board_state.board) + new_node.steps)
#                        print(h2_scores)
                    frontier.append(new_node)
                    current_state.add_node(new_node, tile)
                    visited.append(new_node.board_state.board)

def update_state(frontier, h):
    state_scores = []
    score_locations = []
    new_state = None
#    for frontier_state in frontier:
#        state_scores.append(h_func(frontier_state.board_state.board))
    if (h == H1):
        state_scores = h1_scores
    elif (h == H2):
        state_scores = h2_scores

    top_score = state_scores[0]
    score_locations.append(0)
    for index in range(len(state_scores)-1,-1,-1):
        if (state_scores[index] == top_score):
            score_locations.append(index)
        elif (state_scores[index] < top_score):
            top_score = state_scores[index]
            score_locations = [index]
#    print("Top Score: ", top_score)
    if (len(score_locations) > 1):
        new_state_index = random.randrange(len(score_locations))
        new_state = frontier[new_state_index]
        del frontier[new_state_index]
        if (h == H1):
            del h1_scores[new_state_index]
        if (h == H2):
            del h2_scores[new_state_index]
    else:
        new_state = frontier[score_locations[0]]
        del frontier[score_locations[0]]
        if (h == H1):
            del h1_scores[score_locations[0]]
        if (h == H2):
            del h2_scores[score_locations[0]]
    return new_state

# ------- MAIN --------
BOARD_SIZE = 3
MAX_MOVES = 100000
X = 0
Y = 1
BLANK = 0

LEFT_TILE = 0
UP_TILE = 1
DOWN_TILE = 2
RIGHT_TILE = 3

H1 = 0
H2 = 1
H3 = 2

MOVE = {
    LEFT_TILE: [-1, 0],
    UP_TILE: [0, -1],
    DOWN_TILE: [0, 1],
    RIGHT_TILE: [1, 0]
}

GOAL_BOARD = Board(BOARD_SIZE, "GOAL")
state_tree = Node(Board(BOARD_SIZE))
current_node= state_tree

frontier = []
h1_scores = []
h2_scores = []
node_depths = []

visited = [current_node.board_state.board]
moves = 0
while (current_node.board_state.board != GOAL_BOARD.board and moves < MAX_MOVES):
    heuristic = H2
    moves += 1
    if (moves % 500 == 0):
        print("Moves: ", moves, "  Node Depth: ", current_node.steps, "  Frontier Nodes: ", len(frontier))
    update_search_tree(frontier, current_node, visited, h1_scores, h2_scores, heuristic)
    current_node = update_state(frontier, heuristic)
#    current_node.board_state.print_board()
#    GOAL_BOARD.print_board()

if (moves < MAX_MOVES):
    solution_path = path(current_node)
    for board in solution_path:
        print(board.board, end='-->')   
    print()
    print()
    print("Steps: ", current_node.steps)
#current_node.board_state.print_board()
