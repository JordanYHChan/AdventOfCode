def parse(input):

    stones = []

    for line in open(input, "r"):
        for stone in line.strip("\n").split(" "):
            stones.append(stone)

    return stones

class Stones():

    def __init__(self, stones):

        self.prepare_stones(stones)
        self.stone_blink_map = {
            "0" : ["1"],
        }

    def prepare_stones(self, stones):

        self.stones = {}
        for stone in stones:
            self.stones[stone] = self.stones.get(stone, 0) + 1

    def blink_stones_n_times(self, number_of_blinks):

        for _ in range(number_of_blinks):
            self.blink_stones()

    def blink_stones(self):

        stones = {
            stone: count
            for stone, count in self.stones.items()
        }
        self.stones = {}

        for stone, count in stones.items():
            blinked_stones = self.blink(stone)
            for blinked_stone in blinked_stones:
                self.stones[blinked_stone] = self.stones.get(blinked_stone, 0) + count

    def reset_stone(self, stone):
        return self.stones.pop(stone)

    def blink(self, stone):

        if stone in self.stone_blink_map.keys():
            return self.stone_blink_map[stone]
        
        length = len(stone)

        if length % 2 == 0:
            new_stones = (stone[:length//2], str(int(stone[length//2:])))
            self.stone_blink_map[stone] = new_stones
            return new_stones

        new_stone = str(2024 * int(stone))
        self.stone_blink_map[stone] = [new_stone]
        return [new_stone]
    
    def __len__(self):
        return sum(list(self.stones.values()))

if __name__ == "__main__":

    input_file = input("Input File: ")
    stones = parse(input_file)
    print(stones)

    stones = Stones(stones)
    number_of_blinks = int(input("Number of blinks: "))
    stones.blink_stones_n_times(number_of_blinks)
    print(f"Number of Stones after {number_of_blinks} Blinks: {len(stones)}")
