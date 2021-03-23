
from cryptography.fernet import Fernet
from arcade import load_texture
def load_texture_pair(filename):

    return [
        load_texture(filename),
        load_texture(filename, flipped_horizontally=True),
    ]


def save(save_list: list):
    text = "Start\n"
    for value in save_list:
        text += str(value)
        text += "\n"
    text += "End"
    text = str.encode(text)
    encrypt(text)


def load() -> list:
    with open("save.dat", "rb") as file_enc:
        data = file_enc.read()
    file_enc.close()
    decrypted = bytes.decode(decrypt(data))
    load_list = decrypted.split("\n")
    load_list.pop(0)  # Pop first element Start
    load_list.pop(-1)  # Pop last element blank character
    return load_list


def encrypt(file: bytes):
    with open("game_key.key", "rb") as mykey:
        key = mykey.read()
    mykey.close()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(file)
    with open("save.dat", "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    encrypted_file.close()


def decrypt(file: bytes) -> bytes:
    with open("game_key.key", "rb") as mykey:
        key = mykey.read()
    mykey.close()
    fernet = Fernet(key)
    original = fernet.decrypt(file)
    return original

if __name__ == "__main__":
    main()

def main():
    pass