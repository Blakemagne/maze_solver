from graphics import Window
from maze import Maze
import sys
import time


def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    print("maze created")
    
    # Solve with DFS
    print("\nSolving with DFS...")
    start_time = time.time()
    is_solvable = maze.solve(algorithm="dfs")
    dfs_time = time.time() - start_time
    if not is_solvable:
        print("maze can not be solved!")
    else:
        print(f"maze solved with DFS in {dfs_time:.3f} seconds!")
    
    # Wait a bit before solving with BFS
    time.sleep(2)
    
    # Reset and solve with BFS
    print("\nSolving with BFS...")
    start_time = time.time()
    is_solvable = maze.solve(algorithm="bfs")
    bfs_time = time.time() - start_time
    if not is_solvable:
        print("maze can not be solved!")
    else:
        print(f"maze solved with BFS in {bfs_time:.3f} seconds!")
    
    print(f"\nComparison: DFS: {dfs_time:.3f}s, BFS: {bfs_time:.3f}s")
    
    win.wait_for_close()


main()
