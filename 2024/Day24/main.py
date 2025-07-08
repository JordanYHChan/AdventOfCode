def parse(input):

    initial_wires = []
    gate_connections = []
    finished_wires = False

    for line in open(input, "r"):
        if line == "\n":
            finished_wires = True
            continue

        if finished_wires:
            gate_connections.append(line.strip("\n").split(" "))
            continue

        initial_wires.append(line.strip("\n").split(": "))

    return initial_wires, gate_connections

class Wires:

    def __init__(self, initial_wires, gate_connections):

        self.gate_map = {
            "AND": self.AND,
            "OR": self.OR,
            "XOR": self.XOR,
        }

        self.prepare_wires(initial_wires, gate_connections)
        self.x = self.get_wires_number("x")
        self.y = self.get_wires_number("y")
        self.target_z = self.x + self.y

    def prepare_wires(self, initial_wires, gate_connections):

        self.wires = {}
        self.initial_xs = []
        self.initial_ys = []
        self.bits = 0

        for wire, value in initial_wires:
            if wire[0] == "x":
                self.initial_xs.append(int(value))
            if wire[0] == "y":
                self.initial_ys.append(int(value))


            self.wires[wire] = {
                "wire": wire,
                "value": value,
                "wire1": None,
                "wire2": None,
                "gate": None,
                "connections": set()
            }

        for wire1, gate, wire2, _, wire in gate_connections:
            if wire[0] == "z":
                self.bits += 1
                
            self.wires[wire] = {
                "wire": wire,
                "wire1": wire1,
                "wire2": wire2,
                "gate": gate,
                "connections": set([wire1, wire2]),
            }

    def fix_bits(self):

        self.wires_to_swap = []

        for n in range(self.bits - 1):
            if self.check_nth_bit(n):
                continue
            self.wires_to_swap.extend(self.fix_nth_bit(n))
        
        return self.wires_to_swap

    def check_nth_bit(self, n):

        for x in range(2):
            for y in range(2):
                for carry in range(2):
                    initial_xs = [0] * (self.bits - 1 - n) + [x]
                    initial_ys = [0] * (self.bits - 1 - n) + [y]
                    if n > 0:
                        initial_xs += [carry] + [0] * (n - 1)
                        initial_ys += [carry] + [0] * (n - 1)
                    elif carry > 0:
                        continue
                    initial_xs, initial_ys = list(reversed(initial_xs)), list(reversed(initial_ys))
                    nth_z = self.get_wire_value(f"z{n:02d}", initial_xs, initial_ys)
                    if nth_z != (x + y + carry) % 2:
                        return False
        return True

    def fix_nth_bit(self, n):
        previous_AND = self.find_wire("AND", f"x{n-1:02d}", f"y{n-1:02d}")
        previous_XOR =  self.find_wire("XOR", f"x{n-1:02d}", f"y{n-1:02d}")
        current_XOR = self.find_wire("XOR", f"x{n:02d}", f"y{n:02d}")
        next_AND = self.find_wire("AND", previous_XOR)
        next_OR = self.find_wire("OR", next_AND, previous_AND)
        nth_z = self.find_wire("XOR", current_XOR, next_OR)

        if nth_z is None:
            nth_z = f"z{n:02d}"
            swap = list(set(
                [self.wires[nth_z]["wire1"], self.wires[nth_z]["wire2"]]
            ) ^ set(
                [self.wires[current_XOR]["wire"], self.wires[next_OR]["wire"]]
            ))
        if nth_z != f"z{n:02d}":
            swap = [self.wires[nth_z]["wire"], f"z{n:02d}"]
        self.swap_wires(*swap)
        return swap

    def swap_wires(self, wire1, wire2):
        self.wires[wire1], self.wires[wire2] = self.wires[wire2], self.wires[wire1]

    def find_wire(self, gate=None, wire1=None, wire2=None):
        for wire in self.wires.values():
            if gate and gate != wire["gate"]:
                continue
            if wire1 and wire1 not in [wire["wire1"], wire["wire2"]]:
                continue
            if wire2 and wire2 not in [wire["wire1"], wire["wire2"]]:
                continue
            return wire["wire"]

    def get_wires_number(self, start="z"):

        wires = sorted([wire for wire in self.wires if wire[0] == start], reverse=True)

        number = ""

        for wire in wires:
            number += str(self.get_wire_value(wire))

        return int(number, 2)

    def get_wire_value(self, wire, initial_xs=None, initial_ys=None):

        if initial_xs is None:
            initial_xs = self.initial_xs
        if initial_ys is None:
            initial_ys = self.initial_ys
        
        if wire[0] == "x":
            return initial_xs[int(wire[1:])]
        if wire[0] == "y":
            return initial_ys[int(wire[1:])]
        
        value = self.wires[wire]

        wire1, wire2, gate, connections = value["wire1"], value["wire2"], value["gate"], value["connections"]
        value1 = self.get_wire_value(wire1, initial_xs, initial_ys)
        value2 = self.get_wire_value(wire2, initial_xs, initial_ys)
        gate = self.gate_map[gate]
        connections |= self.wires[wire1]["connections"] | self.wires[wire2]["connections"]

        return gate(value1, value2)

    def AND(self, value1, value2):

        return value1 & value2
    
    def OR(self, value1, value2):

        return value1 | value2

    def XOR(self,value1, value2):

        return value1 ^ value2

if __name__ == "__main__":

    initial_wires, gate_connections = parse(input("Input File: "))
    wires = Wires(initial_wires, gate_connections)
    print(f"Z wires number: {wires.get_wires_number()}")
    print(f"Wires to swap: {','.join(sorted(wires.fix_bits()))}")
