def parse(input):

    initial_secret_numbers = []

    for line in open(input, "r"):
        initial_secret_numbers.append(int(line.strip("\n")))

    return initial_secret_numbers

class SecretNumbers():

    def __init__(self, initial_secret_numbers):

        self.initial_secret_numbers = initial_secret_numbers
        self.cache = {}
        self.best_sequence = None
        self.best_price = 0

    def get_best_sequence_and_price(self):

        return self.best_sequence, self.best_price

    def evolve_secret_numbers_days(self, days=2000):

        secret_numbers = []

        for secret_number in self.initial_secret_numbers:
            secret_numbers.append(self.evolve_secret_number_days(secret_number, days))

        return secret_numbers

    def evolve_secret_number_days(self, secret_number, days=2000):

        self.seen = set()
        self.changes = []

        for _ in range(days):
            new_secret_number = self.evolve_secret_number(secret_number)
            self.check_sequence(secret_number, new_secret_number)

            secret_number = new_secret_number

        return secret_number

    def check_sequence(self, old_secret_number, new_secret_number):

        old_price = int(str(old_secret_number)[-1])
        new_price = int(str(new_secret_number)[-1])

        self.changes.append(new_price - old_price)

        if len(self.changes) < 4:
            return
        
        sequence = ",".join([str(number) for number in self.changes[-4:]])
        if sequence in self.seen:
            return
        
        price = self.cache.get(sequence, 0) + new_price
        self.cache[sequence] = price
        self.seen.add(sequence)

        self.best_price = max(self.best_price, price)
        if self.best_price == new_price:
            self.best_sequence = sequence

    def evolve_secret_number(self, secret_number):

        result =  secret_number * 64
        secret_number = self.mix(secret_number, result)
        secret_number = self.prune(secret_number)
        result = secret_number // 32
        secret_number = self.mix(secret_number, result)
        secret_number = self.prune(secret_number)
        result = secret_number * 2048
        secret_number = self.mix(secret_number, result)
        secret_number = self.prune(secret_number)

        return secret_number

    def mix(self, secret_number, given_number):
        return secret_number ^ given_number

    def prune(self, secret_number, divisor=16777216):
        return secret_number % divisor

if __name__ == "__main__":

    initial_secret_numbers = parse(input("Input File: "))
    secret_numbers = SecretNumbers(initial_secret_numbers)
    print(f"Secret Numbers after 2000 days: {sum(secret_numbers.evolve_secret_numbers_days())}")
    print(f"Best Sequence and Bananas: {secret_numbers.get_best_sequence_and_price()}")