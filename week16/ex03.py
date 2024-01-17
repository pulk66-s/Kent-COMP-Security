import itertools
import hashlib

DICTIONARY = {
    "laplusbelle"
    "Marie",
    "Curie",
    "Woof",
    "2",
    "01",
    "1980",
    "80",
    "ukc",
    "university",
    "kent",
    "canterbury",
    "Jean",
    "Neoskour",
    "Jvaist",
    "Fairecourir",
    "Eltrofor",
    "29",
    "12",
    "1981",
    "81"
}

def try_pass(hash, salt, password):
    """Tries a password.
    Parameters:
        hash (str): The hash.
        salt (str): The salt.
        password (str): The password.
        index (int): The index.
    Returns:
        bool: True if the password is correct, False otherwise.
    """
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed == hash

def dict_attack(hash, salt, dictionary):
    """Performs a dictionary attack.
    Parameters:
        hash (str): The hash.
        salt (str): The salt.
        dictionary (list): The dictionary.
    Returns:
        list: The personalized dictionary.
    """
    personalized_dictionary = []
    for i in range(1, len(dictionary)):
        for combination in itertools.permutations(dictionary, i):
            if try_pass(hash, salt, "".join(combination)):
                print(f"Password is {''.join(combination)}")
                return
    return personalized_dictionary

def main():
    hash = "3281e6de7fa3c6fd6d6c8098347aeb06bd35b0f74b96f173c7b2d28135e14d45"
    salt = "5UA@/Mw^%He]SBaU"
    dict_attack(hash, salt, DICTIONARY)

if __name__ == '__main__':
    main()
