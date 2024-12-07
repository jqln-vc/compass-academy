#!/usr/bin/python3
"""
    Mascarador: Função de mascaramento de string com SHA-1.
"""
def mascarador() -> None:
    """Função de mascaramento de string com SHA-1."""
    import hashlib as h

    string = input("Digite um texto para criptografar - [Enter] para sair: ").encode("utf-8")
    print(f"Texto criptografado em SHA-1: {h.sha1(string).hexdigest()}")
    
    if string == '\n':
        return False


if __name__ == '__main__':
    while True:
        mascarador()
