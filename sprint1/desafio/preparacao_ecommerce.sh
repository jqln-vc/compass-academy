#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# preparacao_ecommerce.sh: Script complementar ao processamento_de_vendas.sh, responsável pela
# prepararação do ambiente ecommerce
# ----------------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

SELF_PATH=$(pwd)
ECOMMERCE="${SELF_PATH}/ecommerce"
DESCARTE="/dev/null"

# Arquivo

PLANILHA=${1}

# Etapas

ITEM1="Criação do diretório ecommerce concluída."
ITEM2="Localização da planilha ${PLANILHA} e seu deslocamento para ecommerce concluídos."
ITEM3="Preparação do ambiente ecommerce concluída com sucesso!"

# ----------------------------------------------------------------------------------------------------------
# Função

prep_env() {        # Criação de ambiente ecommerce, localização de planilha e inserção no ambiente 
    
    echo -e "Preparando ambiente..."

    [[ ! -d ${ECOMMERCE} ]] && mkdir ecommerce && echo ${ITEM1} || echo ${ITEM1}
    
    find ${SELF_PATH} -name ${PLANILHA} 2> ${DESCARTE} | xargs -0 -I {} mv {} $ECOMMERCE/ 2> ${DESCARTE} \
    && echo -e "${ITEM2}\n" 

}

# ----------------------------------------------------------------------------------------------------------
# Execução

main () {

    echo -e "Iniciando script ${0}\n"
    prep_env \
    && echo -e "${ITEM3}\n"

    return 0

}

main