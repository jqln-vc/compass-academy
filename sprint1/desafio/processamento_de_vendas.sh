#!/usr/bin/bash

prep_env() {
    echo "Preparando ambiente..."
    sudo su\
    && mkdir ./ecommerce\
    && PATH=$(find / -name dados_de_vendas.csv)\
    && chmod +rwx $PATH\
    && cp $PATH  ./ecommerce/
    
    exit 0
}







main () {
    prep_env
}

echo "Iniciando script $0"
main