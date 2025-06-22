def parse(input):

    map = []

    for line in open(input, "r"):
        map.append(line.strip("\n"))

    return map

class Map():

    def __init__(self, map):

        self.rows = len(map)
        self.cols = len(map[0])
        self.frequencies = set()
        self.antinodes = set()
        self.resonant_antinodes = set()
        self.antennas = {}

        for row, rows in enumerate(map):
            for col, frequency in enumerate(rows):
                if frequency != ".":
                    self.frequencies.add(frequency)
                    self.antennas[frequency] = self.antennas.get(frequency, []) + [
                        Antenna(row, col, frequency)
                    ]

    def get_resonant_antinodes(self):

        for frequency in self.frequencies:
            antenna_pairs = self.get_all_antenna_pairs(frequency)

            for antenna1, antenna2 in antenna_pairs:
                resonant_antinode_coordinates = self.get_resonant_antinode_coordinates(antenna1, antenna2)

                for antinode_row, antinode_col in resonant_antinode_coordinates:
                    if self.valid_antinode(antinode_row, antinode_col):
                        self.resonant_antinodes.add((antinode_row, antinode_col))

        return self.resonant_antinodes

    def get_antinodes(self):

        for frequency in self.frequencies:
            antenna_pairs = self.get_all_antenna_pairs(frequency)
            
            for antenna1, antenna2 in antenna_pairs:
                antinode_row, antinode_col = self.get_antinode_coordinates(antenna1, antenna2)

                if self.valid_antinode(antinode_row, antinode_col):
                    self.antinodes.add((antinode_row, antinode_col))

        return self.antinodes
    
    def valid_antinode(self, antinode_row, antinode_col):

        return (
            0 <= antinode_row < self.rows and 
            0 <= antinode_col < self.cols
        )

    def get_resonant_antinode_coordinates(self, antenna1, antenna2):

        row1, col1 = antenna1.get_coordinates()
        drow, dcol = self.calculate_direction(antenna1, antenna2)

        return [
            (row1 + i * drow, col1 + j * dcol)
            for i, j in zip(
                range(-self.rows, self.rows + 1),
                range(-self.cols, self.cols + 1)
            )
        ]

    def get_antinode_coordinates(self, antenna1, antenna2):

        row1, col1 = antenna1.get_coordinates()
        drow, dcol = self.calculate_direction(antenna1, antenna2)

        return row1 + drow, col1 + dcol
    
    def get_all_antenna_pairs(self, frequency):

        antennas = self.antennas.get(frequency, [])

        return [
            (antenna1, antenna2)
            for antenna1 in antennas
            for antenna2 in antennas
            if antenna1 != antenna2
        ]

    def calculate_direction(self, antenna1, antenna2):

        row1, col1 = antenna1.get_coordinates()
        row2, col2 = antenna2.get_coordinates()

        return row1 - row2, col1 - col2

class Antenna():

    def __init__(self, row, col, frequency):

        self.row = row
        self.col = col
        self.frequency = frequency

    def get_coordinates(self):
        return self.row, self.col
    
    def __repr__(self):
        return f"{self.frequency}: ({self.row}, {self.col})"
        
if __name__ == "__main__":

    input_file = input("Input File: ")
    map = parse(input_file)

    map = Map(map)
    antinodes = map.get_antinodes()
    print(f"Number of Antinodes: {len(antinodes)}")

    resonant_antinodes = map.get_resonant_antinodes()
    print(f"Number of Resonant Antinodes: {len(resonant_antinodes)}")