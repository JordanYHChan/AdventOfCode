def parse(input):

    positions = []
    velocities = []

    for line in open(input, "r"):
        position, velocity = line.strip("\n").split(" ")
        (position_x, position_y), (velocity_x, velocity_y) = position.strip("p=").split(","), velocity.strip("v=").split(",")
        positions.append((int(position_x), int(position_y)))
        velocities.append((int(velocity_x), int(velocity_y)))

    return positions, velocities

class Robots():

    def __init__(self, positions, velocities, map_size):

        self.positions = positions
        self.velocities = velocities
        self.map_x, self.map_y = (int(size) for size in map_size.split(","))

    def safety_factor_after_x_seconds(self, seconds=100):

        return self.calculate_safety_factor(
            self.walk_x_seconds(seconds)
        )

    def calculate_safety_factor(self, positions):

        safety_factor = 1
        for number_of_robots in self.robots_in_each_quadrant(positions):
            safety_factor *= number_of_robots

        return safety_factor

    def robots_in_each_quadrant(self, positions):

        quadrants = [0, 0, 0, 0]

        for position_x, position_y in positions:
            if position_x < self.map_x // 2 and position_y < self.map_y // 2:
                quadrants[0] += 1
            elif position_x < self.map_x // 2 and position_y > self.map_y // 2:
                quadrants[1] += 1
            elif position_x > self.map_x // 2 and position_y < self.map_y // 2:
                quadrants[2] += 1
            elif position_x > self.map_x // 2 and position_y > self.map_y // 2:
                quadrants[3] += 1
            
        return quadrants

    def walk_x_seconds(self, seconds=100):

        return [
            (
                (position_x + seconds * velocity_x) % self.map_x,
                (position_y + seconds * velocity_y) % self.map_y,
            ) for (position_x, position_y), (velocity_x, velocity_y) in zip(
                self.positions, self.velocities
            )
        ]

    def find_easter_egg(self):

        safety_factors = []

        for seconds in range(10000):
            safety_factors.append(self.safety_factor_after_x_seconds(seconds))

        return safety_factors.index(min(safety_factors))

if __name__ == "__main__":

    positions, velocities = parse(input("Input File: "))
    robots = Robots(positions, velocities, input("Map Size: "))
    print(f"Safety Number after 100 seconds: {robots.safety_factor_after_x_seconds()}")
    print(f"Seconds until Easter egg: {robots.find_easter_egg()}")