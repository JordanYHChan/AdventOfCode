def parse(input):

    A = B = C = program = None

    for line in open(input, "r"):
        if line == "\n":
            continue

        key, value = line.strip("\n").split(": ")

        match key:
            case "Register A":
                A = int(value)
            case "Register B": 
                B = int(value)
            case "Register C":
                C = int(value)
            case "Program":
                program = [int(opcode) for opcode in value.split(",")]

    return A, B, C, program

class Computer():

    def __init__(self, A, B, C, program):

        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.program_length = len(self.program)
    
    def run_program(self):

        self.pointer = 0
        self.output = []

        while self.pointer + 1 < self.program_length:

            opcode, operand = self.program[self.pointer : self.pointer + 2]
            instruction = self.get_instruction(opcode)
            instruction(operand)

            if opcode != 3:
                self.iter_pointer()

    def find_smallest_A(self):

        self.possible_As = {0}

        for i in range(self.program_length):
            expected_instruction = self.program[-(i+1):]

            for A in self.possible_As.copy():
                self.possible_As.remove(A)

                A *= 8

                for modifier in range(8):
                    self.reset_A(A + modifier)
                    self.run_program()

                    if self.output == expected_instruction:
                        self.possible_As.add(A + modifier)

        return min(self.possible_As)

    def reset_A(self, A):
        self.A = A
        self.B = B
        self.C = C

    def iter_pointer(self):

        self.pointer += 2

    def adv(self, operand):
        
        self.A = self._dv(operand)

    def bxl(self, operand):
    
        self.B ^= operand

    def bst(self, operand):
        
        self.B = self.get_combo_operand(operand) % 8

    def jnz(self, operand):
        
        if self.A == 0:
            self.iter_pointer()
        else:
            self.pointer = operand

    def bxc(self, operand):
        
        self.B ^= self.C

    def out(self, operand):
        
        self.output.append(self.get_combo_operand(operand) % 8)

    def bdv(self, operand):
        
        self.B = self._dv(operand)

    def cdv(self, operand):
        
        self.C = self._dv(operand)

    def _dv(self, operand):

        return self.A // (2 ** self.get_combo_operand(operand))

    def get_combo_operand(self, operand):
        match operand:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C

    def get_instruction(self, opcode):
        match opcode:
            case 0:
                return self.adv
            case 1:
                return self.bxl
            case 2:
                return self.bst
            case 3:
                return self.jnz
            case 4:
                return self.bxc
            case 5:
                return self.out
            case 6:
                return self.bdv
            case 7:
                return self.cdv

    def get_output(self):

        return ",".join(str(out) for out in self.output)

if __name__ == "__main__":

    A, B, C, program = parse(input("Input File: "))
    computer = Computer(A, B, C, program)
    computer.run_program()
    print(f"Computer output: {computer.get_output()}")
    print(f"Smallest initial A to copy input: {computer.find_smallest_A()}")