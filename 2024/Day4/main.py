def parse(input):

    word_search = []

    for row in open(input, "r"):
        word_search.append(row.strip("\n"))

    return word_search

class WordSearch():

    def __init__(self, word_search):

        self.word_search = word_search
        self.rows = len(self.word_search)
        self.cols = len(self.word_search[0])

    def get_word_count(self, target="XMAS"):
        
        self.word_count = 0
        length = len(target)

        for row in range(self.rows):
            for col in range(self.cols):

                if self.word_search[row][col] != target[0]:
                    continue

                self.word_count += sum([word == target for word in self.get_words(row, col, length)])

        return self.word_count
    
    def get_words(self, row, col, length):

        return [
            self.get_word(row, col, vertical, horizontal, length)
            for vertical in range(-1, 2)
            for horizontal in range(-1, 2)
        ]

    def get_word(self, row, col, vertical, horizontal, length):

        if vertical == horizontal == 0: return None
        if vertical == 1 and row > self.rows - length: return None
        if vertical == -1 and row < length - 1: return None
        if horizontal == 1 and col > self.cols - length: return None
        if horizontal == -1 and col < length - 1: return None

        return "".join([
            self.word_search[row+vertical*i][col+horizontal*j]
            for i, j in zip(range(length), range(length))
        ])
    
    def get_cross_count(self, target="MAS"):

        self.cross_count = 0
        length = len(target)

        for row in range(self.rows):
            for col in range(self.cols):

                if self.word_search[row][col] != target[length//2]:
                    continue

                self.cross_count += 1 if self.check_cross(row, col, target, length) else 0

        return self.cross_count
    
    def check_cross(self, row, col, target, length):

        length //= 2
        if row < length or row > self.rows - length - 1: return False
        if col < length or col > self.cols - length - 1: return False

        crosses = [
            "".join([
                self.word_search[row+i][col+diagonal*j]
                for i, j in zip(range(-length, length+1), range(-length, length+1))
            ])
            for diagonal in [-1, 1]
        ]

        return all([
            target == crosses[i] or target == crosses[i][::-1]
            for i in range(2)
        ])

if __name__ == "__main__":

    input = input("Input File: ")
    word_search = parse(input)
    print(word_search)

    word_search = WordSearch(word_search)
    XMAS_count = word_search.get_word_count()
    print(f"Number of XMAS: {XMAS_count}")

    X_MAS_count = word_search.get_cross_count()
    print(f"Number of X-MAS: {X_MAS_count}")