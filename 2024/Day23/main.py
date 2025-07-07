from collections import deque

def parse(input):

    network_pairs = []

    for line in open(input, "r"):
        network_pairs.append(set(line.strip("\n").split("-")))

    return network_pairs

class Network():

    def __init__(self, network_pairs):

        self.prepare_network(network_pairs)
        self.prepare_trios()

    def prepare_network(self, network_pairs):

        self.network_mapping = {}

        for network1, network2 in network_pairs:
            self.network_mapping.setdefault(network1, set()).add(network2)
            self.network_mapping.setdefault(network2, set()).add(network1)

    def get_largest_network_password(self):

        self.passwords = set()

        for network in self.network_mapping:
            self.add_network(network, {network})

        return max(self.passwords, key=len)
    
    def add_network(self, network, group):
    
        password = ",".join(sorted(group))
        if password in self.passwords:
            return
    
        self.passwords.add(password)
        for neighbour in self.network_mapping[network]:
            if neighbour in group:
                continue
            if any(
                neighbour not in self.network_mapping[node]
                for node in group
            ):
                continue
            self.add_network(neighbour, {*group, neighbour})

    def prepare_queue(self):

        self.queue = deque()
        seen = set()

        for network1 in self.network_mapping:
            for network2 in self.network_mapping[network1]:
                if (network1, network2) in seen:
                    continue
                seen.add((network2, network1))
                self.queue.append(sorted([network1, network2]))

    def prepare_trios(self):

        self.trios = set()

        for network1 in self.network_mapping:
            for network2 in self.network_mapping[network1]:
                for network3 in self.network_mapping[network2]:
                    if network1 in self.network_mapping[network3]:
                        self.trios.add(tuple(sorted([network1, network2, network3])))

    def trios_with_starting_letter(self, letter="t"):

        count = 0
        for trio in self.trios:
            if any([
                computer.startswith(letter) for computer in trio
            ]):
                count += 1

        return count


if __name__ == "__main__":

    network_pairs = parse(input("Input File: "))
    network = Network(network_pairs)
    print(f"Number of Networks with a computer starting with t: {network.trios_with_starting_letter()}")
    print(f"Largest Network Password: {network.get_largest_network_password()}")
