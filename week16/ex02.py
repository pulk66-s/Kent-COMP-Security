import hashlib

def find_hashed_pwd(hash):
    """Finds the password for a given hash.
    Parameters:
        hash (str): The hash.
    """
    database = open("phpbb.txt", "r")
    for password in database:
        password = password.strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == hash:
            print(f"Password is {password}")
            break
    database.close()

def main():
    hash = "3ddcd95d2bff8e97d3ad817f718ae207b98c7f2c84c5519f89cd15d7f8ee1c3b"
    find_hashed_pwd(hash)

if __name__ == '__main__':
    main()
