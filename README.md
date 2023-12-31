<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/MatMB115/ad_hoc_igdb_back_end?color=a015f5">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/MatMB115/ad_hoc_igdb_back_end">

  <a href="https://github.com/MatMB115/ad_hoc_igdb_back_end/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/MatMB115/ad_hoc_igdb_back_end">
  </a>
  <a href="https://www.postgresql.org/">
  <img alt="Database" src="https://img.shields.io/badge/database PostgreSQL-red">
  </a>

<img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
  <a href="https://github.com/MatMB115/ad_hoc_igdb_back_end/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/MatMB115/ad_hoc_igdb_back_end?style=social">
  </a>
</p>

<p align="center">
  <a href="https://github.com/MatMB115/ad_hoc_igdb_back_end">
    <img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*DpaeArqM7JWzJLylsVl9lg.png" height="250" width="500" alt="IGDB-logo" />
  </a>
</p>

<p align="center">
    <a href="https://www.python.org/">
        <img align="center" alt="Python" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg">
    </a>
    <a href="https://www.python.org/">
        <img align="center" alt="Python" height="50" width="50" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original-wordmark.svg">
    </a>
</p>

# Back-end do relatório Ad-hoc

API capaz de realizar consultas dinâmicas utilizando ORM SQLAlchemy.

---
## Sobre

Conforme as orientações para realização da parte 2 do trabalho da disciplina de Banco de Dados II da Universidade Federal de Itajubá, a equipe desenvolveu uma API responsável por realizar as consultas nas tabelas do banco. O MER utilizado está presente na Figura abaixo e os payloads para requisições estão na pasta [requests](./requests/).

Componentes do Projeto:
- [Front-end](https://gitlab.com/alisonmaciel93/bd_trabalho_final)
- [Script de Carga](https://github.com/MatMB115/script_carga_igdb)

As orientações estão divididas nos seguintes tópicos:

- [Back-end do relatório Ad-hoc](#back-end-do-relatório-ad-hoc)
  - [Sobre](#sobre)
  - [To Do :gear:](#to-do-gear)
  - [Banco de dados :chair: :game\_die:](#banco-de-dados-chair-game_die)
  - [Pré-requisitos e configuração :hammer\_and\_wrench:](#pré-requisitos-e-configuração-hammer_and_wrench)
  - [Tecnologias :technologist:](#tecnologias-technologist)
  - [Contribuidores](#contribuidores)

---
## To Do :gear:
- [x] SELECT
- [x] JOIN
- [x] WHERE
- [x] ORDER BY
- [x] AGREGGATION
- [x] ORDER BY

---
## Banco de dados :chair: :game_die:
A aplicação utiliza um banco relacional presente no modelo entidade relacionamento abaixo:
![MER_IGDB](https://imgur.com/eOmnsVN.png)

Para realizar a conexão com o banco utilizou-se:

>SQLAlchemy - 1.4.48

---
## Pré-requisitos e configuração :hammer_and_wrench:
No geral, para executar a aplicação é recomendado que o sistema já possua:

    > Python 3.11

Para executar essa API é necessário:

```bash

# Criar o banco com nome IGDB para realizar a carga

# Clone este repositório com
$ git clone https://github.com/MatMB115/ad_hoc_igdb_back_end
# OU
$ git clone git@github.com:MatMB115/ad_hoc_igdb_back_end.git

# Navegue até o diretório clonado com terminal

$ cd ad_hoc_igdb_back_end

# Instale as dependências
$ pip install -r reqs.txt

# Abra script no Vscode ou editor de preferência
$ code .

# No DAO, mude as credenciais de acesso do banco (lembre-se de criar um banco com o nome IGDB pelo SGDB)
$ engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/IGDB")

# Rode o script pelo terminal
$ py controller.py
# OU
$ python3 controller.py

```
---
## Tecnologias :technologist:
    O ponto de início deste projeto foi um ambiente Python, as dependências utilizadas estão presentes no 'reqs.txt'. 
---
Dependências:

    -> Python 3.11
    - Flask 2.5.5
    - SQLAlchemy 2.3
    - psycopg2 2.9.6
    - annotated-types 0.5
    - sqlacodegen 3.0.0rc2
    - CORS 4.0.0
---
Banco de Dados:

    -> PostgreSQL
    - pgAdmin4 7.0
---
Utilitários:

    -> Dev
    - Visual Studio Code 1.78
---  

## Contribuidores

<table>
  <tr>
</td>
    <td align="center"><a href="https://github.com/carlosdcsr"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/99037754?v=4" width="100px;" alt=""/><br /><sub><b>Matheus Martins</b></sub></a><br /><a href="https://github.com/carlosdcsr?tab=repositories" title="Ad-hoc">:technologist:</a></td>
</td>
</td>
    <td align="center"><a href="https://github.com/MatMB115"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/63670910?v=4" width="100px;" alt=""/><br /><sub><b>Matheus Martins</b></sub></a><br /><a href="https://github.com/MatMB115/repime" title="Ad-hoc">:technologist:</a></td>
</td>
  </tr>
</table>
