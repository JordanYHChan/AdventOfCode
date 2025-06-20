def parse(input):

    map = []

    for row in open(input, "r"):
        map.append([[cell] for cell in row.strip("\n")])

    return map

class Map():

    def __init__(self, map):

        self.map = map
        self.finished = False
        self.loop = False
        
        self.rows = len(self.map)
        self.cols = len(self.map[0])

        self.turn_mapping = {
            "^" : ">",
            ">" : "v",
            "v" : "<",
            "<" : "^",
        }

        self.guard_front_row_mapping = {
            "^" : -1,
            ">" : 0,
            "v" : 1,
            "<" : 0,
        }

        self.guard_front_col_mapping = {
            "^" : 0,
            ">" : 1,
            "v" : 0,
            "<" : -1,
        }

        self.prepare_guard_location_and_direction()

    def trace_path(self, check_loops=False):

        while not self.finished:
            self.iterate_guard(check_loops)

    def iterate_guard(self, check_loops=False):

        if not self.valid_front():
            self.map[self.guard_row][self.guard_col].append(self.guard_direction)
            self.finished = True
            return

        front = self.map[self.guard_front_row][self.guard_front_col]

        if front in [["O"], ["#"]]:
            self.turn_guard()
            return
        
        if self.valid_loop(front):
            self.loop = True
            self.finished = True
            return
        
        if check_loops and self.map[self.guard_front_row][self.guard_front_col] == ["."]:
            self.map[self.guard_front_row][self.guard_front_col].append(self.check_looping_obstacle())

        self.walk_guard()

    def get_obstacle_map(self):

        map = [
            [
                ["#"] if "#" in cell else ["."]
                for cell in row
            ] for row in self.map
        ]
        map[self.guard_row][self.guard_col] = [self.guard_direction]
        map[self.guard_front_row][self.guard_front_col] = ["O"]

        return map

    def check_looping_obstacle(self):

        obstacle_map = Map(self.get_obstacle_map())
        obstacle_map.trace_path()

        return "valid looping obstacle" if obstacle_map.loop else "invalid looping obstacle"

    def valid_front(self):

        return (
            0 <= self.guard_front_row < self.rows and
            0 <= self.guard_front_col < self.cols
        )
    
    def valid_loop(self, front):

        return self.guard_direction in front

    def walk_guard(self):

        self.guard_row, self.guard_col = self.guard_front_row, self.guard_front_col
        self.map[self.guard_row][self.guard_col].append(self.guard_direction)
        self.prepare_guard_front()

    def turn_guard(self):

        self.guard_direction = self.turn_mapping.get(self.guard_direction)
        self.map[self.guard_row][self.guard_col].append(self.guard_direction)
        self.prepare_guard_front()

    def prepare_guard_location_and_direction(self):
        
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):

                if cell in [["."], ["#"], ["O"]]:
                    continue

                self.guard_direction = cell[0]
                self.guard_row, self.guard_col = i, j
                self.prepare_guard_front()
                break

    def prepare_guard_front(self):
        
        self.guard_front_row = self.guard_row + self.guard_front_row_mapping.get(self.guard_direction)
        self.guard_front_col = self.guard_col + self.guard_front_col_mapping.get(self.guard_direction)

    def get_visited_count(self):

        if not self.finished:
            self.trace_path(check_loops=True)

        return sum([
            sum([
                len(set(cell).intersection({"^", ">", "v", "<"})) > 0
                for cell in row
            ]) for row in self.map
        ])
    
    def get_looping_obstacles_count(self):

        return sum([
            sum([
                "valid looping obstacle" in cell
                for cell in row
            ]) for row in self.map
        ])

if __name__ == "__main__":

    input = input("Input File: ")
    map = parse(input)

    map = Map(map)
    visited_count = map.get_visited_count()
    print(f"Visited Count: {visited_count}")

    looping_obstacles = map.get_looping_obstacles_count()
    print(f"Looping Obstacles Count: {looping_obstacles}")
