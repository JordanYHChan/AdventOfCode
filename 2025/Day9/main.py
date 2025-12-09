def parse(input):

    red_tiles = []

    for line in open(input, 'r'):
        red_tiles.append([int(coordinate) for coordinate in line.removesuffix('\n').split(',')])

    return red_tiles

class MovieTheatre:

    def __init__(self, red_tiles):

        self.red_tiles = red_tiles
        self.number_of_red_tiles = len(self.red_tiles)
        self.green_tiles = self.get_green_tiles()

    def get_maximum_rectangle(self, valid=False):

        rectangles = self.calculate_rectangles(valid)
        maximum_rectangle = max([max(rectangle) for rectangle in rectangles])

        return maximum_rectangle

    def calculate_rectangles(self, valid=False):

        rectangles = [[1] * self.number_of_red_tiles for _ in range(self.number_of_red_tiles)]

        for i, tile1 in enumerate(self.red_tiles):
            for j, tile2 in enumerate(self.red_tiles):
                if i == j:
                    continue

                if not valid:
                    rectangles[i][j] = self._calculate_rectangle(tile1, tile2)
                    continue

                if self._is_valid_rectangle(tile1, tile2):
                    rectangles[i][j] = self._calculate_rectangle(tile1, tile2)

        return rectangles

    def get_green_tiles(self):

        green_tiles = []

        for tile1, tile2 in zip(self.red_tiles, self.red_tiles[1:] + [self.red_tiles[0]]):
            green_tiles.append(tile1)
            green_tiles.append([(tile1[0] + tile2[0]) / 2, (tile1[1] + tile2[1]) / 2])

        return green_tiles

    def _is_valid_rectangle(self, tile1, tile2):

        min_row, max_row = min(tile1[0], tile2[0]), max(tile1[0], tile2[0])
        min_col, max_col = min(tile1[1], tile2[1]), max(tile1[1], tile2[1])

        for row, col in self.green_tiles:
            if min_row < row < max_row and min_col < col < max_col:
                return False
            
        return True

    def _calculate_rectangle(self, tile1, tile2):

        return (
            abs(tile1[0] - tile2[0]) + 1
        ) * (
            abs(tile1[1] - tile2[1]) + 1
        )

if __name__ == '__main__':

    movie_theatre = MovieTheatre(parse(input("Input File: ")))
    print(f"Largest area of any rectangle: {movie_theatre.get_maximum_rectangle()}")
    print(f"Largest area of valid rectangles: {movie_theatre.get_maximum_rectangle(valid=True)}")
