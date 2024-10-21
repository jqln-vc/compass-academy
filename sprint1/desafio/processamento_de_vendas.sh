#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: out/2024
# processamento_de_vendas.sh: Script para processamento de relatórios de vendas,
# com funções de backup, compressão e compilação de relatórios
# -------------------------------------------------------------------------------------------------------------------------
# Declaração de Variáveis
#
# Caminhos

SELF_PATH="/workspaces/compass-academy/sprint1/desafio"
ECOMMERCE="${SELF_PATH}/ecommerce"
VENDAS="${ECOMMERCE}/vendas"
BACKUP="${VENDAS}/backup"
DESCARTE="/dev/null"

# Prefixos e nomes de arquivos

PLANILHA="dados_de_vendas.csv"
DADOS_PLANILHA="dados-"
BACKUP_PLANILHA="backup-dados-"


# Formatos de Datas
# + indica um output personalizado para date, ignorando o valor default 

DATA_FILES=$(date +"%Y%m%d")
DATA_HORA=$(date +"%Y/%m/%d %H:%M")
/

#-------------------------------------------------------------------------------------------------------------------------

prep_env() {                    # Preparação do ambiente ecommerce, com planilha dados_de_vendas.csv inserida
    echo -e "Preparando ambiente..."

    cd ${SELF_PATH}
    prep1="Diretório ecommerce criado"
    [[ ! -d ${ECOMMERCE} ]] && mkdir ecommerce && echo $prep1 || echo $prep1
    
    prep2="Planilha dados_de_vendas.csv movida para o diretório ecommerce"
    find / -name dados_de_vendas.csv 2> /dev/null | xargs -I {} mv {} $ECOMMERCE/ 2> /dev/null \
    && echo -e "${prep2}\nPreparação concluída com sucesso!\n" 

}

vendas_backup() {               # Criação de diretório vendas e backup, criação de cópia de segurança da planilha do dia
    echo "Iniciando backup..."
    
    # + indica um output personalizado para date, ignorando o valor default 
    data=$(date +%Y%m%d)
    
    item1="Diretórios vendas e vendas/backup criados"
    cd ${ECOMMERCE}
    [[ ! -d $BACKUP ]] && mkdir -p $BACKUP && echo $item1 || echo $item1

    item2="Copiado dados_de_vendas.csv para vendas e vendas/backup, renomeado com data atual $data"
    item3="Renomeado dados-AAAAMMDD.csv em vendas/backup para backup-dados-AAAAMMDD.csv"
    cp "${ECOMMERCE}/dados_de_vendas.csv" "${ECOMMERCE}/vendas" \
    && cp "./dados_de_vendas.csv" "${BACKUP}" \
    && echo $item2 \
    && mv "${BACKUP}/dados_de_vendas.csv" "${BACKUP}/dados-${data}.csv" 2> /dev/null \
    && cd ${BACKUP} \
    && mv "dados-${data}.csv" "backup-dados-${data}.csv" \
    && echo -e "${item3}\nBackup concluído com sucesso!\n"

}

relatorio() {               # Criação de relatório de vendas, data inicial e final, quantidade de vendas, amostra
    echo "Iniciando criação de relatório..."

    #sudo ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
    data=$(date +"%Y/%m/%d %H:%M")

    item4="Relatório de hoje ${data} criado com sucesso!"
    cd ${BACKUP}
    touch "relatorio-${DATA_FILES}.txt" \
    && echo $data >> "relatorio-${DATA_FILES}.txt" \
    && cut -d ',' -f 5 backup*.csv | sed -n '2p' >> "relatorio-${DATA_FILES}.txt" 2>/dev/null \
    && cut -d ',' -f 5 backup*.csv | tail -n 1 >> "relatorio-${DATA_FILES}.txt" 2>/dev/null \
    && cut -d ',' -f 2 backup*.csv | sort | uniq -c | wc -l >> "relatorio-${DATA_FILES}.txt" 2>/dev/null \
    && head backup*.csv >> "relatorio-${DATA_FILES}.txt" \
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


main () {

    echo -e "Iniciando script ${0}\n"

    vendas_backup \
    && relatorio \
    && compressao \
    && limpeza_arquivos
}


main