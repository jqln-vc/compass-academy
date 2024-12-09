#!/usr/bin/python3
"""
Mascarador: Função de criptografia de texto com SHA-1.

Autoria: Jaqueline Costa
Data: Dez/2024
"""


def mascarador() -> None:
    """Função de criptografia de texto com SHA-1.

    Recebe textos como input e imprime a string codificada em SHA-1.

    Pressionar [Enter] para sair.
    """
    import hashlib as h

    while True:
        try:
            texto = input("Digite um texto para codificar - [Enter] para sair: ")

            if texto == "":
                break
            else:
                code_texto = texto.encode("utf-8")

                print(f"Texto codificado em SHA-1: \
                {h.sha1(code_texto).hexdigest()}")

        except EOFError as e:
            print(f"{e}: \
                Não foi fornecido nenhum input durante a execução do programa.")


if __name__ == '__main__':
    mascarador()
