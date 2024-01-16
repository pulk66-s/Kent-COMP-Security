from ex2 import *

class Attacker(ClientA):
    def __init__(self, server):
        super().__init__(server, "C")

def attack_work():
    server = Server()
    clientA = ClientA(server)
    clientB = ClientB(server)
    attacker = Attacker(server)

    print("====")
    clientA.ask_connection(clientB)
    attacker.keyAB = clientA.keyAB

    print("==== Send random message ====")
    attacker.send_random_message(clientB)

def main():
    attack_work()

if __name__ == "__main__":
    main()
