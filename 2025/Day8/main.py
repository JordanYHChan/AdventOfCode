def parse(input):

    junction_boxes = []

    for line in open(input, 'r'):
        junction_boxes.append([int(coordinate) for coordinate in line.removesuffix('\n').split(',')])

    return junction_boxes

class JunctionBoxes:

    def __init__(self, junction_boxes):

        self.junction_boxes = junction_boxes
        self.number_of_junction_boxes = len(self.junction_boxes)
        self.distances = self.calculate_distances()
        self.seen = set()
        self.connected_boxes = []

    def connect_boxes(self, number_of_connections=None):

        for _ in range(number_of_connections):
            self._connect_next_two_boxes()

        return sorted(self.connected_boxes, key=lambda x: len(x), reverse=True)

    def connect_all_boxes(self):

        while (
            len(self.connected_boxes[0]) != self.number_of_junction_boxes
        ):
            box1, box2 = self._connect_next_two_boxes()

        return self.junction_boxes[box1], self.junction_boxes[box2]

    def calculate_distances(self):

        distances = [[1_000_000_000_000_000] * self.number_of_junction_boxes for _ in range(self.number_of_junction_boxes)]

        for i, box1 in enumerate(self.junction_boxes):
            for j, box2 in enumerate(self.junction_boxes):
                if i == j:
                    continue

                distances[i][j] = self._calculate_distance(box1, box2)

        return distances

    def _connect_next_two_boxes(self):

        min_distances = [min(distance) for distance in self.distances]
        min_distance = min(min_distances)
        box1 = min_distances.index(min_distance)
        box2 = self.distances[box1].index(min_distance)

        self.distances[box1][box2] = self.distances[box2][box1] = 1_000_000_000_000_000

        box1_seen = box1 in self.seen
        box2_seen = box2 in self.seen

        if box1_seen and box2_seen:
            circuit1 = [box1 in box for box in self.connected_boxes].index(True)
            circuit2 = [box2 in box for box in self.connected_boxes].index(True)
            if circuit1 != circuit2:
                self.connected_boxes[circuit1].extend(self.connected_boxes[circuit2])
                self.connected_boxes.pop(circuit2)
            return box1, box2

        if box1_seen:
            circuit1 = [box1 in box for box in self.connected_boxes].index(True)
            self.connected_boxes[circuit1].append(box2)
            self.seen.add(box2)
            return box1, box2
        
        if box2_seen:
            circuit2 = [box2 in box for box in self.connected_boxes].index(True)
            self.connected_boxes[circuit2].append(box1)
            self.seen.add(box1)
            return box1, box2

        self.connected_boxes.append([box1, box2])
        self.seen.update((box1, box2))
        return box1, box2

    def _calculate_distance(self, box1, box2):

        return (
            (box1[0] - box2[0]) ** 2
            + (box1[1] - box2[1]) ** 2
            + (box1[2] - box2[2]) ** 2
        ) ** 0.5

if __name__ == '__main__':

    junction_boxes = JunctionBoxes(parse(input("Input File: ")))
    size_of_circuits = [len(circuit) for circuit in junction_boxes.connect_boxes(int(input("Number of pairs: ")))]
    print(f"Product of the three largest circuits: {size_of_circuits[0] * size_of_circuits[1] * size_of_circuits[2]}")
    last_box1, last_box2 = junction_boxes.connect_all_boxes()
    print(f"Product of the X coordinates of the last two boxes: {last_box1[0] * last_box2[0]}")
