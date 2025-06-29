def parse(input):

    map = []
    moves = ""
    map_finished = False

    for line in open(input, "r"):

        if line == "\n":
            map_finished = True
            continue
        
        if not map_finished:
            map.append(line.strip("\n"))
            continue

        moves += line.strip("\n")

    return map, moves

class Warehouse():

    def __init__(self, map):

        self.walls = set()
        self.boxes = set()
        self.robot_row = None
        self.robot_col = None
        self.rows = 0
        self.cols = 0

        self.prepare_map(map)

    def prepare_map(self, map):

        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                match cell:
                    case ".":
                        continue
                    case "#":
                        self.walls.add((i, j))
                    case "O":
                        self.boxes.add((i, j))
                    case "@":
                        self.robot_row, self.robot_col = i, j
                self.rows = max(self.rows, i+1)
                self.cols = max(self.cols, j+1)

    def move_robot(self, moves):

        for move in moves:
            free_space = self.check_free_space(move)

            if free_space is None:
                continue
            
            self.robot_row, self.robot_col = self.move(self.robot_row, self.robot_col, move)
            self.move_boxes(free_space, move)

    def move_boxes(self, free_space, move):
        
        if free_space == (self.robot_row, self.robot_col):
            return

        self.boxes.remove((self.robot_row, self.robot_col))
        self.boxes.add(free_space)

    def check_free_space(self, move):

        row, col = self.robot_row, self.robot_col
        self.boxes_to_update = set()

        while True:
            row, col = self.move(row, col, move)
            if (row, col) in self.walls:
                return None
            if (row, col) in self.get_boxes():
                self.boxes_to_update.add((row, col))
                continue
            return (row, col)
    
    def get_boxes(self):

        return self.boxes

    def move(self, row, col, move):

        match move:
            case "^":
                row -= 1
            case ">":
                col += 1
            case "v":
                row += 1
            case "<":
                col -= 1

        return row, col
    
    def sum_of_box_coordinates(self):

        return sum([
            100 * box_row + box_col
            for box_row, box_col in self.boxes
        ])
    
    def __repr__(self):
        
        output = [
            [
                "#" if (i, j) in self.walls else
                "O" if (i, j) in self.boxes else
                "@" if (i, j) == (self.robot_row, self.robot_col) else
                "."
                for j in range(self.cols)
            ] for i in range(self.cols)
        ]

        return "\n".join(
            ["".join(row) for row in output]
        )
    
class BigWarehouse(Warehouse):

    def __init__(self, map):

        self.boxes_right = set()
        super().__init__(map)

    def prepare_map(self, map):

        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                match cell:
                    case ".":
                        continue
                    case "#":
                        self.walls.add((i, 2*j))
                        self.walls.add((i, 2*j+1))
                    case "O":
                        self.boxes.add((i, 2*j))
                        self.boxes_right.add((i, 2*j+1))
                    case "@":
                        self.robot_row, self.robot_col = i, 2*j
                
                self.rows = max(self.rows, i+1)
                self.cols = max(self.cols, 2*j+2)

    def move_boxes(self, free_space, move):

        if free_space == (self.robot_row, self.robot_col):
            return
        
        left_boxes = []
        right_boxes = []

        for row, col in self.boxes_to_update:
            if (row, col) in self.boxes:
                self.boxes.remove((row, col))
                left_boxes.append(self.move(row, col, move))
            else:
                self.boxes_right.remove((row, col))
                right_boxes.append(self.move(row, col, move))

        for row, col in left_boxes:
            self.boxes.add((row, col))

        for row, col in right_boxes:
            self.boxes_right.add((row, col))

    def check_free_space(self, move):

        if move in [">", "<"]:
            return super().check_free_space(move)
        
        row = self.robot_row
        cols = set([self.robot_col])
        self.boxes_to_update = set()

        while True:
            row, _ = self.move(row, self.robot_col, move)
            new_cols = set()

            for col in cols:
                if (row, col) in self.walls:
                    return None
                if (row, col) in self.boxes:
                    self.boxes_to_update.add((row, col))
                    self.boxes_to_update.add((row, col+1))
                    new_cols.add(col)
                    new_cols.add(col+1)
                    continue
                if (row, col) in self.boxes_right:
                    self.boxes_to_update.add((row, col))
                    self.boxes_to_update.add((row, col-1))
                    new_cols.add(col)
                    new_cols.add(col-1)
                    continue

            if len(new_cols) == 0:
                return (row, self.robot_col)
            
            cols = new_cols

    def get_boxes(self):
        
        return self.boxes.union(self.boxes_right)
    
    def __repr__(self):
        
        output = [
            [
                "#" if (i, j) in self.walls else
                "[" if (i, j) in self.boxes else
                "]" if (i, j) in self.boxes_right else
                "@" if (i, j) == (self.robot_row, self.robot_col) else
                "."
                for j in range(self.cols)
            ] for i in range(self.rows)
        ]

        return "\n".join(
            ["".join(row) for row in output]
        )

if __name__ == "__main__":

    map, moves = parse(input("Input File: "))
    warehouse = Warehouse(map)
    warehouse.move_robot(moves)
    print(f"Sum of box coordinates: {warehouse.sum_of_box_coordinates()}")
    big_warehouse = BigWarehouse(map)
    big_warehouse.move_robot(moves)
    print(f"Sum of big box coordinates: {big_warehouse.sum_of_box_coordinates()}")