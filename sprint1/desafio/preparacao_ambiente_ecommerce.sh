#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: out/2024
# processamento_de_vendas.sh: Script complementar ao processamento_de_vendas.sh, responsável pela
# prepararação do ambiente ecommerce
# ------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
ECOMMERCE="${SELF_PATH}/ecommerce"
DESCARTE="/dev/null"


# Prefixos e nomes de arquivos

PLANILHA="dados_de_vendas.csv"

# ------------------------------------------------------------------------------------------------


prep_env() {                    # Preparação do ambiente ecommerce, com planilha dados_de_vendas.csv inserida
    echo -e "Preparando ambiente..."

    cd ${SELF_PATH}
    OUT="Diretório ecommerce criado"
    [[ ! -d ${ECOMMERCE} ]] && mkdir ecommerce && echo $OUT || echo $OUT
    
    find / -name $PLANILHA 2> ${DESCARTE} | xargs -I {} mv {} $ECOMMERCE/ 2> ${DESCARTE} \
    && echo -e "Planilha ${PLANILHA} movida para o diretório ecommerce\nPreparação concluída com sucesso!\n" 

}

main () {
    echo -e "Iniciando script ${0}\n"
    prep_env

}

main