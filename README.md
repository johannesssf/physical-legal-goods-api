# Descrição

Este projeto consiste em uma API REST utilizada para controlar o cadastro e consulta de pessoas físicas, pessoas jurídicas e seus proprietários bem como o registro de bens e posses associados às essas pessoas.

# Conteúdo

* [Status do build](#Status_do_build)
* [Requisitos funcionais](#Requisitos_funcionais)
* [Requisitos não funcionais](#Requisitos_não_funcionais)
* [Documentação da API](#Documentação_da_API)
* [Como subir a aplicação](#Como_subir_a_aplicação)

# Status do projeto

## Status do build

![GitHub branch checks state](https://img.shields.io/github/checks-status/johannesssf/physical-legal-goods-api/main?style=plastic)

## Cobertura

![Codecov branch](https://img.shields.io/codecov/c/github/johannesssf/physical-legal-goods-api/main)

# Requisitos funcionais

* Registro de pessoas, a partir do CPF
* Registro de empresas e donos da empresa (podendo ser pessoas físicas e ou jurídicas, ou seja, uma empresa que tem como dono uma outra empresa)
* Registro de bens e posses de um indivíduo

## Estrutura dos dados

### Pessoa física

* **cpf**
* name
* zipcode
* email
* phone_number

### Pessoa jurídica

* **cnpj**
* social_reason
* fantazy_name
* state_registration
* owner (cpf, cnpj)
* zipcode
* email
* phone_number

### Bens

* type (imovel, veiculo, empresa)
* description
* owner (cpf, cnpj)

# Requisitos não funcionais

* Desenvolvimento em Python 3+
* Django REST framework
* Boa cobertura de testes mínima de 80%
* Docker e/ou algum aparato de containerização e deployment

# Documentação da API

Veja [aqui](https://johannesssf.github.io/physical-legal-goods-api/).

# Como subir a aplicação

## Build da imagem

1. Baixar o arquivo _Dockerfile_

    wget https://github.com/johannesssf/physical-legal-goods-api/blob/main/Dockerfile

1. Executar o comando a seguir para fazer o _build_ da imagem

    docker build --rm -t physical-legal-goods-api:latest .

1. Executar o comando a seguir para iniciar o container

    docker container run -d -p 8000:8000 physical-legal-goods-api

1. Executar os comando a seguir para consultar e criar um registro

    curl -i -X GET http://localhost:8000/v1/physical-people/

    curl -i -X POST http://localhost:8000/v1/physical-people/ -H "Content-Type: application/json" -d '{"cpf": "25845675391", "name": "Fulano da Silva", "zipcode": "55632148", "email": "fulano@email.com", "phone_number": "48999521756"}'

    curl -i -X GET http://localhost:8000/v1/physical-people/
