def parse(input):

    map = []

    for line in open(input, "r"):
        map.append(line.strip("\n"))

    return map

class Map():

    def __init__(self, map):

        self.prepare_map(map)
        self.calculate_scores_and_ratings()

    def prepare_map(self, map):

        self.map = {}

        for i, row in enumerate(map):
            for j, height in enumerate(row):
                height = int(height)
                self.map.setdefault(height, []).append(Cell(i, j, height))

    def calculate_scores_and_ratings(self):

        for height in range(8, -1, -1):
            aboves = {
                above.get_coordinates(): above for above in self.map.get(height+1)
            }

            for cell in self.map.get(height):
                for neighbour_coordinates in cell.get_neighbour_coordinates():
                    if neighbour_coordinates in aboves.keys():
                        above = aboves[neighbour_coordinates]
                        cell.add_reachable_summits(above.reachable_summits)
                        cell.add_rating(above.get_rating())

    def get_trailhead_scores_sum(self):

        return sum([
            cell.get_score()
            for cell in self.map.get(0)
        ])
    
    def get_trailhead_ratings_sum(self):

        return sum([
            cell.get_rating()
            for cell in self.map.get(0)
        ])

class Cell():

    def __init__(self, row, col, height):

        self.row = row
        self.col = col
        self.height = height
        self.reachable_summits = set()

        if self.height == 9:
            self.add_reachable_summits([self])

        self.rating = 1 if self.height == 9 else 0

    @property
    def is_trailhead(self):
        return self.height == 0

    def get_score(self):
        return len(self.reachable_summits)

    def get_rating(self):
        return self.rating
    
    def add_reachable_summits(self, summits):
        for summit in summits:
            self.reachable_summits.add(summit)

    def add_rating(self, rating):
        self.rating += rating

    def get_coordinates(self):
        return self.row, self.col
    
    def get_neighbour_coordinates(self):
        return [
            (self.row + i, self.col + j)
            for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        ]
    
    def __repr__(self):
        return f"Cell({self.row}, {self.col})"

if __name__ == "__main__":

    input_file = input("Input File: ")
    map = parse(input_file)
    map = Map(map)

    trailhead_scores_sum = map.get_trailhead_scores_sum()
    print(f"Trailhead Scores Sum: {trailhead_scores_sum}")

    trailhead_ratings_sum = map.get_trailhead_ratings_sum()
    print(f"Trailhead Ratings Sum: {trailhead_ratings_sum}")