def parse(input):

    toilet_papers = []

    for line in open(input, 'r'):
        toilet_papers.append(line.removesuffix('\n'))

    return toilet_papers

class ToiletPaper:

    def __init__(self, toilet_papers):

        self.toilet_papers = set()

        for i, row in enumerate(toilet_papers):
            for j, toilet_paper in enumerate(row):
                if toilet_paper == '@':
                    self.toilet_papers.add((i, j))

    def get_removed_toilet_papers(self):

        removed_toilet_papers = set()

        while True:

            accessible_toilet_papers = self.get_accessible_toilet_papers()
            if len(accessible_toilet_papers) == 0:
                break

            removed_toilet_papers.update(accessible_toilet_papers)
            self.toilet_papers.difference_update(accessible_toilet_papers)

        return removed_toilet_papers

    def get_accessible_toilet_papers(self):

        accessible_toilet_papers = set()

        for toilet_paper in self.toilet_papers:
            counter = 0

            for adjacent_position in self._get_adjacent_positions(toilet_paper):
                if adjacent_position in self.toilet_papers:
                    counter += 1
            
            if counter < 4:
                accessible_toilet_papers.add(toilet_paper)

        return accessible_toilet_papers

    def _get_adjacent_positions(self, toilet_paper):

        row, column = toilet_paper

        return [
            (row + i, column + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
            if not (
                i == 0 and j == 0
            )
        ]

if __name__ == '__main__':

    toilet_papers = ToiletPaper(parse(input("Input File: ")))
    print(f"Number of Accessible Toilet Papers: {len(toilet_papers.get_accessible_toilet_papers())}")
    print(f"Total Number of Toilet Papers Removed: {len(toilet_papers.get_removed_toilet_papers())}")
