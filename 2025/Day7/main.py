def parse(input):

    tachyon_manifold = []

    for line in open(input, 'r'):
        tachyon_manifold.append([cell for cell in line.removesuffix('\n')])

    return tachyon_manifold

class TachyonManifold:

    def __init__(self, tachyon_manifold):

        self.tachyon_manifold = tachyon_manifold
        self.rows = len(self.tachyon_manifold)
        self.columns = len(self.tachyon_manifold[0])
        self.beam_extended = False

    def extend_tachyon_beam(self):

        splits = 0

        row = 1

        while row < self.rows:
            column = 0

            while column < self.columns:
                if self.tachyon_manifold[row - 1][column] in ['.', '^']:
                    column += 1
                    continue

                if self.tachyon_manifold[row-1][column] == 'S':
                    self.tachyon_manifold[row][column] = '1'
                    column += 1
                    continue

                if self.tachyon_manifold[row][column] == '^':
                    self._split_beam(row, column)
                    splits += 1
                    column += 1
                    continue

                if self.tachyon_manifold[row][column] == '.':
                    self.tachyon_manifold[row][column] = self.tachyon_manifold[row-1][column]
                    column += 1
                    continue

                current = int(self.tachyon_manifold[row][column])
                self.tachyon_manifold[row][column] = str(current + int(self.tachyon_manifold[row-1][column]))
                column += 1

            row += 1

        self.beam_extended = True

        return splits

    def get_number_of_timelines(self):

        if not self.beam_extended:
            self.extend_tachyon_beam()

        timelines = 0
        for cell in self.tachyon_manifold[-1]:
            if cell != '.':
                timelines += int(cell)

        return timelines

    def _split_beam(self, row, column):
        previous = int(self.tachyon_manifold[row-1][column])

        if column > 0:
            left = int(self.tachyon_manifold[row][column-1]) if self.tachyon_manifold[row][column-1] != '.' else 0
            self.tachyon_manifold[row][column-1] = str(previous + left)
        
        if column < self.columns - 1:
            right = int(self.tachyon_manifold[row][column+1]) if self.tachyon_manifold[row][column+1] != '.' else 0
            self.tachyon_manifold[row][column+1] = str(previous + right)

    def __repr__(self):
        
        return "\n".join([
            "".join(line) for line in self.tachyon_manifold
        ])

if __name__ == '__main__':

    tachyon_manifold = TachyonManifold(parse(input("Input File: ")))
    print(f"Number of tachyon beam splits: {tachyon_manifold.extend_tachyon_beam()}")
    print(f"Number of timelines: {tachyon_manifold.get_number_of_timelines()}")
