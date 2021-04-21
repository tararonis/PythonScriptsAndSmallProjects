"""

NeuralCoin (NC)

t1: A sends B 2 NC
t2: B sends D 4.3 NC
t3: M sends C 3.2 NC

B1 ("AAA", t1, t2) -> 76fd89, 
B2 ("76fd89..", t3, t4) -> 8923ff..,
B3 ("8923ff".., ...)

NeuralHash()

"""
import hashlib

class NeuralCoinBlock:

    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = "-".join(transaction_list) + " // " + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

def main():
    t1 = "Anna sends 2 NC to Mike"
    t2 = "Bob sends 4.2 NC to Mike"
    t3 = "Mike sends 3.2 NC to Bob"
    t4 = "Daniel sends 0.3 NC to Anna"
    t5 = "Mike sends 1 NC to Charlie"
    t6 = "Mike sends 5.4 NC to Daniel"

    genesis_block = NeuralCoinBlock("Initial block", [t1, t2])

    print(genesis_block.block_data)
    print(genesis_block.block_hash)

    second_block = NeuralCoinBlock(genesis_block.block_hash, [t3, t4])

    print(second_block.block_data)
    print(second_block.block_hash)

    third_block = NeuralCoinBlock(second_block.block_hash [t5, t6])

    print(third_block.block_data)
    print(third_block.block_hash)





if __name__ == '__main__':
    main()