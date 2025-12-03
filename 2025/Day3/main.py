def parse(input):

    batteries = []

    for line in open(input, 'r'):
        batteries.append(line.removesuffix('\n'))

    return batteries

class Batteries:

    def __init__(self, batteries):

        self.batteries = batteries

    def get_maximum_joltages(self, digits=2):

        maxmimum_joltages = []

        for battery in self.batteries:
            maxmimum_joltages.append(self._get_maximum_joltage(battery, digits))

        return maxmimum_joltages

    def _get_maximum_joltage(self, battery, digits):
        
        maximum_jolgate = ''
        
        while digits > 0:

            for number in [f'{i}' for i in range(9, 0, -1)]:
                if number not in battery:
                    continue

                index = battery.index(number)

                if index > len(battery) - digits:
                    continue

                maximum_jolgate += number
                battery = battery[index+1:]
                digits -= 1
                break

        return int(maximum_jolgate)

if __name__ == '__main__':

    batteries = Batteries(parse(input("Input File: ")))
    print(f"Total 2 battery output joltage: {sum(batteries.get_maximum_joltages(2))}")
    print(f"Total 12 battery output joltage: {sum(batteries.get_maximum_joltages(12))}")
