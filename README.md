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

Descrever o procedimento para subir um container com a aplicação.
