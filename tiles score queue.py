import random
import copy
#import winsound

# ------ Node Class ------
class Node:
    def __init__(self, board_state, parent=None):
        ''' Build Node object
        Args:
            self: the Node object
            board_state: Board object to store in the Node
            parent: pointer to parent Node - default: None
        Returns:
            Nothing
        '''  
        self.parent = parent                        # Parent Node
        self.move_tile = [None] * 4                 # Pointers to the Left/Up/Down/Right Nodes from this Node
        self.board_state = board_state              # Board object
        self.steps = 0                              # Number of steps to the root Node
        if (self.parent != None):                   
            self.steps = self.parent.steps + 1

    def add_node(self, new_node, tile):
        ''' Adds a node to the 
        Args:
            self: the Board object
            size: size of the board  size X size
            board_type: RANDOM or GOAL - default: RANDOM
        Returns:
            Nothing
        '''  
        self.move_tile[tile] = new_node
# ------ End Node Class ------

# ------ Board Class ------
class Board:
    def __init__(self, size, board_type="RANDOM"):
        ''' Build Board object
        Args:
            self: the Board object
            size: size of the board  size X size
            board_type: RANDOM or GOAL - default: RANDOM
        Returns:
            Nothing
        '''  
        self.size = size                        # Length the side of the puzzle
        self.blank = []                         # coordinates of the blank space (y, x)
        if (board_type == "GOAL"):
            self.board = self.build_goal()
        else:
            parity = False
            while (parity == False):
                self.board = self.build_initial_board()
                parity = self.check_parity()

    def build_initial_board(self):
        ''' Build goal state puzzle
        Args:
            self: the Board object
        Returns:
            2-D List: random puzzle board
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
#       '''
        return board

    def build_goal(self):
        ''' Build goal state puzzle
        Args:
            self: the Board object
        Returns:
            2-D List: puzzle board goal state
        '''  
        board = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(y*self.size + x)
            board.append(row)
        return board

    def check_parity(self):
        ''' Checks if the board is in the domain of the goal state
        Args:
            self: the Board object
        Returns:
            bool: True - is in the domain of the goal state / False - is not
        '''  
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
        ''' Activates our AI overlords..or just prints a formated puzzle
        Args:
            self: the Board object
        Returns:
            Nothing
        '''  
        for i in range(self.size):
            print(self.board[i])
# ------ End Board Class ------

def to_tuple(board):
    board_key = ()
    for row in range(BOARD_SIZE):
        board_key = board_key + tuple(board[row])
    return(board_key)        

def h1_score(board):
    ''' Score board using h1 heuristic
    Args:
        board: 2-D array puzzle board to be scored
    Returns:
        int: the board's heuristic score
    '''  
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if (board[x][y] != GOAL_BOARD.board[x][y] and board[x][y] != 0):
                score += 1
    return score

def h2_score(board):
    ''' Score board using h2 heuristic
    Args:
        board: 2-D array puzzle board to be scored
    Returns:
        int: the board's heuristic score
    '''  
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
    ''' Score board using h3 heuristic
    Args:
        board: 2-D array puzzle board to be scored
    Returns:
        int: the board's heuristic score
    '''  
    return h1_score(board) + h2_score(board)

def path(final_node):
    ''' Start from the final node and record path through parents to the start state
    Args:
        final_node: current node equal to the goal state
    Returns:
        List: list of nodes making a path from the final node to the start state
    '''  
    solution_path = [final_node]
    current_node = final_node
    while(current_node.parent != None):
        current_node = current_node.parent
        solution_path.insert(0, current_node)
    return solution_path

