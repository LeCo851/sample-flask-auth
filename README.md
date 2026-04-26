# sample-flask-auth

Repositório criado para armazenar o código de uma API RESTful de autenticação e gerenciamento de usuários.

## Tecnologias Utilizadas

- **Python & Flask:** Framework principal para o desenvolvimento da API.
- **Flask-SQLAlchemy:** ORM para interação com o banco de dados MySQL.
- **Flask-Login:** Gerenciamento de sessões e autenticação de usuários.
- **Bcrypt:** Criptografia (hashing) de senhas para maior segurança.
- **MySQL:** Banco de dados relacional.

## Funcionalidades e Rotas (Endpoints)

A API trabalha com requisições e respostas no formato JSON.

### Autenticação
- `POST /login`: Realiza o login do usuário. Requer `username` e `password`.
- `GET /logout`: Realiza o logout do usuário atual (Requer autenticação).

### Gerenciamento de Usuários
- `POST /user`: Cria (registra) um novo usuário. A senha é salva com hash (bcrypt) e a permissão padrão é `user`.
- `GET /user/<id>`: Retorna os dados (`id` e `username`) de um usuário específico. (Requer autenticação).
- `PUT /user/<id>`: Atualiza a senha de um usuário.
  - **Regra:** Um usuário com role `user` só pode atualizar a própria senha.
  - Requer autenticação e envio do campo `password`.
- `DELETE /user/<id>`: Exclui um usuário do sistema.
  - **Regra:** Apenas administradores (`role == 'admin'`) podem realizar esta operação. Um admin não pode deletar a si mesmo.
  - Requer autenticação.

## Execução

### 1. Subindo o Banco de Dados com Docker

Para rodar o banco de dados MySQL com as configurações exigidas pela API de forma rápida, utilize o Docker executando o comando abaixo:

```bash
docker run --name flask-mysql -e MYSQL_ROOT_PASSWORD=admin123 -e MYSQL_DATABASE=flask-crud -p 3307:3306 -d mysql:latest
```

### 2. Iniciando a API

1. Instale as dependências necessárias do projeto (ex: `pip install flask flask-sqlalchemy flask-login bcrypt pymysql cryptography`).
2. Execute a aplicação rodando o comando: `python app.py`