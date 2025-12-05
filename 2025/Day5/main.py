def parse(input):

    fresh_ingredient_ranges = []
    fresh_ingredient_ranges_finished = False
    available_ingredients = []

    for line in open(input, 'r'):
        if line == '\n':
            fresh_ingredient_ranges_finished = True
            continue

        if fresh_ingredient_ranges_finished:
            available_ingredients.append(int(line.removesuffix('\n')))
            continue

        start, stop = line.removesuffix('\n').split('-')
        fresh_ingredient_ranges.append([int(start), int(stop)])


    return fresh_ingredient_ranges, available_ingredients

class Ingredients:

    def __init__(self, fresh_ingredient_ranges, available_ingredients):

        self.fresh_ingredient_ranges = self.simplify_fresh_ingredient_ranges(fresh_ingredient_ranges)
        self.available_ingredients = available_ingredients
        
    def get_available_fresh_ingredients(self):

        self.available_fresh_ingredients = []

        for available_ingredient in self.available_ingredients:
            for start, stop in self.fresh_ingredient_ranges:
                if start > available_ingredient:
                    continue

                if stop < available_ingredient:
                    continue

                self.available_fresh_ingredients.append(available_ingredient)
                break

        return self.available_fresh_ingredients

    def simplify_fresh_ingredient_ranges(self, fresh_ingredient_ranges):

        fresh_ingredient_ranges = sorted(fresh_ingredient_ranges)
        simplified_fresh_ingredient_ranges = [fresh_ingredient_ranges[0]]

        for start, stop in fresh_ingredient_ranges[1:]:
            if start <= simplified_fresh_ingredient_ranges[-1][1]:
                simplified_fresh_ingredient_ranges[-1][1] = max(
                    simplified_fresh_ingredient_ranges[-1][1], stop
                )
                continue

            simplified_fresh_ingredient_ranges.append([start, stop])

        return simplified_fresh_ingredient_ranges

    def get_number_of_fresh_ingredients(self):

        self.number_of_fresh_ingredients = 0

        for start, stop in self.fresh_ingredient_ranges:
            self.number_of_fresh_ingredients += stop - start + 1

        return self.number_of_fresh_ingredients

if __name__ == '__main__':

    fresh_ingredient_ranges, available_ingredients = parse(input("Input File: "))
    ingredients = Ingredients(fresh_ingredient_ranges, available_ingredients)
    print(f"Number of available fresh ingredients: {len(ingredients.get_available_fresh_ingredients())}")
    print(f"Number of fresh ingredients: {ingredients.get_number_of_fresh_ingredients()}")
