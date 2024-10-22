#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# consolidador_de_processamento_de_vendas.sh: Script a consolidação de relatórios gerados
# -------------------------------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
ECOMMERCE="${SELF_PATH}/ecommerce"
VENDAS="${ECOMMERCE}/vendas"
BACKUP="${VENDAS}/backup"
DESCARTE="${DESCARTE}"

# -------------------------------------------------------------------------------------------------------------------------
# Função

consolidacao() {            # Consolidação de relatórios.txt em ordem cronológica
    
    echo "Consolidando relatórios de vendas..."
    # cd ./ecommerce/vendas/backup
    cd "${BACKUP}"
    find . -name "*-*.txt" | xargs cat >> relatorio_final.txt
    echo "Relatório final gerado com sucesso!"
}

# -------------------------------------------------------------------------------------------------------------------------
# Execução

main() {            # Execução do script
    
    echo -e "Iniciando script ${0}\n"
    consolidacao

}

main