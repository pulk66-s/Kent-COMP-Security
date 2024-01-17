import hashlib
from itertools import permutations

def find_hashed_pass(hash, grid):
    """Finds the hashed password.
    Parameters:
        hash (str): The hash.
        grid (str): The grid.
    """
    combinations = permutations(grid)
    for permutation in combinations:
        pattern = ''.join(permutation)
        hashed_pattern = hashlib.sha1(pattern.encode()).hexdigest()
        if hashed_pattern == hash:
            print("Unlock pattern:", pattern)
            rehashed_pattern = hashlib.sha1(pattern.encode()).hexdigest()
            if rehashed_pattern == hash:
                print("Unlock pattern correct")
            else:
                print("Unlock pattern incorrect")
            break

def main():
    hash = "91077079768edba10ac0c93b7108bc639d778d67"
    grid = "abcdefghi"
    find_hashed_pass(hash, grid)

if __name__ == '__main__':
    main()
