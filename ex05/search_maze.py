import sys
from collections import deque

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RESET = "\033[0m"

def neighbors(grid, r, c):
    H, W = len(grid), len(grid[0])
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):  # UP, DOWN, LEFT, RIGHT
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] != "#":
            yield nr, nc

def search(grid, start, target, algo):
    came_from = {start:None}
    if algo == "bfs":
        frontier = deque([start])
        pop = frontier.popleft
        push = frontier.append
    elif algo == "dfs":
        frontier = [start]
        pop = frontier.pop
        push = frontier.append  
    else:
        raise ValueError("Algorithm must be bfs or dfs")
    
    while frontier:
        r, c = pop()
        if(r, c) == target:
            break
        for nbr in neighbors(grid, r,c):
            if nbr not in came_from:
                came_from[nbr] = (r, c)
                push(nbr)
    
    if target not in came_from:
        return []
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path

def apply_path(grid, path, start, target):
    for (r, c) in path:
        if (r, c) != start and (r, c) != target:
            grid[r][c] = "*"

def print_colored(grid):
    for row in grid:
        line = []
        for ch in row:
            if ch == "*":
                line.append(f"{RED}{ch}{RESET}")
            elif ch == "T":
                line.append(f"{YELLOW}{ch}{RESET}")
            elif ch == "S":
                line.append(f"{GREEN}{ch}{RESET}")
            else:
                line.append(ch)
        print("".join(line))

def main():

    if len(sys.argv) != 3:
        print("Usage: python search_maze.py [bfs|dfs] maze.txt")
        sys.exit(1)

    algorithm = str(sys.argv[1].lower())
    maze_file = str(sys.argv[2])

    with open(maze_file,"r") as f:
        maze = [list(line.rstrip("\n")) for line in f.read().splitlines()]

    #finding coordinates
    start = target = None
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch =="T":
                target = (r, c)

    if start is None or target is None:
            raise ValueError("Maze must contain 'S' (start) and 'T' (target).")
    
    path = search(maze, start, target, algorithm)
    if not path:
        print("No path found.")
        print_colored(maze)
        sys.exit(0)

    apply_path(maze, path, start, target)
    print_colored(maze)

if __name__ == "__main__":
    main()