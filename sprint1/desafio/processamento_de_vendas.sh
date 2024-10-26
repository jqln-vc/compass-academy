#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# processamento_de_vendas.sh: Script para processamento de relatórios de vendas,
# com funções de backup, compressão e geração de relatórios
# ----------------------------------------------------------------------------------------------------------------------------
# Declaração de Variáveis

# Caminhos

SELF_PATH=$(pwd)
ECOMMERCE="${SELF_PATH}/ecommerce"
VENDAS="${ECOMMERCE}/vendas"
BACKUP="${VENDAS}/backup"
DESCARTE="/dev/null"

# Arquivo

PLANILHA="dados_de_vendas.csv"

# Formatos de Datas
    # + indica um output personalizado para date, ignorando o valor default 

DATA=$(date +"%Y%m%d")
DATA_HORA=$(date +"%Y/%m/%d %H:%M")

# Etapas

ITEM1="Criação dos diretórios vendas e backup concluída."
ITEM2="Cópias de dados_de_vendas.csv concluída. Renomeação com data atual ${DATA} concluída."
ITEM3="Renomeação de dados-AAAAMMDD.csv para backup-dados-AAAAMMDD.csv concluída."
ITEM4="Criação de relatório de hoje ${DATA_HORA} concluída."
ITEM5="Compressão de arquivos de backup concluída."
ITEM6="Remoção de arquivos processados concluída."
ITEM7="Processamento de vendas concluído com sucesso!"

# ----------------------------------------------------------------------------------------------------------------------------
# Funções

vendas_backup() {       # Criação de diretório vendas e backup, criação de cópia de segurança da planilha do dia
    echo "Iniciando backup..."
         
    [[ ! -d $BACKUP ]] && mkdir -p ${BACKUP} && echo ${ITEM1} || echo ${ITEM1}

    cp "${ECOMMERCE}/${PLANILHA}" "${VENDAS}" \
    && cp "${ECOMMERCE}/${PLANILHA}" "${BACKUP}/dados-${DATA}.csv" \
    && echo ${ITEM2} \
    && mv "${BACKUP}/dados-${DATA}.csv" "${BACKUP}/backup-dados-${DATA}.csv" 2> ${DESCARTE} \
    && echo -e "${ITEM3}\nBackup concluído com sucesso!\n"

}

relatorio() {       # Criação de relatório: data/hora atuais, data de venda inicial e final, qtd de itens distintos, amostra
    echo "Iniciando criação de relatório..."

    cd ${BACKUP} \
    && touch "relatorio-${DATA}.txt" \
    && echo $DATA_HORA >> "relatorio-${DATA}.txt" \
    && cut -d ',' -f 5 backup*.csv | sed -n '2p' >> "relatorio-${DATA}.txt" 2> ${DESCARTE} \
    && cut -d ',' -f 5 backup*.csv | tail -n 1 >> "relatorio-${DATA}.txt" 2> ${DESCARTE} \
    && cut -d ',' -f 2 backup*.csv | sed '1d' | sort | uniq -c | wc -l >> "relatorio-${DATA}.txt" 2> ${DESCARTE} \
    && sed '1d' backup*.csv | head -n 10 >> "relatorio-${DATA}.txt" \
    && echo >> "relatorio-${DATA}.txt" \
    && echo -e "${ITEM4}\n"

}    

compressao() {      # Compressão de arquivos de backup
    
    echo "Iniciando compressão de arquivos de backup..."

    cd ${BACKUP} \
    && zip "backup-dados-${DATA}.zip" "backup-dados-${DATA}.csv" \
    && echo -e "${ITEM5}\n"
}

limpeza_arquivos() {        # Remoção de dados de vendas e backup já processados
    
    echo "Iniciando limpeza de arquivos..."

    rm -f ${BACKUP}/backup*.csv \
    && rm -f ${VENDAS}/dados*.csv \
    && echo -e "${ITEM6}\n"
} 

# ----------------------------------------------------------------------------------------------------------------------------
# Execução

main () {       # Pipeline de execução do script

    echo -e "Iniciando script ${0}\n"

    vendas_backup \
    && relatorio \
    && compressao \
    && limpeza_arquivos \
    && echo -e "${ITEM7}\n"

    exit 0
}


main