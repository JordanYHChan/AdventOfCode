def parse(input):

    locks_and_keys = [[]]

    for line in open(input, "r"):
        if line == "\n":
            locks_and_keys.append([])
            continue

        locks_and_keys[-1].append(line.strip("\n"))

    return locks_and_keys

class LockAndKeys:

    def __init__(self, locks_and_keys):

        self.prepare_locks_and_keys(locks_and_keys)
        print(self.locks)
        print(self.keys)

    def prepare_locks_and_keys(self, locks_and_keys):

        self.locks = []
        self.keys = []

        for lock_or_key in locks_and_keys:
            self.prepare_lock_or_key(lock_or_key)

    def prepare_lock_or_key(self, lock_or_key):

        if lock_or_key[0] == "#####":
            lock = [0] * 5
            for row in lock_or_key[1:]:
                for i, col in enumerate(row):
                    if col == "#":
                        lock[i] += 1
        
            self.locks.append(lock)
            return

        key = [0] * 5
        for row in lock_or_key[-2::-1]:
            for i, col in enumerate(row):
                if col == "#":
                    key[i] += 1
        
        self.keys.append(key)

    def get_unique_valid_pairs(self):

        self.unqiue_valid_pairs = 0

        for lock in self.locks:
            for key in self.keys:
                self.unqiue_valid_pairs += 1 if self.valid_pair(lock, key) else 0

        return self.unqiue_valid_pairs

    def valid_pair(self, lock, key):

        for lock_height, key_height in zip(lock, key):
            if lock_height + key_height > 5:
                return False
            
        return True

if __name__ == "__main__":

    locks_and_keys = parse(input("Input File: "))
    locks_and_keys = LockAndKeys(locks_and_keys)
    print(f"Unique Valid Pairs: {locks_and_keys.get_unique_valid_pairs()}")