import random

def encrypt(message, key):
    print("message:", message, "key:", key, type(message), type(key))
    cipher = [ chr((ord(c) + key) % 256) for c in message ]
    return ''.join(cipher)

class Server:
    def __generateKey(self):
        return random.randint(1000, 5000)

    def __init__(self):
        self.keyA = self.__generateKey()
        self.keyB = self.__generateKey()

    def receiveConnection(self, clientA, clientB, nonceA):
        print("nonceA:", nonceA)
        print("clientA.keyS:", clientA.keyS)
        print("clientB.keyS:", clientB.keyS)

        ab_key = clientA.keyS + clientB.keyS
        ab_key_message = str(ab_key) + str(clientA.id)
        print("ab_key_message:", ab_key_message)

        encrypted_ab_key = encrypt(ab_key_message, clientB.keyS)
        print("encrypted_ab_key:", encrypted_ab_key)

        response = str(clientA.nonce) + str(clientB.id) + str(ab_key) + encrypted_ab_key
        print("response:", response)

        encrypted_response = encrypt(response, clientA.keyS)
        print("encrypted_response:", encrypted_response)

        return encrypted_response

class Client:
    def __init__(self, server, id):
        self.id = id
        self.nonce = random.randint(1000, 5000)
        self.server = server
        self.keyS = ""

    def _decrypt_response(self, encrypted_response, key):
        response = [ chr((ord(c) - key) % 256) for c in encrypted_response ]
        return ''.join(response)

    def ask_connection(self, clientB):
        encrypted_response = self.server.receiveConnection(self, clientB, self.nonce)
        print("Encrypted response:", encrypted_response)

        decrypted_response = self._decrypt_response(encrypted_response, self.keyS)
        print("Decrypted response:", decrypted_response)

        self.keyAB = int(decrypted_response[5:9])
        encrypted_message_for_B = decrypted_response[9:]
        print("self.keyAB:", self.keyAB)
        print("encrypted_message_for_B:", encrypted_message_for_B)
        clientB.receive_encrypted_key(encrypted_message_for_B)

    def receive_encrypted_key(self, encrypted_message):
        decrypted_message = self._decrypt_response(encrypted_message, self.keyS)
        print("Decrypted message:", decrypted_message)
        self.keyAB = int(decrypted_message[0:4])
        print("keyAB:", self.keyAB)


class ClientA(Client):
    def __init__(self, server, key="A"):
        super().__init__(server, key)
        self.keyS = self.server.keyA

    def send_random_message(self, clientB):
        nonce = random.randint(1000, 5000)
        encrypted_message = encrypt(str(nonce), self.keyAB)
        clientB.receive_random_message(encrypted_message, self)

    def receive_answer(self, encrypted_message):
        decrypted_message = self._decrypt_response(encrypted_message, self.keyAB)
        print("Decrypted message:", decrypted_message)

class ClientB(Client):
    def __init__(self, server):
        super().__init__(server, "B")
        self.keyS = self.server.keyB

    def receive_random_message(self, encrypted_message, clientA):
        decrypted_message = self._decrypt_response(encrypted_message, self.keyAB)
        print("Decrypted message:", decrypted_message)
        nonce = int(decrypted_message) - 1
        encrypted_message = encrypt(str(nonce), self.keyAB)
        clientA.receive_answer(encrypted_message)

def normal_work():
    server = Server()
    clientA = ClientA(server)
    clientB = ClientB(server)

    print("====")
    clientA.ask_connection(clientB)
    clientA.send_random_message(clientB)

def main():
    normal_work()

if __name__ == "__main__":
    main()
