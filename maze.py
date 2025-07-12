from cell import Cell
import random
import time
from collections import deque


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__cells = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self, delay=0.01):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(delay)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self.__draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self.__break_walls_r(next_index[0], next_index[1])

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False
    
    def __clear_solution_paths(self):
        # Clear the entire canvas and redraw the maze structure
        if self.__win is not None:
            self.__win.clear_canvas()
            # Redraw all cells - this preserves the broken walls from maze generation
            for i in range(self.__num_cols):
                for j in range(self.__num_rows):
                    self.__draw_cell(i, j)
            # Add a small delay to show the cleared maze
            self.__animate(0.1)

    # returns True if this is the end cell, OR if it leads to the end cell.
    # returns False if this is a loser cell.
    def _solve_r(self, i, j):
        self.__animate(0.005)  # Fast animation for exploring

        # vist the current cell
        self.__cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], True)
                self.__animate(0.02)  # Slower animation for backtracking

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.__num_cols - 1
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], True)
                self.__animate(0.02)  # Slower animation for backtracking

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], True)
                self.__animate(0.02)  # Slower animation for backtracking

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.__num_rows - 1
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)
                self.__animate(0.02)  # Slower animation for backtracking

        # we went the wrong way let the previous cell know by returning False
        return False

    # create the moves for the solution using a depth first search
    def solve(self, algorithm="dfs"):
        self.__reset_cells_visited()
        if algorithm == "dfs":
            return self._solve_r(0, 0)
        elif algorithm == "bfs":
            return self._solve_bfs()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def _solve_bfs(self):
        # BFS implementation - find path without drawing until the end
        queue = deque([(0, 0, [(0, 0)])])  # (i, j, path)
        visited = set()
        visited.add((0, 0))
        
        while queue:
            i, j, path = queue.popleft()
            
            # Check if we reached the end
            if i == self.__num_cols - 1 and j == self.__num_rows - 1:
                # Draw the BFS solution path in bright green over existing lines
                for k in range(len(path) - 1):
                    curr_i, curr_j = path[k]
                    next_i, next_j = path[k + 1]
                    self.__cells[curr_i][curr_j].draw_move(self.__cells[next_i][next_j], color="#00ff41")  # Bright green
                    self.__animate(0.05)  # Slower to show solution clearly
                return True
            
            # Check all four directions
            directions = [
                (i - 1, j, not self.__cells[i][j].has_left_wall),  # left
                (i + 1, j, not self.__cells[i][j].has_right_wall),  # right
                (i, j - 1, not self.__cells[i][j].has_top_wall),  # up
                (i, j + 1, not self.__cells[i][j].has_bottom_wall)  # down
            ]
            
            for next_i, next_j, can_move in directions:
                if (0 <= next_i < self.__num_cols and 
                    0 <= next_j < self.__num_rows and 
                    can_move and 
                    (next_i, next_j) not in visited):
                    
                    visited.add((next_i, next_j))
                    new_path = path + [(next_i, next_j)]
                    queue.append((next_i, next_j, new_path))
        
        return False
