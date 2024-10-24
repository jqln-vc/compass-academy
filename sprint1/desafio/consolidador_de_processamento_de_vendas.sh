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

#SELF_PATH=$(pwd)
SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
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
    find . -name "relatorio*.txt" | xargs cat >> relatorio-final.txt
    echo -e "${ITEM1}\n"
}

# ---------------------------------------------------------------------------------------------------------------------
# Execução

main() {            
    
    echo -e "Iniciando script ${0}\n"

    consolidacao \
    && echo -e "${ITEM2}\n"

    exit 0
}

main