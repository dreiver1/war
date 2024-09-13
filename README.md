# War Game Backend

Este repositório contém o backend para o jogo de tabuleiro War, desenvolvido usando FastAPI. O projeto utiliza um banco de dados SQLite para armazenar dados do jogo.

## Estrutura do Repositório

- `src/`: Contém o código-fonte do projeto e o banco de dados SQLite.
  - `war_game.db`: Banco de dados SQLite com dados já cadastrados.
  - `main.py`: Arquivo principal para iniciar o servidor FastAPI.
  - `requirements.txt`: Lista de dependências necessárias para o projeto.

## Instruções de Instalação e Execução

1. **Instale as dependências**:
   Navegue até o diretório `src` e execute o seguinte comando para instalar as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt

1. **Inicie o Servidor local**:
   Execute o Servidor com o comando:
   ```bash
   uvicorn main:app --reload

   - cetifique-se de estar dentro do diretorio `/src`