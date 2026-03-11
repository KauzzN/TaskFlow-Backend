# TaskFlow – Backend

TaskFlow é um projeto de estudo focado no desenvolvimento de um backend para gerenciamento de tarefas diárias.
O objetivo é construir uma API REST capaz de se integrar com um frontend, explorando boas práticas de arquitetura backend, autenticação de usuários e persistência de dados.

O projeto simula a base de um sistema real de gerenciamento de tarefas, onde usuários podem criar e organizar suas atividades de forma segura.

---

## Objetivos do projeto

* Praticar desenvolvimento backend com Django
* Construir uma API REST estruturada
* Implementar autenticação baseada em tokens
* Desenvolver operações CRUD completas
* Integrar backend com frontend
* Observabilidade, monitoramento, logs e metricas
* Preparar o projeto para deploy em ambiente real

---

## Stack utilizada

**Linguagem:** Python
**Framework:** Django
**Banco de dados:** PostgreSQL
**ORM:** ORM nativa do Django
**IDE:** Visual Studio Code

---

## Funcionalidades implementadas

### Autenticação

* Cadastro de usuários
* Login com geração de tokens
* Logout
* Autenticação baseada em tokens
* Refresh automático de token
* Blacklist de refresh_tokens

### Gerenciamento de tarefas

* Criar tarefas
* Listar tarefas do usuário
* Atualizar tarefas
* Remover tarefas

### API

* API REST baseada em JSON
* Estrutura de endpoints organizada
* Validação de dados
* Tratamento de erros

### EndPoints

- Auth

* POST /accounts/register/
* POST /accounts/login/
* POST /accounts/refresh/
* POST /accounts/logout/

- CRUD

* GET /tasks/
* POST /tasks/
* PATCH /tasks/{id}
* DELETE /tasks/{id}

---

## Estrutura geral do projeto

O backend é responsável por:

* Gerenciar autenticação de usuários
* Controlar o acesso às tarefas
* Persistir dados no banco
* Expor endpoints REST para consumo do frontend

O frontend se comunica com a API utilizando requisições HTTP com autenticação via token.

---

## Status do projeto

Em desenvolvimento (projeto de estudo).

Atualmente o sistema já possui autenticação funcional e CRUD completo para gerenciamento de tarefas.

Próximos passos planejados:

* Melhorias de validação e segurança
* Containerização com Docker
* Observabilidade (logs e métricas)
* Deploy em ambiente real

---

## Como executar o projeto

# 1 - Clonar o repositório

  git clone {repo-url}

# 2 - Criar ambiente virtual

  python -m venv venv

# 3 - Ativar o ambiente virtual

  Linux / Mac:

# source venv/bin/activate

  Windows:

# venv\Scripts\activate

# 4 - Instalar dependências

  pip install -r requirements.txt

# 5 - Configurar banco de dados

# O projeto utiliza PostgreSQL.
# As configurações de conexão estão definidas no arquivo settings.py.

# Certifique-se de ter um banco criado no PostgreSQL antes de rodar as migrations.

# 6 - Rodar migrations

  python manage.py migrate

# 7 - Iniciar servidor

  python manage.py runserver
