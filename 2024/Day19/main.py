def parse(input):

    towels = set()
    designs = []
    towels_finished = False

    for line in open(input, "r"):
        if line == "\n":
            towels_finished = True
            continue

        if towels_finished:
            designs.append(line.strip("\n"))
            continue

        towels.update(line.strip("\n").split(", "))

    return towels, designs

class Onsen():

    def __init__(self, towels, designs):

        self.towels = sorted(towels, key=lambda x: len(x))
        self.designs = designs
        self.possible_designs = {}
    
    def get_number_of_possible_designs(self):

        possible_designs = 0
        possible_ways = 0

        for design in self.designs:
            different_ways = self.design_is_possible(design)
            if different_ways != 0:
                possible_designs += 1
                possible_ways += different_ways

        return possible_designs, possible_ways

    def design_is_possible(self, design):

        if design in self.possible_designs:
            return self.possible_designs[design]

        possible_ways = 0

        if design == "":
            possible_ways += 1

        for towel in self.towels:
            if design.startswith(towel):
                possible_ways += self.design_is_possible(design[len(towel):])
        self.possible_designs[design] = possible_ways

        return possible_ways

if __name__ == "__main__":

    towels, designs = parse(input("Input File: "))
    onsen = Onsen(towels, designs)
    print(f"Number of Possible Designs and Ways: {onsen.get_number_of_possible_designs()}")