
# Block objects represent the different blocks in a frame.
class Block:

    HSBC = 0

    # Constructor
    #
    # @param l: Length of block
    def __init__(self, l):

        # Calculate HSBC
        self.HSBC = len("{0:b}".format(l)) if l > 0 else 0
