from cryptography.fernet import Fernet

'''
    Stub function to understand how to use Fernet's Cryptography Module

    (This file can't be used as standalone program)
'''


def main():
    key = Fernet.generate_key()  # Generating Key

    with open("game_key.key", "wb") as mykey:
        mykey.write(key)

    # If you want to open and read the key file
    with open('game_key.key', 'rb') as mykey:
        key = mykey.read()


if __name__ == "__main__":
    main()
