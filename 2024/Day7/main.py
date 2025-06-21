def parse(input):

    equations = []

    for line in open(input, "r"):
        value, numbers = line.strip("\n").split(": ")
        equations.append([int(value), [int(number) for number in numbers.split(" ")]])

    return equations

def calculate_total_calibration_result(equations, modified=False):

    return sum(
        [
            calculate_calibration_result(value, number, modified)
            for value, number in equations
        ]
    )

def calculate_calibration_result(value, numbers, modified=False):

    if possible(value, numbers, modified):
        return value

    return 0

def possible(value, numbers, modified=False):

    if modified:
        iterate_operators = part_two_iterate_operators
    else:
        iterate_operators = part_one_iterate_operators

    operators = ["+" for _ in range(len(numbers) - 1)]
    
    while True:
        test = perform_operation(numbers, operators)

        if test == value:
            return True
        
        operators = iterate_operators(operators)

        if operators is None:
            break
        
    return False

def perform_operation(numbers, operators):

    result = numbers[0]

    for number, operator in zip(numbers[1:], operators):
        if operator == "+":
            result += number
        elif operator == "*":
            result *= number
        elif operator == "||":
            result = int(str(result)+str(number))
        else:
            raise ValueError(f"Invalid operator: {operator}")

    return result

def part_two_iterate_operators(operators):

    for i, operator in enumerate(operators):
        if operator == "+":
            return ["+"]  * i + ["*"] + operators[i+1:]
        if operator == "*":
            return ["+"] * i + ["||"] + operators[i+1:]

    return None

def part_one_iterate_operators(operators):

    for i, operator in enumerate(operators):
        if operator == "+":
            return ["+"] * i + ["*"] + operators[i+1:]
        
    return None

if __name__ == "__main__":

    input_file = input("Input File: ")
    equations = parse(input_file)

    total_calibration_result = calculate_total_calibration_result(equations)
    print(f"Total Calibration Result: {total_calibration_result}")

    modified_calibration_result = calculate_total_calibration_result(equations, modified=True)
    print(f"Modified Total Calibration Result: {modified_calibration_result}")