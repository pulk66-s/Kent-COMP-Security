from bitstring import BitArray
import hmac
import hashlib

def hmac_encrypt_16bit(key, message):
    """Returns the HMAC of the message.
    Parameters:
        key: secret key used to encrypt the message.
        message: The message to encrypt.
    """
    hash_algorithm = hashlib.sha256
    hmac_obj = hmac.new(key.encode("utf-8"), message.encode("utf-8"), hash_algorithm)

    # Truncate the HMAC to 16 bits
    truncated_hmac = hmac_obj.digest()[:2]
    return truncated_hmac

def hmac_verify_16bit(key, message, tag):
    """Returns True if the tag is correct, False otherwise.
    Parameters:
        key: The key used to encrypt the message.
        message: The message to encrypt.
        tag: The tag to verify.
            What is a tag? A tag is a short piece of information used to authenticate a message.
    """
    return hmac_encrypt_16bit(key, message) == tag

def eve_manipulation(key, message, tag):
    """Eve is a malicious attacker who wants to change the message.
    She can't change the tag, but she can change the message.
    """
    return hmac_encrypt_16bit(key, message + "Eve was here!") == tag

def eve_brute_force(key, message):
    """Eve is a malicious attacker who wants to change the message.
    She can't change the tag, but she can change the message. to test all
    """
    new_message = message + "Eve was here!"
    for i in range(2 ** 16):
        new_tag = i.to_bytes(2, byteorder="big")
        if hmac_verify_16bit(key, new_message, new_tag):
            print("Found tag:", new_tag)
            return True
    return False

def password_guessing_attack(message, tag):
    """Eve is a malicious attacker who wants to guess the password.
    She can't change the tag, but she can change the message.
    """
    for i in range(10):
        new_password = str(i)
        if hmac_encrypt_16bit(new_password, message) == tag:
            return new_password
    return None

def main():
    # Message to send
    message = "Hello, world! This is a very long message."
    # Secret key
    key = "5"
    # generate hmac
    tag = hmac_encrypt_16bit(key, message)
    print("Tag:", tag, BitArray(hex=tag.hex()).bin)
    # eve interception
    message = "This message has been intercepted by Eve!"
    # verification
    print("Verified:", hmac_verify_16bit(key, message, tag))

    # # Eve tries to manipulate the message.
    # print("Eve's manipulation:", eve_manipulation(key, message, tag))

    # # Eve tries to brute force the message.
    # print("Eve's brute force:", eve_brute_force(key, message))

    # # Eve tries to guess the password.
    # print("Eve's password guessing attack:", password_guessing_attack(message, tag))

if __name__ == "__main__":
    main()
