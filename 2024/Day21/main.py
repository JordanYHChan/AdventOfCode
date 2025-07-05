def parse(input):

    codes = []

    for line in open(input, "r"):
        codes.append(line.strip("\n"))

    return codes

class Keypad():

    def __init__(self):

        self.cache = {}
        self.prepare_buttons_mapping()

    def get_code_complexities(self, codes, depth):

        complexities = 0

        for code in codes:
            complexities += self.get_code_complexity(code, depth)

        return complexities
    
    def get_code_complexity(self, code, depth):

        return int(code.strip("A")) * self.get_sequence_length(code, depth)
    
    def get_sequence_length(self, code, depth):

        length = 0
        for subcode in self.get_subcodes(code):
            length += self.get_subsequence_length(subcode, depth)

        return length

    def get_subsequence_length(self, subcode, depth):

        if (subcode, depth) in self.cache:
            return self.cache[subcode, depth]
        
        if depth == 1:
            length = len(self.buttons_mapping[subcode])
            self.cache[subcode, depth] = length
            return length
        
        length = 0
        for subsequence in self.get_subcodes(self.buttons_mapping[subcode]):
            length += self.get_subsequence_length(subsequence, depth - 1)

        self.cache[subcode, depth] = length
        return length

    def get_subcodes(self, code):

        return [
            start + end
            for start, end in zip(
                "A" + code[:-1], code
            )
        ]

    def prepare_buttons_mapping(self):

        self.buttons_mapping = {}

        self.prepare_button_sequences({
            "A": (3, 2),
            "0": (3, 1),
            "1": (2, 0),
            "2": (2, 1),
            "3": (2, 2),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "7": (0, 0),
            "8": (0, 1),
            "9": (0, 2),
        })

        self.prepare_button_sequences({
            "A": (0, 2),
            "^": (0, 1),
            "<": (1, 0),
            "v": (1, 1),
            ">": (1, 2),
        })

    def prepare_button_sequences(self, buttons):

        for start in buttons:
            for end in buttons:
                self.buttons_mapping[start+end] = self.get_button_sequence(
                    buttons, start, end
                )

    def get_button_sequence(self, buttons, start, end):

        start_row, start_col = buttons[start]
        end_row, end_col = buttons[end]
        rows = end_row - start_row
        cols = end_col - start_col

        if start in "147" and end in "0A":
            return ">" * cols + "v" * rows + "A"
        
        if start in "0A" and end in "147":
            return "^" * -rows + "<" * -cols + "A"
        
        if start in "<" and end in "^A":
            return ">" * cols + "^" * -rows + "A"
            
        if start in "^A" and end in "<":
            return "v" * rows + "<" * -cols + "A"

        return (
            "<" * -cols if cols < 0 else ""
        ) + (
            "v" * rows if rows > 0 else "^" * - rows
        ) + (
            ">" * cols if cols > 0 else ""
        ) + "A"

if __name__ == "__main__":

    codes = parse(input("Input File: "))
    keypad = Keypad()
    depth = int(input("Depth of Keypads: "))
    print(f"Sum of Code Complexities: {keypad.get_code_complexities(codes, depth)}")