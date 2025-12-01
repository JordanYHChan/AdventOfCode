def parse(input):

    rotation_sequence = []

    for line in open(input, 'r'):
        rotation_sequence.append((line[0], int(line[1:])))

    return rotation_sequence

class Dial:

    def __init__(self, rotation_sequence, position_start=50, numbers=100):

        self.position = position_start
        self.numbers = numbers
        self.rotation_sequence = rotation_sequence

        self.password = 0
        self.secure_password = 0

    def find_passwords(self):

        for direction, rotations in self.rotation_sequence:
            self.direction, self.rotations = direction, rotations

            self.remove_full_rotations()
            self.rotate_dial()

        return self.password, self.secure_password

    def remove_full_rotations(self):
        
        full_rotations = self.rotations // self.numbers
        self.secure_password += full_rotations
        self.rotations -= full_rotations * self.numbers
        
    def rotate_dial(self):

        if self.direction == 'L':
            new_position = self.position - self.rotations
        else:
            new_position = self.position + self.rotations
    
        if self.position != 0 and not 0 < new_position < 100:
            self.secure_password += 1

        self.position = new_position % self.numbers

        if self.position == 0:
            self.password += 1
    
if __name__ == '__main__':

    rotation_sequence = parse(input("Input File: "))
    dial = Dial(rotation_sequence)
    password, secure_password = dial.find_passwords()
    print(f"Password: {password}")
    print(f"Secure Password: {secure_password}")
