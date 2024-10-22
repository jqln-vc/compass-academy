#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# preparacao_ecommerce.sh: Script complementar ao processamento_de_vendas.sh, responsável pela
# prepararação do ambiente ecommerce
# ------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

#SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
SELF_PATH=$(pwd)
ECOMMERCE="${SELF_PATH}/ecommerce"
DESCARTE="/dev/null"


# Arquivos

#PLANILHA="dados_de_vendas.csv"
PLANILHA="$1"

# ------------------------------------------------------------------------------------------------

echo "${SELF_PATH} e ${PLANILHA}"
prep_env() {                    # Preparação do ambiente ecommerce, com planilha dados_de_vendas.csv inserida
    echo -e "Preparando ambiente..."

    #cd ${SELF_PATH}
    OUT="Diretório ecommerce criado"

    [[ ! -d ${ECOMMERCE} ]] && mkdir ecommerce && echo $OUT || echo $OUT
    
    #find / -name $PLANILHA 2> ${DESCARTE} | xargs -I {} mv {} $ECOMMERCE/ 2> ${DESCARTE} \
    find ${SELF_PATH} -name ${PLANILHA} 2> ${DESCARTE} | xargs -I {} mv {} $ECOMMERCE/ 2> ${DESCARTE} \
    && echo -e "Planilha ${PLANILHA} localizada e movida para o diretório ecommerce\nPreparação concluída com sucesso!\n" 

}

main () {
    echo -e "Iniciando script ${0}\n"
    prep_env

}

main