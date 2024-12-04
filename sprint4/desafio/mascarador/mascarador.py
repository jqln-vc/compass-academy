#!/usr/bin/python3
def mascarador() -> None:
    """Função de mascaramento de string com SHA-1."""
    import hashlib as h

    string = input("Digite um texto para criptografar: ").encode("utf-8")
    print(f"Texto criptografado em SHA-1: {h.sha1(string).hexdigest()}")


if __name__ == '__main__':
    mascarador()
