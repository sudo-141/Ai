# N-Queens using Backtracking + Branch & Bound

def solve_n_queens(n):
    board = [[0 for _ in range(n)] for _ in range(n)]

    # Branch & Bound helpers
    col = [False] * n
    diag1 = [False] * (2 * n - 1)   # row + col
    diag2 = [False] * (2 * n - 1)   # row - col + (n-1)

    def solve(row):
        # Base case
        if row == n:
            print_solution(board)
            return True

        for c in range(n):
            # Check constraints (Branch & Bound pruning)
            if not col[c] and not diag1[row + c] and not diag2[row - c + n - 1]:
                
                # Place queen
                board[row][c] = 1
                col[c] = diag1[row + c] = diag2[row - c + n - 1] = True

                # Recur
                if solve(row + 1):
                    return True  # remove this line to get all solutions

                # Backtrack
                board[row][c] = 0
                col[c] = diag1[row + c] = diag2[row - c + n - 1] = False

        return False

    def print_solution(board):
        print("\nSolution:")
        for row in board:
            print(" ".join("Q" if x == 1 else "." for x in row))

    if not solve(0):
        print("No solution exists")


# Run
n = int(input("Enter value of N: "))
solve_n_queens(n)