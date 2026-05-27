import random
from copy import deepcopy

class SudokuGame:
    def __init__(self, difficulty='medium'):
        """
        Initialize Sudoku game with specified difficulty.
        difficulty: 'easy' (35-40 empty), 'medium' (45-50 empty), 'hard' (55-60 empty)
        """
        self.difficulty = difficulty
        self.board = [[0] * 9 for _ in range(9)]
        self.solution = [[0] * 9 for _ in range(9)]
        self.original_board = [[0] * 9 for _ in range(9)]
        self.generate_board()
        
    def generate_board(self):
        """Generate a new Sudoku board."""
        # Fill diagonal 3x3 boxes (they don't conflict with each other)
        for box in range(3):
            self.fill_box(box, box)
        
        # Fill remaining cells
        self.solve(self.board)
        
        # Save the complete solution
        self.solution = deepcopy(self.board)
        
        # Remove numbers based on difficulty
        self.remove_numbers()
        
        # Save the original puzzle
        self.original_board = deepcopy(self.board)
    
    def fill_box(self, row_box, col_box):
        """Fill a 3x3 box with random numbers 1-9."""
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_box * 3 + i][col_box * 3 + j] = nums[i * 3 + j]
    
    def is_valid(self, board, row, col, num):
        """Check if placing num at board[row][col] is valid."""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def solve(self, board):
        """Solve the Sudoku puzzle using backtracking."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    
    def remove_numbers(self):
        """Remove numbers from the solved board based on difficulty."""
        if self.difficulty == 'easy':
            remove_count = random.randint(35, 40)
        elif self.difficulty == 'hard':
            remove_count = random.randint(55, 60)
        else:  # medium
            remove_count = random.randint(45, 50)
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i in range(remove_count):
            row, col = cells[i]
            self.board[row][col] = 0
    
    def display(self):
        """Display the current board state."""
        print("\n   0 1 2   3 4 5   6 7 8")
        print("  " + "─" * 25)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("  " + "─" * 25)
            row_str = f"{i} │ "
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "│ "
                val = self.board[i][j] if self.board[i][j] != 0 else "."
                row_str += f"{val} "
            print(row_str)
        print()
    
    def is_complete(self):
        """Check if the board is completely filled."""
        return all(self.board[i][j] != 0 for i in range(9) for j in range(9))
    
    def is_valid_move(self, row, col, num):
        """Check if a move is valid."""
        if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
            return False
        if self.board[row][col] != 0:
            return False
        return self.is_valid(self.board, row, col, num)
    
    def place_number(self, row, col, num):
        """Place a number on the board."""
        if self.is_valid_move(row, col, num):
            self.board[row][col] = num
            return True
        return False
    
    def remove_number(self, row, col):
        """Remove a number from the board (undo a move)."""
        if self.original_board[row][col] == 0:
            self.board[row][col] = 0
            return True
        return False
    
    def get_hint(self):
        """Provide a hint by revealing a cell from the solution."""
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                       if self.board[i][j] == 0 and self.original_board[i][j] == 0]
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = self.solution[row][col]
            return row, col, self.solution[row][col]
        return None
    
    def reset(self):
        """Reset the board to its initial state."""
        self.board = deepcopy(self.original_board)
    
    def is_solved(self):
        """Check if the current board matches the solution."""
        return self.board == self.solution


def play_game():
    """Main game loop for playing Sudoku."""
    print("╔═════════════════════════════════════╗")
    print("║         WELCOME TO SUDOKU           ║")
    print("╚═════════════════════════════════════╝")
    
    # Choose difficulty
    print("\nSelect difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == '1':
            difficulty = 'easy'
            break
        elif choice == '2':
            difficulty = 'medium'
            break
        elif choice == '3':
            difficulty = 'hard'
            break
        else:
            print("Invalid choice. Please try again.")
    
    game = SudokuGame(difficulty)
    
    print(f"\n{difficulty.upper()} Sudoku Game Started!")
    print("\nControls:")
    print("  place <row> <col> <num> - Place a number")
    print("  remove <row> <col>      - Remove a number")
    print("  hint                     - Get a hint")
    print("  show                     - Display the board")
    print("  reset                    - Reset the board")
    print("  solve                    - Show the solution")
    print("  quit                     - Exit the game")
    print("\n(Use 0-8 for row/col indices)")
    
    game.display()
    
    while True:
        command = input("Command: ").strip().lower().split()
        
        if not command:
            continue
        
        if command[0] == 'quit':
            print("Thanks for playing! Goodbye!")
            break
        
        elif command[0] == 'show':
            game.display()
        
        elif command[0] == 'reset':
            game.reset()
            print("Board reset to initial state.")
            game.display()
        
        elif command[0] == 'hint':
            hint = game.get_hint()
            if hint:
                row, col, num = hint
                print(f"Hint: Row {row}, Col {col} = {num}")
                game.display()
            else:
                print("No more hints available!")
        
        elif command[0] == 'place':
            if len(command) != 4:
                print("Usage: place <row> <col> <num>")
                continue
            try:
                row, col, num = int(command[1]), int(command[2]), int(command[3])
                if game.place_number(row, col, num):
                    print(f"✓ Placed {num} at [{row},{col}]")
                    game.display()
                    
                    if game.is_complete() and game.is_solved():
                        print("╔══════════════════════════════════╗")
                        print("║   🎉 CONGRATULATIONS! YOU WON! 🎉 ║")
                        print("╚══════════════════════════════════╝")
                        break
                else:
                    print("✗ Invalid move. That number violates Sudoku rules.")
            except (ValueError, IndexError):
                print("Invalid input. Use: place <row> <col> <num>")
        
        elif command[0] == 'remove':
            if len(command) != 3:
                print("Usage: remove <row> <col>")
                continue
            try:
                row, col = int(command[1]), int(command[2])
                if game.remove_number(row, col):
                    print(f"✓ Removed number from [{row},{col}]")
                    game.display()
                else:
                    print("✗ Cannot remove this cell (it's part of the puzzle).")
            except (ValueError, IndexError):
                print("Invalid input. Use: remove <row> <col>")
        
        elif command[0] == 'solve':
            print("Solution:")
            for i in range(9):
                if i % 3 == 0 and i != 0:
                    print("  " + "─" * 25)
                row_str = f"{i} │ "
                for j in range(9):
                    if j % 3 == 0 and j != 0:
                        row_str += "│ "
                    row_str += f"{game.solution[i][j]} "
                print(row_str)
            print()
        
        else:
            print("Unknown command. Type 'show' to see the board or 'quit' to exit.")


if __name__ == "__main__":
    play_game()
