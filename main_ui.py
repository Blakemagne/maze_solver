from tkinter import Tk, Frame, Label, Button, Scale, StringVar, OptionMenu, HORIZONTAL
from graphics import Window
from maze import Maze
import sys
import time
import threading


class MazeSolverUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Maze Solver Control Panel")
        self.root.geometry("300x500")
        
        # Variables
        self.num_rows = 12
        self.num_cols = 16
        self.algorithm = StringVar(value="dfs")
        self.solving = False
        self.maze_window = None
        self.maze = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = Label(self.root, text="Maze Solver Configuration", font=("Arial", 16))
        title.pack(pady=10)
        
        # Rows control
        Label(self.root, text="Number of Rows:").pack()
        self.rows_scale = Scale(self.root, from_=5, to=50, orient=HORIZONTAL, 
                                command=self.update_rows)
        self.rows_scale.set(self.num_rows)
        self.rows_scale.pack(pady=5)
        
        # Columns control
        Label(self.root, text="Number of Columns:").pack()
        self.cols_scale = Scale(self.root, from_=5, to=50, orient=HORIZONTAL,
                                command=self.update_cols)
        self.cols_scale.set(self.num_cols)
        self.cols_scale.pack(pady=5)
        
        # Algorithm selection
        Label(self.root, text="Algorithm:").pack(pady=(20, 5))
        algorithms = ["dfs", "bfs"]
        self.algo_menu = OptionMenu(self.root, self.algorithm, *algorithms)
        self.algo_menu.pack()
        
        # Buttons
        self.generate_btn = Button(self.root, text="Generate New Maze", 
                                   command=self.generate_maze, bg="#4CAF50", fg="white")
        self.generate_btn.pack(pady=10)
        
        self.solve_btn = Button(self.root, text="Solve Maze", 
                                command=self.solve_maze, bg="#2196F3", fg="white")
        self.solve_btn.pack(pady=5)
        
        # Statistics
        self.stats_frame = Frame(self.root)
        self.stats_frame.pack(pady=20)
        self.time_label = Label(self.stats_frame, text="Solve Time: --")
        self.time_label.pack()
        
        # Instructions
        instructions = Label(self.root, text="Instructions:\n" +
                            "1. Adjust maze size with sliders\n" +
                            "2. Select solving algorithm\n" +
                            "3. Click 'Generate New Maze'\n" +
                            "4. Click 'Solve Maze' to watch it solve",
                            justify="left", font=("Arial", 10))
        instructions.pack(pady=20)
        
    def update_rows(self, value):
        self.num_rows = int(value)
        
    def update_cols(self, value):
        self.num_cols = int(value)
        
    def generate_maze(self):
        # Close existing window if any
        if self.maze_window:
            self.maze_window.close()
            
        # Calculate dimensions
        margin = 50
        screen_x = 800
        screen_y = 600
        cell_size_x = (screen_x - 2 * margin) / self.num_cols
        cell_size_y = (screen_y - 2 * margin) / self.num_rows
        
        # Create new window and maze
        self.maze_window = Window(screen_x, screen_y)
        self.maze = Maze(margin, margin, self.num_rows, self.num_cols, 
                         cell_size_x, cell_size_y, self.maze_window, 10)
        
        # Update button states
        self.solve_btn['state'] = 'normal'
        self.time_label.config(text="Solve Time: --")
        
    def solve_maze(self):
        if not self.maze or self.solving:
            return
            
        self.solving = True
        self.solve_btn['state'] = 'disabled'
        
        # Solve in a separate thread to keep UI responsive
        def solve_thread():
            start_time = time.time()
            
            # Get selected algorithm
            algo = self.algorithm.get()
            result = self.maze.solve(algorithm=algo)
            
            end_time = time.time()
            solve_time = end_time - start_time
            
            # Update UI
            self.root.after(0, lambda: self.time_label.config(
                text=f"Solve Time: {solve_time:.3f}s ({algo.upper()})"
            ))
            
            if result:
                print(f"Maze solved using {algo.upper()}!")
            else:
                print(f"Maze cannot be solved!")
                
            self.solving = False
            self.root.after(0, lambda: self.solve_btn.config(state='normal'))
            
        thread = threading.Thread(target=solve_thread)
        thread.start()
        
    def run(self):
        sys.setrecursionlimit(10000)
        self.root.mainloop()


if __name__ == "__main__":
    app = MazeSolverUI()
    app.run()