def parse(input):

    reports = []

    for report in open(input, "r"):
        reports.append([int(level) for level in report.rstrip('\n').split(" ")])

    return reports

def get_number_of_safe_reports(reports, dampener=False):

    safe_reports = 0
    is_safe_function = is_dampened_safe if dampener else is_safe

    for report in reports:
        safe_reports += 1 if is_safe_function(report) is True else 0

    return safe_reports

def is_safe(report):

    ascending = report[0] < report[-1]
    length = len(report)

    for index in range(length - 1):
        difference = report[index + 1] - report[index]

        if not 1 <= abs(difference) <= 3:
            return index
        
        if difference < 0 and ascending:
            return index
        
        if difference > 0 and not ascending:
            return index

    return True

def is_dampened_safe(report):

    index = is_safe(report)

    if index is True:
        return True
    
    else:
        return check_dampener(report, index)

def check_dampener(report, index):

    first_removed_report = report[:index] + report[index + 1:]
    second_removed_report = report[:index + 1] + report[index + 2:]

    return is_safe(first_removed_report) is True or is_safe(second_removed_report) is True

if __name__ == "__main__":

    input = input("Input File: ")
    reports = parse(input)
    print(reports)

    number_of_safe_reports = get_number_of_safe_reports(reports)
    print(f"Number of Safe Reports: {number_of_safe_reports}")

    number_of_dampened_safe_reports = get_number_of_safe_reports(reports, dampener=True)
    print(f"Number of Dampened Safe Reports: {number_of_dampened_safe_reports}")