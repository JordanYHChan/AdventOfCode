from tqdm import tqdm

def parse(input):

    racetrack = []

    for line in open(input, "r"):
        racetrack.append(line.strip("\n"))

    return racetrack

class Racetrack():

    def __init__(self, racetrack):

        self.walls = set()
        self.rows = 0
        self.cols = 0
        self.start = None
        self.end = None

        self.prepare_racetrack(racetrack)
        self.traverse_racetrack()

    def prepare_racetrack(self, racetrack):

        for i, row in enumerate(racetrack):
            for j, track in enumerate(row):
                match track:
                    case "#":
                        self.walls.add((i, j))
                    case "S":
                        self.start = (i, j)
                    case "E":
                        self.end = (i, j)
                self.rows = max(self.rows, i + 1)
                self.cols = max(self.cols, j + 1)

    def check_cheats(self, cheat_limit=20, min_saved_time=100):

        valid_cheats = 0

        for start in tqdm(range(len(self.track) - min_saved_time), leave=False):
            for end in range(start + min_saved_time, len(self.track)):
                cheat_time = self.manhattan_distance(self.track[start], self.track[end])
                saved_time = end - start - cheat_time
                if saved_time >= min_saved_time and cheat_time <= cheat_limit:
                    valid_cheats += 1

        return valid_cheats

    def manhattan_distance(self, start, end):

        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def traverse_racetrack(self):

        self.track = [self.start]

        while self.track[-1] != self.end:
            self.track.append(self.get_track_next_move(self.track[-1]))

    def get_track_next_move(self, position):

        for position in self.get_next_moves(position):
            if position in self.walls:
                continue
            if position in self.track:
                continue
            
            return position

    def get_next_moves(self, position):

        row, col = position

        return [
            (row + i, col + j)
            for i, j in [
                (0, 1), (1, 0), (0, -1), (-1, 0)
            ]
            if (
                0 <= row + i < self.rows
            ) and (
                0 <= col + j < self.cols
            )
        ]

    def __repr__(self):
        
        racetrack = [
            [
                "S" if (i, j) == self.start else
                "E" if (i, j) == self.end else
                "#" if (i, j) in self.walls else
                "."
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

        return "\n".join(
            ["".join(row) for row in racetrack]
        )

if __name__ == "__main__":

    racetrack = parse(input("Input File: "))
    racetrack = Racetrack(racetrack)
    cheat_limit = int(input("Cheat Timer Limit: "))
    min_saved_time = int(input("Minimum Saved Time: "))
    print(f"Number of Valid Cheats: {racetrack.check_cheats(cheat_limit, min_saved_time)}")