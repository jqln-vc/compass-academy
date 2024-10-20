#!/usr/bin/bash

prep_env() {
    echo -e "Preparando ambiente..."
    prep1="Diretório ecommerce criado"
    [[ ! -d ./ecommerce ]] && mkdir ecommerce && echo $prep1 || echo $prep1
    
    prep2="Planilha dados_de_vendas.csv movida para o diretório ecommerce"
    find / -name "*vendas.csv" 2> /dev/null | xargs -I {} mv {} ecommerce/ 2> /dev/null \
    && echo -e "${prep2}\nPreparação concluída com sucesso!\n" 
}

vendas_backup() {
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
    && echo -e "${item3}\nBackup concluído com sucesso!"
}






main () {
    prep_env
    vendas_backup
}

echo -e "Iniciando script ${0}\n"
main