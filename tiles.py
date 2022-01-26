import random
import copy

# ------ Node Class ------


class Node:
    def __init__(self, board_state, parent=None):
        self.parent = parent
        self.move_tile = [None] * 4
        self.board_state = board_state

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
            self.board = self.build_initial_board()

    def build_initial_board(self):
        board = [[4,5,0],[6,1,8],[7,3,2]]
        self.blank = [0,2]
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
#            board.append(row)
        print(board)
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

    def print_board(self):
        for i in range(self.size):
            print(self.board[i])
# ------ End Board Class ------

# Count number of displaced tiles


def h1_score(board):
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if (board[x][y] == GOAL_BOARD.board[x][y]):
                score += 1
    return score


def h2_score(board):
    score = 0
    for goal_y in range(BOARD_SIZE):
        for goal_x in range(BOARD_SIZE):
            found = False
#            print(GOAL_BOARD.board[goal_x][goal_y])
#            print(board)
            while (found == False):
                for board_y in range(BOARD_SIZE):
                    for board_x in range(BOARD_SIZE):
                        #print(board[board_x][board_y])
                        if (board[board_x][board_y] == GOAL_BOARD.board[goal_x][goal_y]):                            
                            man_distance = abs(board_x - goal_x) + abs(board_y - goal_y)
                            score += man_distance
                            found = True
                            break
                    if (found == True):
                        break
#    print(score)
    return score


def update_search_tree(new_frontier, current_state, visited):
    for tile in range(4):
        new_board_state = copy.deepcopy(current_state.board_state)
        blank_x = new_board_state.blank[X]
        blank_y = new_board_state.blank[Y]
        new_blank_position_x = blank_x + (MOVE[tile])[X]
        new_blank_position_y = blank_y + (MOVE[tile])[Y]
#        print("[", new_blank_position_x, ",", new_blank_position_y,"]")
        if (new_blank_position_x >= 0 and new_blank_position_x < BOARD_SIZE):
            if (new_blank_position_y >= 0 and new_blank_position_y < BOARD_SIZE):
                #                print(new_board_state.blank, " ", new_board_state.board[blank_x][blank_y])
                new_board_state.board[blank_x][blank_y] = new_board_state.board[new_blank_position_x][new_blank_position_y]
                new_board_state.board[new_blank_position_x][new_blank_position_y] = BLANK
                new_board_state.blank = [new_blank_position_x,new_blank_position_y]
                new_node = Node(new_board_state, current_state)
                current_state.add_node(new_node, tile)
                # Check if node has already been added
                do_not_add = False
                for visited_node in visited:    
                    if (visited_node == new_node.board_state.board):
                        do_not_add = True
                        break
                if (do_not_add == False):
                    new_frontier.append(new_node)
#                    new_node.board_state.print_board()
#                    print()
                    visited.append(new_node.board_state.board)
    return new_frontier

def update_state(frontier, h_func):
    state_scores = []
    top_score = 9999
    score_locations = []
#    print("frontier(update_state): ", frontier)
    for frontier_state in frontier:
#        frontier_state.board_state.print_board()
        state_scores.append(h_func(frontier_state.board_state.board))
#            frontier_state.board_state.print_board()
#            print()
#    print(state_scores)
    for index in range(len(state_scores)):
        if (state_scores[index] == top_score):
            score_locations.append(index)
        elif (state_scores[index] < top_score):
            top_score = state_scores[index]
            score_locations = [index]
    print("Top Score: ", top_score)
    if (len(score_locations) > 1):
        new_state_index = random.randrange(len(score_locations))
        temp = frontier[new_state_index]
        return temp, new_state_index
    else:
        temp = frontier[score_locations[0]]
        return temp, score_locations[0]

# ------- MAIN --------
BOARD_SIZE = 3
X = 0
Y = 1
BLANK = 0

LEFT_TILE = 0
UP_TILE = 1
DOWN_TILE = 2
RIGHT_TILE = 3

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
scores = []
visited = [current_node.board_state.board]
moves = 0
while (current_node.board_state.board != GOAL_BOARD.board and moves < 100000):
    moves += 1
#    print("MOVE ", moves)
    frontier = update_search_tree(frontier, current_node, visited)
    current_node, location = update_state(frontier, h2_score)
#    print("frontier: ", frontier)
#    print("location: ", location)
#    visited.append(current_node.board_state.board)
    del frontier[location]
    print()
    current_node.board_state.print_board()
#current_state = update_state(frontier, current_state, h2_score)

# current_state.board_state.print_board()

#print(h1_score(board_state.board, goal_board.board))
#print(h2_score(board_state.board, goal_board.board))
