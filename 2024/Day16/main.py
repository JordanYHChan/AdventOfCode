from collections import deque

def parse(input):

    maze = []

    for line in open(input, "r"):
        maze.append(line.strip("\n"))

    return maze

class Maze():

    def __init__(self, maze):

        self.prepare_maze(maze)
        self.traverse_maze()
        self.traverse_maze(forward=False)

    def prepare_maze(self, maze):

        self.maze = {}
        self.rows = 0
        self.cols = 0
        self.queue = deque()

        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                self.maze[i, j] = Cell(cell)
                self.rows = max(self.rows, i+1)
                self.cols = max(self.cols, j+1)
                if cell == "S":
                    self.start = i, j
                if cell == "E":
                    self.end = i, j

    def traverse_maze(self, forward=True):

        checks = self.forward_checks if forward else self.backward_checks
        self.queue.append(self.start if forward else self.end)
        while len(self.queue) > 0:
            row, col = self.queue.popleft()
            current_cell = self.maze[row, col]

            for neighbour_row, neighbour_col, neighbour_direction in self.get_valid_neighbours(row, col):
                checks(current_cell, neighbour_row, neighbour_col, neighbour_direction)

        self.maze[self.end].update_best_path_scores(self.maze[self.end].get_best_score())

    def forward_checks(self, current_cell, neighbour_row, neighbour_col, neighbour_direction):                
        best_score, best_direction = current_cell.get_best_score_and_direction()
        if self.opposite_directions(best_direction, neighbour_direction):
            return

        neighbour_cell = self.maze[neighbour_row, neighbour_col]

        score = best_score + (
            1 if best_direction == neighbour_direction else
            1001
        )
        neighbour_cell.update_scores(score, neighbour_direction)

        if neighbour_cell.get_best_score() == score:
            self.queue.append((neighbour_row, neighbour_col))

    def backward_checks(self, current_cell, neighbour_row, neighbour_col, neighbour_direction):
        if current_cell.is_start:
            current_cell.update_cell("O")

        neighbour_cell = self.maze[neighbour_row, neighbour_col]        

        if self.valid_best_path_step(current_cell, neighbour_cell):
            current_cell.update_cell("O")
            self.queue.append((neighbour_row, neighbour_col))

    def valid_best_path_step(self, current, neighbour):

        best_path_scores = current.best_path_scores
        neighbour_score = neighbour.get_best_score()

        if neighbour_score + 1 in best_path_scores:
            neighbour.update_best_path_scores(neighbour_score)
            return True
        
        if neighbour_score + 1001 in best_path_scores:
            neighbour.update_best_path_scores(neighbour_score)
            neighbour.update_best_path_scores(neighbour_score + 1000)
            return True

        return False

    def get_side_directions(self, direction):
        if direction in ["^", "v"]:
            return [">", "<"]
        return ["^", "v"]

    def get_score(self):

        return self.maze[self.end].get_best_score()
    
    def get_tiles(self):

        return sum([
            sum([
                self.maze[i, j].cell == "O"
                for j in range(self.cols)
            ]) for i in range(self.rows)
        ])

    def opposite_directions(self, direction1, direction2):
        match direction1, direction2:
            case "^", "v":
                return True
            case ">", "<":
                return True
            case "v", "^":
                return True
            case "<", ">":
                return True
        return False

    def get_valid_neighbours(self, row, col):

        return [
            (i, j, direction) for i, j, direction in self.get_neighbours(row, col)
            if not self.maze[i, j].is_wall
        ]

    def get_neighbours(self, row, col):

        return [
            (row + i, col + j, direction)
            for (i, j), direction in zip(
                [(-1, 0), (0, 1), (1, 0), (0, -1)],
                ["^", ">", "v", "<"]
            )
        ]

    def __repr__(self):

        maze = [
            [
                self.maze[i, j].cell
                for j in range(self.cols)
            ] for i in range(self.rows)
        ]

        return "\n".join(
            ["".join(row) for row in maze]
        )

class Cell():

    def __init__(self, cell):

        self.cell = cell
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.scores = {}
        self.best_path_scores = set()

        match self.cell:
            case "#":
                self.is_wall = True
            case "S":
                self.is_start = True
                self.scores[0] = ">"
            case "E":
                self.is_end = True

    def get_best_score(self):
        if self.scores == {}:
            return None
        
        return min(self.scores)

    def get_best_score_and_direction(self):
        return self.get_best_score(), self.get_best_direction()

    def get_best_direction(self):
        best_score = self.get_best_score()

        if best_score is None:
            return None
        
        return self.scores[best_score]

    def update_scores(self, score, direction):
        self.scores[score] = direction

    def update_best_path_scores(self, score):
        self.best_path_scores.add(score)

    def update_cell(self, cell):
        self.cell = cell

    def __repr__(self):
        return self.cell

if __name__ == "__main__":

    maze = parse(input("Input File: "))
    maze = Maze(maze)
    print(f"Lowest Score: {maze.get_score()}")
    print(f"Number of Tiles: {maze.get_tiles()}")