import Block

# Frame object holds the blocks and frame information.
class Frame:
    
    F = 0
    blocks = []
    CRC = 32
    
    
    # Constructor
    #
    # @param K: The number of blocks
    # @param F: Size of the frame in number of bits.
    def __init__(self, K, F):
        self.F = F
        
        # Create blocks
        block_length = F/K
        self.blocks = []
        for i in range(K):
            self.blocks.append(Block.Block(block_length));

    # Checks probability of error on every bit.
    #
    # @return: bool indicating whether transmission successful. (If 2+ bits in
    # a block are corrupted, then need to retransfer).
    def performErrorChance(self, error_chance, rnd):
        for block in self.blocks:
            if not block.performErrorChance(error_chance, rnd):
                return False
        return True

    # Calculate number of bits needed for HSBC and CRC
    # @return : Sum of HSBC bits + CRC length
    def getWastedData(self):
        total = self.CRC
        
        for block in self.blocks:
            total += block.HSBC

        return total
