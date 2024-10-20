#!/usr/bin/bash

prep_env() {
    echo "Preparando ambiente..."
    [[ ! -d ./ecommerce ]] && mkdir ecommerce
    
    find / -name "*vendas.csv" 2> /dev/null | xargs -I {} mv {} ecommerce/ 2> /dev/null \
    && echo "Preparação concluída: diretório ecommerce criado e planilha dados_de_vendas.csv movida dentro dele"
}







main () {
    prep_env
}

echo "Iniciando script $0"
main