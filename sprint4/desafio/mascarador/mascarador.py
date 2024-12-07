#!/usr/bin/python3
"""
Mascarador: Função de mascaramento de texto com SHA-1.

Autoria: Jaqueline Costa
Data: Dez/2024
"""


def mascarador() -> None:
    """Função de mascaramento de texto com SHA-1.

    Recebe textos como input e imprime a texto codificada em SHA-1.

    Pressionar [Enter] para Sair.
    """
    import hashlib as h

    while True:
        texto = input("Digite um texto para codificar - [Enter] para sair: ")

        if texto == "":
            break
        else:
            code_texto = texto.encode("utf-8")

            print(f"Texto codificado em SHA-1: \
            {h.sha1(code_texto).hexdigest()}")


if __name__ == '__main__':
    mascarador()
