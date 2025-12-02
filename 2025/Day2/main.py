def parse(input):

    id_ranges = []

    for line in open(input, 'r'):
        for id_range in line.split(","):
            id_range_start, id_range_end = id_range.split("-")
            id_ranges.append((int(id_range_start), int(id_range_end)))

    return id_ranges

class IDValidator:

    def __init__(self, id_ranges):

        self.id_ranges = id_ranges
        self.single_invalid_ids = []
        self.repeated_invalid_ids = []

    def get_invalid_ids(self):

        for start, end in self.id_ranges:
            for id in range(start, end+1):
                id_string = str(id)

                if self.is_single_invalid(id_string):
                    self.single_invalid_ids.append(id)
                    continue

                if self.is_repeated_invalid(id_string):
                    self.repeated_invalid_ids.append(id)
                    continue

        return self.single_invalid_ids, self.repeated_invalid_ids

    def is_single_invalid(self, id_string):

        length = len(id_string)

        if id_string[:length//2] == id_string[length//2:]:
            return True

        return False

    def is_repeated_invalid(self, id_string):

        length = len(id_string)

        for i in range(3, length+1):
            if length % i != 0:
                continue

            length_ = length // i

            if len(set(id_string[length_ * n:length_ * (n+1)] for n in range(i))) == 1:
                return True
        
        return False

if __name__ == '__main__':

    id_ranges = parse(input("Input File: "))
    id_validator = IDValidator(id_ranges)
    single_invalid_ids, repeated_invalid_ids = id_validator.get_invalid_ids()
    print(f"Sum of all single invalid IDs: {sum(single_invalid_ids)}")
    print(f"Sum of all repeated invalid IDs: {sum(single_invalid_ids) + sum(repeated_invalid_ids)}")
