#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# consolidador_de_processamento_de_vendas.sh: Script para consolidação de relatórios gerados pelo
# script processamento_de_vendas.sh. Lê todos os arquivos .txt do diretório backup e concatena em um único arquivo.
# -------------------------------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
ECOMMERCE="${SELF_PATH}/ecommerce"
VENDAS="${ECOMMERCE}/vendas"
BACKUP="${VENDAS}/backup"
DESCARTE="/dev/null"

# -------------------------------------------------------------------------------------------------------------------------
# Função

consolidacao() {            # Consolidação de relatórios.txt em ordem cronológica
    
    echo "Consolidando relatórios de vendas..."
    # cd ./ecommerce/vendas/backup
    cd "${BACKUP}"
    find . -name "*-*.txt" | xargs cat >> relatorio-final.txt
    echo "Relatório final gerado com sucesso!"
}

# -------------------------------------------------------------------------------------------------------------------------
# Execução

main() {            # Execução do script
    
    echo -e "Iniciando script ${0}\n"
    consolidacao

}

main