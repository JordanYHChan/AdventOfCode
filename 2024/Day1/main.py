def parse(input):

    list1, list2 = [], []

    for line in open(input, "r"):
        location1, location2 = line.rstrip('\n').split("   ")

        list1.append(int(location1))
        list2.append(int(location2))

    return list1, list2

def get_total_distance(list1, list2):

    list1, list2 = sorted(list1), sorted(list2)
    total_distance = 0

    for location1, location2 in zip(list1, list2):
        total_distance += abs(location1 - location2)

    return total_distance

def get_similarity_score(list1, list2):

    counter1, counter2 = {}, {}
    similarity_score = 0

    for location1 in list1:
        counter1[location1] = counter1.get(location1, 0) + 1

    for location2 in list2:
        counter2[location2] = counter2.get(location2, 0) + 1

    for location1 in counter1.keys():
        similarity_score += location1 * counter1.get(location1, 0) * counter2.get(location1, 0)

    return similarity_score

if __name__ == "__main__":

    input = input("Input File: ")
    list1, list2 = parse(input)
    print(list1, list2)

    total_distance = get_total_distance(list1, list2)
    print(f"Total Distance: {total_distance}")

    similarity_score = get_similarity_score(list1, list2)
    print(f"Similarity Score: {similarity_score}")