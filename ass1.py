import hashlib
import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n):
    if n <= 1:
        return 2
    prime = n
    found = False
    while not found:
        prime += 1
        if is_prime(prime):
            found = True
    return prime

def generate_keys(name):
    seed = sum(ord(char) for char in name)

    p = next_prime(seed)
    q = next_prime(p + 1)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2
    while math.gcd(e, phi) != 1:
        e += 1

    d = pow(e, -1, phi)

    return ((e, n), (d, n))

def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)


class Block:
    def __init__(self, previous_hash, transaction):
        self.previous_hash = previous_hash
        self.transaction = transaction
        string_to_hash = "".join(transaction) + previous_hash
        self.block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.all_transactions = []
        self.genesis_block()

    def genesis_block(self):
        genesis_block = Block("nothing", ["nothing"])
        self.chain.append(genesis_block)
        return self.chain

    def add_block(self, transaction):
        previous_block_hash = self.chain[len(self.chain) - 1].block_hash
        new_block = Block(previous_block_hash, transaction)
        self.chain.append(new_block)
        return self.chain

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.block_hash:
                return False
        return True

    def print_blocks(self):
        for i in range(len(self.chain)):
            current = self.chain[i]
            print("Block ", i)
            print("Hash: ", current.block_hash)
            print("Previous Hash: ", current.previous_hash)
            print("Transaction: ")
            for transaction in current.transaction:
                print(transaction)
            print("\n")

    def add_transaction(self, transaction):
        self.all_transactions.append(transaction)

    def print_transactions(self):
        for i in range(len(self.all_transactions)):
            print("Transaction ", i)
            print(self.all_transactions[i])
            print("\n")

    def generate_merkle_tree(self):
        if len(self.all_transactions) == 0:
            return None

        merkle_tree = []

        for transaction in self.all_transactions:
            merkle_tree.append(hashlib.sha256(str(transaction).encode()).hexdigest())

        level = merkle_tree

        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                if i + 1 < len(level):
                    next_level.append(hashlib.sha256((level[i] + level[i + 1]).encode()).hexdigest())
                else:
                    next_level.append(hashlib.sha256((level[i] + level[i]).encode()).hexdigest())
            level = next_level

        return level[0]


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def __str__(self):
        return f'Transaction from {self.sender} to {self.receiver} for {self.amount}'

    def sign(self, private_key):
        message = str(self.sender) + str(self.receiver) + str(self.amount)
        self.signature = encrypt(message, private_key)

    def verify_signature(self, public_key):
        message = str(self.sender) + str(self.receiver) + str(self.amount)
        decrypted_message = decrypt(self.signature, public_key)
        return message == decrypted_message

def main():
    blockchain = Blockchain()

    user = input("Enter your name: ")

    public_key, private_key = generate_keys(user)

    print("Your public key is: ", public_key)
    print("Your private key is: ", private_key)

    while True:
        print("1. Add transaction")
        print("2. Add block")
        print("3. Print transactions")
        print("4. Print blocks")
        print("5. Validate chain")
        print("6. Generate Merkle Tree")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            sender = input("Enter sender's name: ")
            receiver = input("Enter receiver's name: ")
            amount = input("Enter amount: ")
            transaction = Transaction(sender, receiver, amount)
            transaction.sign(private_key)
            blockchain.add_transaction(transaction)
        elif choice == 2:
            blockchain.add_block(blockchain.all_transactions)
        elif choice == 3:
            blockchain.print_transactions()
        elif choice == 4:
            blockchain.print_blocks()
        elif choice == 5:
            print(blockchain.validate_chain())
        elif choice == 6:
            merkle_tree = blockchain.generate_merkle_tree()
            print("Merkle Tree: ", merkle_tree)
        elif choice == 7:
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()