def update_search_tree(frontier, current_state_node, visited, h, g):
    ''' Take the new current Node and create its children states, verify 
        they haven't been visited score them based on the heuristic and
        algorithm, then append them to the frontier priority queue
    Args:
        frontier: 2-dimenstional List priority queue of leaf puzzle states
        current_state_node: current puzzle state node
        visited: map of previously visited puzzle states
        h: heuristic scoring function
        g: algorithm being used (GBFS or A_STAR)
    Returns:
        int: nodes added to the state tree
    '''
    nodes_added = 0
    # Child nodes generated are kept from previous heuristic/node tests
    for tile in range(4):
        # Check if the current node already has a child node, check if it's been visited, if not, score it, add
        # it to the frontier
        if (current_state_node.move_tile[tile] != None):
            old_node = current_state_node.move_tile[tile]
            if (visited.get(to_tuple(old_node.board_state.board)) == None):
                score = h(old_node.board_state.board)
                if (g == A_STAR):
                    score += old_node.steps
                frontier[score].append(old_node)
                nodes_added += 1
        # If there is not a child node already, build the puzzle, check if it was visited, create a new node, add
        # it to the parent Node as a child, score it, and add it to the frontier
        else:
            #Build the new puzzle board
            new_board_state = copy.deepcopy(current_state_node.board_state)
            blank_x = new_board_state.blank[X]
            blank_y = new_board_state.blank[Y]
            new_blank_position_x = blank_x + (MOVE[tile])[X]
            new_blank_position_y = blank_y + (MOVE[tile])[Y]
            if (new_blank_position_x >= 0 and new_blank_position_x < BOARD_SIZE):
                if (new_blank_position_y >= 0 and new_blank_position_y < BOARD_SIZE):
                    new_board_state.board[blank_x][blank_y] = new_board_state.board[new_blank_position_x][new_blank_position_y]
                    new_board_state.board[new_blank_position_x][new_blank_position_y] = BLANK
                    new_board_state.blank = [new_blank_position_x,new_blank_position_y]
                    # Check visited, score the puzzle, add to the frontier
                    if (visited.get(to_tuple(new_board_state.board)) == None):
                        new_node = Node(new_board_state, current_state_node)
                        current_state_node.add_node(new_node, tile)
                        score = h(new_node.board_state.board)
                        if (g == A_STAR):
                            score += new_node.steps
                        frontier[score].append(new_node)
                        current_state_node.add_node(new_node, tile)
                        nodes_added += 1
    return nodes_added

def update_state(frontier):
    ''' Choose next state from the frontier priority queue
    Args:
        frontier: 2-dimenstional List priority queue of leaf puzzle states
    Returns:
        Node: New puzzle state
        int: current best heuristic score
    '''
    new_state = None
    top_score = 0
    index = 0
    for score in range(FRONTIER_MAX_SCORE):
        length = len(frontier[score])
        if (length > 0):
            top_score = score
            if (length > 1):
                index = random.randrange(length-1)
            new_state = frontier[top_score][index]
            del frontier[top_score][index]
            break
    return new_state, top_score

def run_test(frontier, curr_node, visited, moves, heuristic, algorithm):
    ''' Main test loop - Tests one heuristic/algorithm combination
    Args:
        frontier: 2-dimenstional List priority queue of leaf puzzle states
        curr_node: current puzzle state node
        visited: map of previously visited puzzle states
        moves: count of total iterations
        heuristic: heuristic scoring function
        algorithm: algorithm being used (GBFS or A_STAR)
    Returns:
        List: nodes path from start to goal
        bool: True - solution not found / False - solution found 
    '''
    solution_path = None
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
        curr_node, top_score = update_state(frontier)
        current_node_key = to_tuple(curr_node.board_state.board)
        visited[current_node_key] = True
    if (moves < MAX_MOVES):
        solution_path = path(curr_node)
        print("SOLUTION FOUND! Visited Nodes: ", moves, "  Steps: ", curr_node.steps, "  Total Nodes: ", total_nodes, "  Frontier: ", end='')
        for index in range(len(frontier)-1):
            frontier_size = len(frontier[index])
            if (frontier_size > 0):
                print(f"{index}: {frontier_size} ", end='')
        print()
        failed = False
    return solution_path, failed

# ------- MAIN --------
BOARD_SIZE = 3                  # H x W of the board
MAX_MOVES = 10000000            # Maximum number of iterations
REPORT_FREQUENCY = 10000        # Number of iterations to complete between progress reports
X = 0                           # For locating X-location values in array representing coordinates
Y = 1                           # For locating Y-location values in array representing coordinates
BLANK = 0                       # Value of the "blank" space
FRONTIER_MAX_SCORE = 60         # Max heuristic score for frontier priority queue

