# Experiment 2 : 

# A* start algorithm | A problem solving algorithm
# f(n) = g(n)  + h(n) 
# g(n) --> actual value | written on the edges
# h(n) --> heurastic value | wriiten along the node

import heapq

class PuzzleState:
    def __init__(self, board, g=0, parent=None):
        self.board = board  # 1D tuple representing the 3x3 grid
        self.g = g          # Path cost
        self.h = self.calculate_manhattan()
        self.f = self.g + self.h
        self.parent = parent

    def calculate_manhattan(self):
        distance = 0
        goal_pos = {val: (i // 3, i % 3) for i, val in enumerate((1, 2, 3, 4, 5, 6, 7, 8, 0))}
        for i, tile in enumerate(self.board):
            if tile != 0:
                curr_row, curr_col = i // 3, i % 3
                goal_row, goal_col = goal_pos[tile]
                distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return distance

    def __lt__(self, other):
        return self.f < other.f

    def get_neighbors(self):
        neighbors = []
        zero_idx = self.board.index(0)
        row, col = zero_idx // 3, zero_idx % 3
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_board = list(self.board)
                neighbor_idx = nr * 3 + nc
                new_board[zero_idx], new_board[neighbor_idx] = new_board[neighbor_idx], new_board[zero_idx]
                neighbors.append(PuzzleState(tuple(new_board), self.g + 1, self))
        return neighbors

def solve_a_star(start_board):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    start_state = PuzzleState(start_board)
    
    open_list = [start_state]
    closed_set = set()

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.board == goal:
            return reconstruct_path(current_state)

        closed_set.add(current_state.board)

        for neighbor in current_state.get_neighbors():
            if neighbor.board in closed_set:
                continue
            heapq.heappush(open_list, neighbor)

    return None

def reconstruct_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    return path[::-1]

initial_board = (1, 2, 3, 0, 4, 6, 7, 5, 8)
solution = solve_a_star(initial_board)

for step in solution:
    print(step[0:3])
    print(step[3:6])
    print(step[6:9])
    print("---")