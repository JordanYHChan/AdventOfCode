def parse(input):

    conditions = {}
    updates = []

    conditions_finished = False

    for line in open(input, "r"):
        line = line.strip("\n")

        if line == "":
            conditions_finished = True
            continue

        if conditions_finished:
            updates.append([int(page) for page in line.split(",")])
            continue

        X, Y = (int(page) for page in line.split("|"))
        conditions[Y] = conditions.get(Y, []) + [X]

    return conditions, updates

def get_valid_middle_page_sum(conditions, updates):

    valid_middle_page_sum = 0

    for update in updates:
        valid_middle_page_sum += update[len(update)//2] if is_valid(conditions, update) else 0

    return valid_middle_page_sum

def is_valid(conditions, update):

    for i, page in enumerate(update):
        for condition in conditions.get(page, []):
            if condition in update[i:]:
                return False

    return True

def get_corrected_middle_page_sum(conditions, updates):

    corrected_middle_page_sum = 0

    for update in updates:
        corrected_middle_page_sum += 0 if is_valid(conditions, update) else get_corrected_update(conditions, update)[len(update)//2]

    return corrected_middle_page_sum

def get_corrected_update(conditions, update):

    update_conditions = {
        Y: [
            X for X in Xs if X in update
        ] for Y, Xs in conditions.items() if Y in update
    }

    return sorted(update, key=lambda page: len(update_conditions.get(page, [])))

if __name__ == "__main__":

    input = input("Input File: ")
    conditions, updates = parse(input)
    print(conditions)
    print(updates)

    valid_middle_page_sum = get_valid_middle_page_sum(conditions, updates)
    print(f"Valid Middle Page Sum: {valid_middle_page_sum}")

    corrected_middle_page_sum = get_corrected_middle_page_sum(conditions, updates)
    print(f"Corrected Middle Page Sum: {corrected_middle_page_sum}")