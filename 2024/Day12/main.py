def parse(input):

    garden = []

    for line in open(input, "r"):
        garden.append(line.strip("\n"))

    return garden

class Garden():
    
    def __init__(self, garden):

        self.prepare_garden(garden)
        self.sweep_garden()

    def prepare_garden(self, garden):

        self.garden = {}

        for i, row in enumerate(garden):
            for j, label in enumerate(row):

                self.garden[i, j] = label
    
    def sweep_garden(self):

        self.regions = []

        seen = set()
        for plot in self.garden:
            if plot in seen:
                continue

            region = set([plot])
            region = self.crawl_region(region, self.garden[plot])

            seen |= region
            self.regions.append(region)

    def crawl_region(self, region, label):

        new_plots = set(
            side_neighbour
            for side_neighbour in self.get_region_perimeter_side_neighbours(region)
            if self.garden.get(side_neighbour) == label
        )

        if len(new_plots) == 0:
            return region
        
        region |= new_plots
        return self.crawl_region(region, label)
    
    def get_region_perimeter_length(self, region):

        return len(self.get_region_perimeter_side_neighbours(region))

    def get_region_perimeter_corners(self, region):

        corners = 0

        for plot in region:
            for corner, sides in self.get_plot_corner_side_neighbours_mapping(plot).items():
                if all([side not in region for side in sides]):
                    corners += 1
                    continue
                
                if corner in region:
                    continue

                if all([side in region for side in sides]):
                    corners += 1
                    continue


        return corners

    def get_region_perimeter_corner_neighbours(self, region):

        return [
            neighbour
            for plot in region
            for neighbour in self.get_plot_corner_neighbours(plot)
            if neighbour not in region
        ]

    def get_region_perimeter_side_neighbours(self, region):

        return [
            neighbour
            for plot in region
            for neighbour in self.get_plot_side_neighbours(plot)
            if neighbour not in region
        ]
    
    def get_plot_corner_side_neighbours_mapping(self, plot):

        corners = self.get_plot_corner_neighbours(plot)
        sides = self.get_plot_side_neighbours(plot)

        return {
            corner: [
                side for side in self.get_plot_side_neighbours(corner) if side in sides
            ] for corner in corners
        }

    def get_plot_corner_neighbours(self, plot):

        return [
            (plot[0] + i, plot[1] + j)
            for i, j in
            [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        ]

    def get_plot_side_neighbours(self, plot):

        return [
            (plot[0] + i, plot[1] + j)
            for i, j in
            [(-1, 0), (0, 1), (1, 0), (0, -1)]
        ]
    
    def get_total_price(self, discounted=False):

        total_price = 0

        for region in self.regions:
            total_price += len(region) * (
                self.get_region_perimeter_corners(region)
                if discounted else
                self.get_region_perimeter_length(region)
            )

        return total_price    

if __name__ == "__main__":

    garden = parse(input("Input File: "))
    garden = Garden(garden)
    print(f"Total Price of Fences: {garden.get_total_price()}")
    print(f"Total Discounted Price of Fences: {garden.get_total_price(discounted=True)}")