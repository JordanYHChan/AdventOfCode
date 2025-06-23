def parse(input):

    disk_map = ""

    for line in open(input, "r"):
        disk_map += line.strip("\n")

    return disk_map

class DiskMap():

    def __init__(self, disk_map):

        self.disk_map = disk_map
        self.prepare_disk_map()
        self.prepare_disk()
        self.rearrange_disk()
        self.rearrange_modified_disk()

    def prepare_disk_map(self):

        self.disk_map = [
            int(count) for count in self.disk_map
        ]

    def prepare_disk(self):

        self.disk = []
        files = True
        ID_number = 0

        for count in self.disk_map:
            self.disk += [
                ID_number if files else "."
            ] * count

            if files:
                ID_number += 1
            
            files = not files

    def rearrange_disk(self):

        self.rearranged_disk = [file for file in self.disk]
        disk_length = len(self.rearranged_disk)
        left, right = 0, disk_length - 1

        while left < right:

            if self.rearranged_disk[left] != ".":
                left += 1
                continue

            if self.rearranged_disk[right] == ".":
                right -= 1
                continue

            self.rearranged_disk[left], self.rearranged_disk[right] = self.rearranged_disk[right], self.rearranged_disk[left]

    def rearrange_modified_disk(self):

        self.rearranged_modified_disk = [file for file in self.disk]
        disk_length = len(self.rearranged_modified_disk)
        file_block_left = file_block_right = disk_length

        for file_block_length, empty_block_length in zip(
            self.disk_map[::-2],
            self.disk_map[-2::-2],
        ):

            file_block_left = file_block_right - file_block_length

            for empty_block_left, empty_block_right in self.get_empty_block_left_rights(self.rearranged_modified_disk):
                if file_block_length > empty_block_right - empty_block_left:
                    continue

                if file_block_left < empty_block_left:
                    break

                (
                    self.rearranged_modified_disk[empty_block_left:empty_block_left+file_block_length],
                    self.rearranged_modified_disk[file_block_left:file_block_right],
                ) = (
                    self.rearranged_modified_disk[file_block_left:file_block_right],
                    self.rearranged_modified_disk[empty_block_left:empty_block_left+file_block_length],
                )
                break

            file_block_right = file_block_left - empty_block_length

    def get_empty_block_left_rights(self, disk):

        empty_block_left_rights = []
        empty_block_start = None

        for index, file in enumerate(disk):
            if file == ".":
                empty_block_start = index if empty_block_start is None else empty_block_start
                continue

            if empty_block_start is not None:
                empty_block_left_rights.append((empty_block_start, index))
                empty_block_start = None

        return empty_block_left_rights

    def prepare_filesystem_checksum(self, modified=False):

        self.filesystem_checksum = 0
        disk = self.rearranged_modified_disk if modified else self.rearranged_disk

        for index, file in enumerate(disk):
            if file == ".":
                continue

            self.filesystem_checksum += index * file

    def get_filesystem_checksum(self, modified=False):

        self.prepare_filesystem_checksum(modified)

        return self.filesystem_checksum

    def __repr__(self):
        return f"{self.disk_map}"

if __name__ == "__main__":

    input_file = input("Input File: ")
    disk_map = parse(input_file)
    disk_map = DiskMap(disk_map)

    filesystem_checksum = disk_map.get_filesystem_checksum()
    print(f"Filesystem Checksum: {filesystem_checksum}")

    modified_filesystem_checksum = disk_map.get_filesystem_checksum(modified=True)
    print(f"Modified Filesystem Checksum: {modified_filesystem_checksum}")