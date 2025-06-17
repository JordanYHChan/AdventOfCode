def parse(input):

    program = ""

    for line in open(input, "r"):
        program += line

    return program

def run_program(program):

    result = 0

    for start_split in program.split("mul("):
        for end_split in start_split.split(")"):
            ints = end_split.split(",")

            if len(ints) != 2:
                continue

            try:
                result += int(ints[0]) * int(ints[1])

            except:
                continue

    return result

def run_conditional_program(program):

    result = 0

    for start_split in program.split("do()"):
        enabled = start_split.split("don't()")[0]
        result += run_program(enabled)

    return result

if __name__ == "__main__":

    input = input("Input File: ")
    program = parse(input)
    print(program)

    result = run_program(program)
    print(f"Results: {result}")

    conditional_result = run_conditional_program(program)
    print(f"Conditional Results: {conditional_result}")