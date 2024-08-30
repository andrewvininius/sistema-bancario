# Sistema Bancário em Python

## Descrição

Este projeto é um sistema bancário básico desenvolvido em Python. O sistema permite realizar operações de depósito, saque e visualizar extratos de uma conta bancária. Utiliza SQLite para armazenar os dados e possui um menu interativo para o usuário.

## Funcionalidades

- **Depósito**: Permite ao usuário depositar valores positivos na conta. O sistema formata os valores para o padrão monetário brasileiro (R$ 1.000,00).
- **Saque**: Permite ao usuário sacar valores da conta com limites diários e por operação. O sistema registra a quantidade de saques diários e o limite máximo por saque.
- **Extrato**: Exibe todas as transações realizadas (depósitos e saques) e o saldo atual. O extrato é salvo em um arquivo `extrato.txt` com o mesmo formato exibido no console.
- **Menu Interativo**: O usuário pode escolher entre realizar depósitos, saques, visualizar o extrato ou sair do sistema.

## Requisitos

- Python 3.x
- SQLite

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/usuario/repo.git

 
