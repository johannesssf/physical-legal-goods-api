# Descrição

Este projeto consiste em uma API REST utilizada para controlar o cadastro e consulta de pessoas físicas, pessoas jurídicas e seus proprietários bem como o registro de bens e posses associados à estas.

# Conteúdo

* [Status do build](#Status_do_build)
* [Requisitos funcionais](#Requisitos_funcionais)
* [Requisitos não funcionais](#Requisitos_não_funcionais)
* [Documentação da API](#Documentação_da_API)
* [Como subir a aplicação](#Como_subir_a_aplicação)
* [Pontos de melhoria](#Pontos_de_melhoria)

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

## Informações

**user**: admin

**password**: 123456

## Fazer o build da imagem

Baixe o arquivo _Dockerfile_ e execute o comando de build

        $ wget https://github.com/johannesssf/physical-legal-goods-api/blob/main/Dockerfile
        $ docker build --rm -t physical-legal-goods-api:latest .

## Fazer o pull da imagem pronta

Baixar uma imagem já pronta

        $ docker pull johannesssf/physical-legal-goods-api:latest

## Executar alguns comandos para testar

Comando para iniciar o container

        $ docker container run -d -p 8000:8000 physical-legal-goods-api

Comandos para consultar e criar um registro

        $ curl --location --request GET 'http://localhost:8000/v1/physical-people/' --header 'Authorization: Basic YWRtaW46MTIzNDU2'

        $ curl -i -X POST http://localhost:8000/v1/physical-people/ -H "Content-Type: application/json" -d '{"cpf": "25845675391", "name": "Fulano da Silva", "zipcode": "55632148", "email": "fulano@email.com", "phone_number": "48999521756"}' --header 'Authorization: Basic YWRtaW46MTIzNDU2'

        $ curl -i -X GET http://localhost:8000/v1/physical-people/ --header 'Authorization: Basic YWRtaW46MTIzNDU2'

# Pontos de melhoria

* Adicionar um meio de autenticação mais seguro, atualmente está com o modo básico;
* Embora a cobertura esteja em 100%, ainda poderíamos adicionar mais casos para deixar mais robusto;
* Adicionar endpoints para gerenciar contas de usuário que podem acessar a aplicação;
* Também podemos adicionar outros tipos de teste;
*
