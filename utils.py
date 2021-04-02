from cryptography.fernet import Fernet
from arcade import load_texture


def load_texture_pair(filename):

    return [
        load_texture(filename),
        load_texture(filename, flipped_horizontally=True),
    ]


def save(save_list: list):
    """
    Used to save a list of object as encrypted bytes into save.dat

    Parameters
    ----------
    save_list : list
        The list to save in the file
    """

    text = "Start\n"
    for value in save_list:
        text += str(value)
        text += "\n"
    text += "End"
    text = str.encode(text)
    encrypted = encrypt(text)
    with open("save.dat", "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    encrypted_file.close()


def load() -> list:
    """
    Open save.dat as decrypted bytes and return a list of strings

    Returns
    -------
    list
        The list of strings decrypted
    """

    with open("save.dat", "rb") as file_enc:
        data = file_enc.read()
    file_enc.close()
    decrypted = bytes.decode(decrypt(data))
    load_list = decrypted.split("\n")
    load_list.pop(0)  # Pop first element Start
    load_list.pop(-1)  # Pop last element blank character
    return load_list


def encrypt(file: bytes) -> bytes:
    """
    Encrypt bytes with Fernet Cryptography using game_key.key file

    Parameters
    ----------
    file : bytes
        The alredy open file as bytes not crypted
    
    Returns
    -------
    bytes
        Same bytes as input but encrypted
    """

    with open("game_key.key", "rb") as mykey:
        key = mykey.read()
    mykey.close()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(file)
    return encrypted


def decrypt(file: bytes) -> bytes:
    """
    Decrypt bytes with Fernet Cryptography using game_key.key file

    Parameters
    ----------
    file : bytes
        The alredy open file as bytes crypted
    
    Returns
    -------
    bytes
        Same bytes as input but decrypted
    """

    with open("game_key.key", "rb") as mykey:
        key = mykey.read()
    mykey.close()
    fernet = Fernet(key)
    original = fernet.decrypt(file)
    return original
