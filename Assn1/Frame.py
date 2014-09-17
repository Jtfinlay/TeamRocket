import Block

# Frame object holds the blocks and frame information.
class Frame:
    
    F = 0
    blocks = []
    CRC = 0 ## TODO - Calculate size of CRC
    
    
    # Constructor
    #
    # @param K: The number of blocks
    # @param F: Size of the frame in number of bits.
    def __init__(self, K, F):
        self.F = F
        
        # Create blocks
        for i in range(K):
            self.blocks.append(Block.Block());

    # Calculate number of bits needed for HSBC and CRC
    def getWastedData(self):
        total = self.CRC
        
        for block in self.blocks:
            total += block.HSBC

        return total
