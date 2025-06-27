def parse(input):

    As = []
    Bs = []
    prizes = []

    for line in open(input, "r"):
        if line == "\n":
            continue

        key, value = line.strip("\n").split(": ")
        X, Y = value.split(", ")
        
        if key == "Button A":
            As.append((int(X.strip("X+")), int(Y.strip("Y+"))))
        if key == "Button B":
            Bs.append((int(X.strip("X+")), int(Y.strip("Y+"))))
        if key == "Prize":
            prizes.append((int(X.strip("X=")), int(Y.strip("Y="))))

    return As, Bs, prizes

class ClawMachines():

    def __init__(self, As, Bs, prizes):

        self.As = As
        self.Bs = Bs
        self.prizes = prizes

    def cheapest_prize(self, A, B, prize):
        
        A_X, A_Y = A
        B_X, B_Y = B
        prize_X, prize_Y = prize

        A_presses = (prize_X * B_Y - prize_Y * B_X) / (A_X * B_Y - A_Y * B_X)
        B_presses = (prize_X * A_Y - prize_Y * A_X) / (B_X * A_Y - B_Y * A_X)
        if A_presses % 1 == 0 and B_presses % 1 == 0:
            return int(3 * A_presses + B_presses)

        return 0

    def modify_prizes(self, add=10000000000000):

        self.prizes = [
            (X + add, Y + add)
            for X, Y in self.prizes
        ]

    def get_fewest_tokens(self):

        total_tokens = 0

        for A, B, prize in zip(
            self.As, self.Bs, self.prizes
        ):
            total_tokens += self.cheapest_prize(A, B, prize)

        return total_tokens

if __name__ == "__main__":

    As, Bs, prizes = parse(input("Input File: "))
    claw_machines = ClawMachines(As, Bs, prizes)
    print(f"Fewest Tokens for all possible Prizes: {claw_machines.get_fewest_tokens()}")
    claw_machines.modify_prizes()
    print(f"Fewest Tokens for all possible modified Prizes: {claw_machines.get_fewest_tokens()}")