LEFT_TILE = 0                   # Tile to the left of blank
UP_TILE = 1                     # Tile up from the blank
DOWN_TILE = 2                   # Tile down from the blank
RIGHT_TILE = 3                  # Tile to the right of blank

GBFS = 0                        # Greedy Best First Search
A_STAR = 1                      # A* Search
H1 = 0                          # h1 heuristic
H2 = 1                          # h2 heuristic
H3 = 2                          # h3 heuristic

h_name = {                      # map heuristic to string name
    H1 : "H1",
    H2 : "H2",
    H3 : "H3"
}

algorithm_name = {              # map algorithm to string name
    GBFS : "GBFS",
    A_STAR : "A*"
}

SCORE_FUNCTION = 0              # score function pointer array location
SCORE_LIST = 1                  # score list array location (not used)

MOVE = {                        # Vectors for transitioning to indicated tile
    LEFT_TILE: [-1, 0],
    UP_TILE: [0, -1],
    DOWN_TILE: [0, 1],
    RIGHT_TILE: [1, 0]
}

GOAL_BOARD = Board(BOARD_SIZE, "GOAL")                                      # Goal state
successes = 0                                                               # Puzzles solved
visited = {}                                                                # map of previously visited puzzle states
total_steps = [ [0]*len(algorithm_name) for i in range(len(h_name))]        # store steps for each algorithm/heuristic combination
h_choice = {                                                                # map of heuristics to scoring functions
    H1 : h1_score,
    H2 : h2_score,
    H3 : h3_score
}
# Repeat until the number of successes is reached
while (successes < 1):                                                  
    state_tree = Node(Board(BOARD_SIZE))                                    # Initialize the puzzle root node
    state_tree.board_state.print_board()            

    paths_table = []                                                        # Array for storing solution paths
    failed = False                                                          # failed to find a solution
    
    # Repeat until all heuristics are tested
    for heuristic in range(H1, H3+1):
        paths = []
        # Repeat until all algoritms are tested                                                          
        for algorithm in range(GBFS, A_STAR+1):
            visited = {}                                                    # reset visited map
            moves = 0                                                       # reset moves (iteration) count
            first_node = state_tree                                         
            current_node_key = to_tuple(first_node.board_state.board)       # Create tuple of root puzzle
            visited[current_node_key] = True                                # Set root puzzle map to True
            frontier = [ [] for i in range(FRONTIER_MAX_SCORE) ]            # Initialize frontier priority queue
            print("Heuristic: ", h_name[heuristic], "  Algorithm: ", algorithm_name[algorithm])
            solution_path, failed = run_test(frontier, first_node, visited, moves, h_choice[heuristic], algorithm)
            # if a solution wasn't found, break out of loop
            if (failed == True):
                break
            paths.append(solution_path)
#            solution_path = None
        # if a solution wasn't found, break out of loop
        if (failed == True):
            break
        paths_table.append(paths)
    
    # If a solution is found for all 6 heuristic/algorithm combos, output results
    if (failed == False):
        successes += 1
        print()
        with open("data.txt", "a") as out:
            out.write(str(state_tree.board_state.board) + "\n")
            for heuristic in range(H1, H3+1):
                for algorithm in range(GBFS, A_STAR+1):
                    solution_path = paths_table[heuristic][algorithm]
                    total_steps[heuristic][algorithm] += solution_path[len(solution_path)-1].steps
                    print("Heuristic: ", h_name[heuristic], "  Algorithm: ", algorithm_name[algorithm], "  Steps: ", solution_path[len(solution_path)-1].steps)
                    line = "Heuristic: " + str(h_name[heuristic]) + "  Algorithm: " + str(algorithm_name[algorithm]) + "  Steps: " + str(solution_path[len(solution_path)-1].steps) + "\n"
                    out.write(line)
#                    for node in solution_path:
#                        out.write(str(node.board_state.board) + "-->")
#                        print(node.board_state.board, end='-->')
#                        node.board_state.print_board()
#                        print()
#                    print()
#                    print()
                    out.write("\n\n")
            out.write("\n\n")
            out.close()        
    else:
        print("Failed to find a solution...")   
        print()             