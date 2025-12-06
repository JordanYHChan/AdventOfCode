def parse(input):

    worksheet = []

    for line in open(input, 'r'):
        worksheet.append(line.removesuffix('\n'))

    return worksheet

class Worksheet:

    def __init__(self, worksheet):

        self.problems, self.operations = self.align_worksheet(worksheet)
        self.problems2 = self.align_worksheet2(worksheet)
        
    def align_worksheet(self, worksheet):

        worksheet = [[
            split for split in line.split(' ') if split != ''
        ] for line in worksheet]

        problems = [[int(number)] for number in worksheet[0]]
        operations = [operation for operation in worksheet[-1]]

        for numbers in worksheet[1:-1]:
            for i, number in enumerate(numbers):
                problems[i].append(int(number))

        return problems, operations

    def align_worksheet2(self, worksheet):

        problems = [number for number in worksheet[0]]
        operations_line = worksheet[-1]

        for row in worksheet[1:-1]:
            for i, number in enumerate(row):
                problems[i] += number

        aligned_problems = []
        for problem, operation in zip(problems, operations_line):
            if operation in ['+', '*']:
                aligned_problems.append([])

            try:
                aligned_problems[-1].append(int(problem))
            except:
                pass

        return aligned_problems

    def get_answers(self, part='1'):

        answers = []
        problems = self.problems if part == '1' else self.problems2

        for problem, operation in zip(problems,self.operations):
            answers.append(self.solve_problem(problem, operation))

        return answers
    
    def solve_problem(self, problem, operation):

        if operation == '+':
            answer = self._sum_operation(problem)

        if operation == '*':
            answer = self._product_operation(problem)

        return answer
    
    def _sum_operation(self, problem):

        answer = 0
        for number in problem:
            answer += number
        
        return answer
    
    def _product_operation(self, problem):

        answer = 1
        for number in problem:
            answer *= number

        return answer

if __name__ == '__main__':

    worksheet = Worksheet(parse(input("Input File: ")))
    print(f"Grand total of answers: {sum(worksheet.get_answers())}")
    print(f"Grand total of answers (part 2): {sum(worksheet.get_answers(part='2'))}")
    