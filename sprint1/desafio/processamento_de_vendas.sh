#!/usr/bin/bash
# Desafio Sprint 1 - Processamento de Vendas
# Autoria: Jaqueline Costa
# Data: out/2024
# processamento_de_vendas.sh: Script para processamento de relatórios de vendas,
# com funções de backup, compressão e compilação de relatórios
#-------------------------------------------------------------------------------------------------------------------------
# Declaração de variáveis úteis
#
# Caminhos

ECOMMERCE="./ecommerce"
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


#-------------------------------------------------------------------------------------------------------------------------

prep_env() {                    # Preparação do ambiente ecommerce, com planilha dados_de_vendas.csv inserida
    echo -e "Preparando ambiente..."

    prep1="Diretório ecommerce criado"
    [[ ! -d ./ecommerce ]] && mkdir ecommerce && echo $prep1 || echo $prep1
    
    prep2="Planilha dados_de_vendas.csv movida para o diretório ecommerce"
    find / -name dados_de_vendas.csv 2> /dev/null | xargs -I {} mv {} ecommerce/ 2> /dev/null \
    && echo -e "${prep2}\nPreparação concluída com sucesso!\n" 

}

vendas_backup() {               # Criação de diretório vendas e backup, criação de cópia de segurança da planilha do dia
    echo "Iniciando backup..."
    
    # + indica um output personalizado para date, ignorando o valor default 
    data=$(date +%Y%m%d)
    
    item1="Diretórios vendas e vendas/backup criados"
    cd ecommerce
    [[ ! -d ./vendas/backup/ ]] && mkdir -p ./vendas/backup/ && echo $item1 || echo $item1

    item2="Copiado dados_de_vendas.csv para vendas e vendas/backup, renomeado com data atual $data"
    item3="Renomeado dados-AAAAMMDD.csv em vendas/backup para backup-dados-AAAAMMDD.csv"
    cp "./dados_de_vendas.csv" ./vendas \
    && cp "./dados_de_vendas.csv" ./vendas/backup \
    && echo $item2 \
    && mv "./vendas/backup/dados_de_vendas.csv" "./vendas/backup/dados-${data}.csv" 2> /dev/null \
    && cd ./vendas/backup \
    && mv "dados-${data}.csv" "backup-dados-${data}.csv" \
    && cd ../../../ \
    && echo -e "${item3}\nBackup concluído com sucesso!\n"

}

relatorio() {               # Criação de relatório de vendas, data inicial e final, quantidade de vendas, amostra
    echo "Iniciando criação de relatório..."

    #sudo ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
    data=$(date +"%Y/%m/%d %H:%M")

    item4="Relatório de hoje ${data} criado com sucesso!"
    cd ./ecommerce/vendas/backup
    touch relatorio.txt \
    && echo $data >> relatorio.txt \
    && cut -d ',' -f 5 backup*.csv | sed -n '2p' >> relatorio.txt 2>/dev/null \
    && cut -d ',' -f 5 backup*.csv | tail -n 1 >> relatorio.txt 2>/dev/null \
    #&& cut -d ',' -f 3 backup*.csv | paste -sd+ | bc >>  relatorio.txt \
    && cut -d ',' -f 2 backup*.csv | sort | uniq -c >> relatorio.txt 2>/dev/null \
    && head backup*.csv >> relatorio.txt \
    && echo -e "${item4}\n"

}    

compressao() {              # Compressão de arquivos de backup
    echo "Iniciando compressão de arquivos de backup..."
    cd ./ecommerce/vendas/backup
    data=$(find . -name backup*.csv | cut -d '-' -f 3 | cut -d '.' -f 1) \
    && zip "backup-dados-${data}.zip" "backup-dados-${data}.csv" \
    && cd ../../../ \
    && echo -e "Compressão concluída com sucesso!\n"
}

limpeza_arquivos() {        # Remoção de dados de vendas e backup já processados
    echo "Removendo arquivos csv de dados de vendas e backup já processados"

    rm -f ./ecommerce/vendas/backup/backup*.csv \
    && rm -f ./ecommerce/vendas/dados_de_vendas.csv

    echo -e "Planilha de vendas de hoje e backup removidos com sucesso!\n"
}

agendamento_rotina() {
    echo "Iniciando agendamento..."
    #sudo apt update
    #sudo apt install cron
    
    #rotina="27 15 * * 1-4 ./processamento_de_vendas.sh >> ./log_rotinas.log 2>&1"
    rotina="*/5 * * * * /workspaces/compass-academy/sprint1/desafio/processamento_de_vendas.sh >> /home/log_rotinas.log 2>&1"

}


main () {

    vendas_backup \
    && relatorio \
    && compressao \
    && limpeza_arquivos
}

echo -e "Iniciando script ${0}\n"
main