#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# consolidador_de_processamento_de_vendas.sh: Script para consolidação de relatórios gerados pelo
# script processamento_de_vendas.sh. Lê todos os relatórios do diretório backup e os concatena em um único arquivo.
# ---------------------------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

SELF_PATH=$(pwd)
BACKUP="${SELF_PATH}/ecommerce/vendas/backup"
DESCARTE="/dev/null"

# Etapas

ITEM1="Geração de relatório final concluída."
ITEM2="Consolidação de relatórios concluída com sucesso!"

# ---------------------------------------------------------------------------------------------------------------------
# Função

consolidacao() {            # Consolidação de relatórios em ordem cronológica
    
    echo "Consolidando relatórios de vendas..."

    cd "${BACKUP}"
    find . -name "relatorio*.txt" | grep -E 'relatorio-[0-9]{8}\.txt' | sort | xargs -0 -I {} cat {} >> relatorio-final.txt 2> ${DESCARTE} \
    && echo -e "${ITEM1}\n"
}

# ---------------------------------------------------------------------------------------------------------------------
# Execução

main() {            
    
    echo -e "Iniciando script ${0}\n"

    consolidacao \
    && echo -e "${ITEM2}\n"

    return 0
}

main