
# Block objects represent the different blocks in a frame.
class Block:

    HSBC = 0
    length = 0

    # Constructor
    #
    # @param l: Length of block
    def __init__(self, l):

        # Calculate HSBC
        self.HSBC = len("{0:b}".format(l)) if l > 0 else 0
        self.length = l

    def performErrorChance(self, error_chance):
        # TODO - Check if bits are in error. If 2+ are wrong,
        # then return false
        
        return True
