"""
"""

#####################################################################
# IMPORTAÇÕES

import random
import time
import names

#####################################################################
# ETAPA 1: NÚMEROS ALEATÓRIOS

numeros_random = [random.randrange(0, 1000000) for num in range(250)][::-1]
#print(numeros_random)

#####################################################################
# ETAPA 2: LISTA DE ANIMAIS

with open("nomes_animais.csv", "a") as arq:
    animais_fofinhos = [
        "Tyrannosaurus rex",
        "Velociraptor mongoliensis",
        "Spinosaurus aegyptiacus",
        "Allosaurus fragilis",
        "Baryonyx walkeri",
        "Carnotaurus sastrei",
        "Deinonychus antirrhopus",
        "Irritator challengeri",
        "Saurophaganax maximus",
        "Therizinosaurus cheloniformis",
        "Argentinosaurus huinculensis",
        "Pachycephalosaurus wyomingensis",
        "Ankylosaurus magniventris",
        "Edmontosaurus regalis",
        "Carcharodontosaurus saharicus",
        "Utahraptor ostrommaysorum",
        "Gallimimus bullatus",
        "Protoceratops andrewsi",
        "Microraptor gui",
        "Coelophysis bauri"
    ]

    #for dino in sorted(animais_fofinhos):
        #print(dino)
        #arq.write(f"{dino}\n")

#####################################################################
# ETAPA 3: NOMES ALEATÓRIOS

random.seed(210388)
qtd_nomes_unicos = 3001
qtd_nomes_aleatorios = 10000001
nomes_unicos = [names.get_full_name() for num in range(qtd_nomes_unicos)]

print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios...")
nomes_aleatorios = [random.choice(nomes_unicos) for num in range(qtd_nomes_aleatorios)]

with open("nomes_aleatorios.txt", "a") as arq2:
    for nome in nomes_aleatorios:
        arq2.write(f"{nome}\n")

print("Geração de nomes aleatórios concluída. Arquivo salvo com sucesso!")
