
# Block objects represent the different blocks in a frame.
class Block:

    HSBC = 0
    length = 0
    errorLimit = 2

    # Constructor
    #
    # @param l: Length of block
    def __init__(self, l, useErrorCorrection):

        # Calculate HSBC
        self.HSBC = len("{0:b}".format(l)) if l > 0 else 0
        self.length = l
        self.errorLimit = (2 if useErrorCorrection else 1)

    def performErrorChance(self, error_chance, rnd):

        error_count = 0
        for trial in range(self.length):
            if rnd.random() < error_chance:
                error_count = error_count + 1
                if error_count >= self.errorLimit:
                    return False

        return True
