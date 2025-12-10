def parse(input):

    indicator_light_diagrams = []
    button_wiring_schematics = []
    joltage_requirements = []

    for line in open(input, 'r'):
        indicator_light_diagrams.append(line.removesuffix('\n').split(' ')[0])
        button_wiring_schematics.append(line.removesuffix('\n').split(' ')[1:-1])
        joltage_requirements.append(line.removesuffix('\n').split(' ')[-1])

    return indicator_light_diagrams, button_wiring_schematics, joltage_requirements

class FactoryMachines:

    def __init__(self, indicator_light_diagrams, button_wiring_schematics, joltage_requirements):

        self.indicator_light_diagrams = self._prepare_indicator_light_diagrams(indicator_light_diagrams)
        self.button_wiring_schematics = self._prepare_button_wiring_schematics(button_wiring_schematics)
        self.joltage_requirements = self._prepare_joltage_requirements(joltage_requirements)

    def get_joltage_total_presses(self):

        total_presses = 0

        for joltage_requirement, button_wiring_schematic in zip(self.joltage_requirements, self.button_wiring_schematics):
            total_presses += self._get_joltage_fewest_presses(joltage_requirement, button_wiring_schematic)

        return total_presses

    def get_light_total_presses(self):

        total_presses = 0

        for indicator_light_diagram, button_wiring_schematic in zip(self.indicator_light_diagrams, self.button_wiring_schematics):
            total_presses += self._get_light_fewest_presses(indicator_light_diagram, button_wiring_schematic)

        return total_presses

    def _get_joltage_fewest_presses(self, joltage_requirement, button_wiring_schematic):

        configurations = [[0] * len(joltage_requirement)]
        presses = 0
        found = False

        return presses

    def _get_light_fewest_presses(self, indicator_light_diagram, button_wiring_schematic):

        configurations = set(tuple(sorted(light)) for light in button_wiring_schematic)
        seen = set(configuration for configuration in configurations)
        presses = 0
        found = False

        while not found:
            new_configurations = set()
            for configuration in configurations:
                if indicator_light_diagram == configuration:
                    found = True

                for buttons in button_wiring_schematic:
                    new_configuration = tuple(sorted(set(configuration).symmetric_difference(buttons)))

                    if new_configuration in seen:
                        continue

                    new_configurations.add(new_configuration)
                    seen.add(new_configuration)
            configurations = new_configurations
            presses += 1

        return presses

    def _prepare_indicator_light_diagrams(self, indicator_light_diagrams):

        return [
            tuple([
                i
                for i, light in enumerate(indicator_light_diagram[1:-1])
                if light == '#'
            ]) for indicator_light_diagram in indicator_light_diagrams
        ]
    
    def _prepare_button_wiring_schematics(self, button_wiring_schematics):

        return [
            [
                set([
                    int(button) for button in listed_button[1:-1].split(',')
                ]) for listed_button in button_wiring_schematic
            ] for button_wiring_schematic in button_wiring_schematics
        ]

    def _prepare_joltage_requirements(self, joltage_requirements):

        return [
            [int(joltage) for joltage in listed_joltage[1:-1].split(',')]
            for listed_joltage in joltage_requirements
        ]

if __name__ == '__main__':

    factory_machines = FactoryMachines(*parse(input("Input File: ")))
    print(f"Total fewest light button presses required: {factory_machines.get_light_total_presses()}")
    print(f"Total fewest joltage button presses required: {factory_machines.get_joltage_total_presses()}")
