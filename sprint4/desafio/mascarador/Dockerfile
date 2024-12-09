# Uso de imagem pypy slim (mais ágil e eficiente)
FROM pypy:3-slim

# Criação de usuário para a aplicação, flag -m para criação de /home
RUN useradd -m mascarador

# Definição do diretório de trabalho
WORKDIR /mascarador

# Cópia dos arquivos da aplicação para o WORKDIR
COPY . .

# Alteração da propriedade da pasta e conteúdo para o usuário "mascarador"
RUN chown -R mascarador /mascarador

# Definição do usuário atual como "mascarador"
USER mascarador

# Fornecimento de permissão de execução para os arquivos da aplicação
RUN chmod +x *.py

# Comando de execução da aplicação
CMD [ "pypy3", "mascarador.py" ]