#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: Out/2024
# processamento_de_vendas.sh: Script para processamento de relatórios de vendas,
# com funções de backup, compressão e geração de relatórios
# -------------------------------------------------------------------------------------------------------------------------
# Declaração de Variáveis

# Caminhos

SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
ECOMMERCE="${SELF_PATH}/ecommerce"
VENDAS="${ECOMMERCE}/vendas"
BACKUP="${VENDAS}/backup"
DESCARTE="/dev/null"

# Arquivo

PLANILHA="dados_de_vendas.csv"

# Formatos de Datas
    # + indica um output personalizado para date, ignorando o valor default 

DATA_FILES=$(date +"%Y%m%d")
DATA_HORA=$(date +"%Y/%m/%d %H:%M")


#-------------------------------------------------------------------------------------------------------------------------
# Funções

vendas_backup() {           # Criação de diretório vendas e backup, criação de cópia de segurança da planilha do dia
    echo "Iniciando backup..."
        
    item1="Diretórios vendas e vendas/backup criados"
    cd ${ECOMMERCE}
    [[ ! -d $BACKUP ]] && mkdir -p $BACKUP && echo $item1 || echo $item1

    item2="Copiado dados_de_vendas.csv para vendas e vendas/backup, renomeado com data atual ${DATA_FILES}"
    item3="Renomeado dados-AAAAMMDD.csv em vendas/backup para backup-dados-AAAAMMDD.csv"
    cp "${ECOMMERCE}/${PLANILHA}" "${VENDAS}" \
    && cp "${ECOMMERCE}/${PLANILHA}" "${BACKUP}" \
    && echo $item2 \
    && mv "${BACKUP}/dados_de_vendas.csv" "${BACKUP}/dados-${DATA_FILES}.csv" 2> ${DESCARTE} \
    && cd ${BACKUP} \
    && mv "dados-${DATA_FILES}.csv" "backup-dados-${DATA_FILES}.csv" \
    && echo -e "${item3}\nBackup concluído com sucesso!\n"

}

relatorio() {               # Criação de relatório de vendas, data inicial e final, quantidade de vendas, amostra
    echo "Iniciando criação de relatório..."

    item4="Relatório de hoje ${DATA_HORA} criado com sucesso!"
    cd ${BACKUP}
    touch "relatorio-${DATA_FILES}.txt" \
    && echo $DATA_HORA >> "relatorio-${DATA_FILES}.txt" \
    && cut -d ',' -f 5 backup*.csv | sed -n '2p' >> "relatorio-${DATA_FILES}.txt" 2> ${DESCARTE} \
    && cut -d ',' -f 5 backup*.csv | tail -n 1 >> "relatorio-${DATA_FILES}.txt" 2> ${DESCARTE} \
    && cut -d ',' -f 2 backup*.csv | sed '1d' backup*.csv | sort | uniq -c | wc -l >> "relatorio-${DATA_FILES}.txt" 2> ${DESCARTE} \
    && sed '1d' backup*.csv | head -n 10 >> "relatorio-${DATA_FILES}.txt" \
    && echo >> "relatorio-${DATA_FILES}.txt" \
    && echo -e "${item4}\n"

}    

compressao() {              # Compressão de arquivos de backup
    echo "Iniciando compressão de arquivos de backup..."
    cd ${BACKUP}
    
    zip "backup-dados-${DATA_FILES}.zip" "backup-dados-${DATA_FILES}.csv" \
    && echo -e "Compressão concluída com sucesso!\n"
}

limpeza_arquivos() {        # Remoção de dados de vendas e backup já processados
    echo "Removendo arquivos csv de dados de vendas e backup já processados"

    rm -f ${BACKUP}/backup*.csv \
    && rm -f "${VENDAS}/dados_de_vendas.csv"

    echo -e "Planilha de vendas de hoje e backup removidos com sucesso!\n"
}

# -------------------------------------------------------------------------------------------------------------------------
# Execução

main () {           # Pipeline de execução do script

    echo -e "Iniciando script ${0}\n"

    vendas_backup \
    && relatorio \
    && compressao \
    && limpeza_arquivos
}


main