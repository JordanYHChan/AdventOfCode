def parse(input):

    byte_coordinates = []

    for line in open(input, "r"):
        X, Y = line.strip("\n").split(",")
        byte_coordinates.append((int(X), int(Y)))

    return byte_coordinates

class MemorySpace():

    def __init__(self, byte_coordinates):

        self.byte_coordinates = byte_coordinates
        self.start = (0, 0)
        self.end = (
            max([X for X, _ in self.byte_coordinates]),
            max([Y for _, Y in self.byte_coordinates])
        )
        self.fallen_bytes = set()

    def simulate_bytes(self, bytes):

        self.fallen_bytes = set()

        for byte in range(bytes):
            self.fall_byte(byte)

    def fall_byte(self, byte):

        self.fallen_bytes.add(self.byte_coordinates[byte])

    def find_exit(self):

        self.possible_locations = set([self.start])

        for steps in range(1, self.end[0] * self.end[1]):
            for possible_location in self.possible_locations.copy():
                self.possible_locations.remove(possible_location)
                self.possible_locations.update(self.find_possible_steps(possible_location))
            
            if self.end in self.possible_locations:
                return steps

        return None

    def first_bad_byte(self):

        for time in range(len(self.byte_coordinates), 0, -1):
            self.simulate_bytes(time)
            if self.find_exit() is not None:
                return self.byte_coordinates[time]

    def find_possible_steps(self, position):

        x, y = position

        return [
            (x + i, y + j)
            for i, j in
            [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if (
                0 <= x + i <= self.end[0] and
                0 <= y + j <= self.end[1] and
                (x + i, y + j) not in self.fallen_bytes
            )
        ]

    def __repr__(self):

        memory_space = [
            [
                "#" if (i, j) in self.fallen_bytes else "."
                for i in range(self.end[0] + 1)
            ] for j in range(self.end[1] + 1)
        ]

        return "\n".join(
            ["".join(row) for row in memory_space]
        )

if __name__ == "__main__":

    byte_coordinates = parse(input("Input File: "))
    memory_space = MemorySpace(byte_coordinates)
    bytes_to_simulate = int(input("Bytes to simulate: "))
    memory_space.simulate_bytes(bytes_to_simulate)
    print(f"Minimum number of steps to exit: {memory_space.find_exit()}")
    print(f"First byte to prevent exit: {memory_space.first_bad_byte()}")