import sqlite3
from datetime import datetime
import time
'''
Eu abordo desafios de maneira inovadora, 
dedicando tempo para apresentar e salvar a solução de forma detalhada. 
Comprometo-me a documentar todo o processo e fornecer um relatório claro em um arquivo TXT. 
Além disso, sou meticuloso em garantir que todos os requisitos sejam atendidos e aprimorados conforme necessário, 
assegurando a entrega de um resultado de alta qualidade. 
Também tenho a capacidade de criar um ambiente que simule como seria um projeto com a parte backend, 
permitindo uma visão completa e funcional do sistema

'''
class ContaBancaria:
    def __init__(self):
        # Inicializa a conexão com o banco de dados SQLite e define o cursor.
        # Cria as tabelas necessárias e obtém o saldo inicial da conta.
        self.conn = sqlite3.connect('banco.db')
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        self.saldo = self.obter_saldo()
        self.saques_diarios = 0
        self.limite_saques_diarios = 3
        self.limite_valor_saque = 500.00

    def criar_tabelas(self):
        # Cria tabelas para armazenar contas e extratos, se ainda não existirem.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                saldo REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS extratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                valor REAL,
                data TEXT
            )
        ''')
        self.conn.commit()

    def obter_saldo(self):
        # Obtém o saldo atual da conta. Se não houver saldo, inicializa com 0.
        self.cursor.execute('SELECT saldo FROM contas WHERE id = 1')
        saldo = self.cursor.fetchone()
        if saldo:
            return saldo[0]
        else:
            self.cursor.execute('INSERT INTO contas (saldo) VALUES (0)')
            self.conn.commit()
            return 0.0

    def formatar_valor(self, valor):
        # Formata o valor para o formato monetário brasileiro (R$ 1.000,00).
        valor_formatado = f"{valor:,.2f}"
        valor_formatado = valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {valor_formatado}"

    def depositar(self, valor):
        # Realiza um depósito na conta, atualiza o saldo e registra a transação no extrato.
        if valor > 0:
            self.saldo += valor
            self.cursor.execute('UPDATE contas SET saldo = ? WHERE id = 1', (self.saldo,))
            self.cursor.execute('INSERT INTO extratos (tipo, valor, data) VALUES (?, ?, ?)', 
                                ('Depósito', valor, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()
            return f"Depósito de {self.formatar_valor(valor)} realizado com sucesso.\n"
        else:
            time.sleep(1)
            return "Valor de depósito inválido. Apenas valores positivos são aceitos.\n"

    def sacar(self, valor):
        # Realiza um saque da conta, atualiza o saldo e registra a transação no extrato.
        if self.saques_diarios >= self.limite_saques_diarios:
            return "Limite de saques diários atingido."

        if valor > self.limite_valor_saque:
            return f"O limite por saque é de {self.formatar_valor(self.limite_valor_saque)}. Não é possível sacar valores maiores."

        if valor > self.saldo:
            return "Saldo insuficiente para realizar o saque."

        if valor <= 0:
            return "Valor de saque inválido. Apenas valores positivos são aceitos."

        self.saldo -= valor
        self.cursor.execute('UPDATE contas SET saldo = ? WHERE id = 1', (self.saldo,))
        self.cursor.execute('INSERT INTO extratos (tipo, valor, data) VALUES (?, ?, ?)', 
                            ('Saque', valor, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        self.saques_diarios += 1
        return f"Saque de {self.formatar_valor(valor)} realizado com sucesso."

    def visualizar_extrato(self):
        # Exibe e grava o extrato de todas as transações realizadas.
        self.cursor.execute('SELECT tipo, valor, data FROM extratos ORDER BY data DESC')
        extrato = self.cursor.fetchall()
        
        if not extrato:
            return "Nenhuma transação realizada."
        
        # Gera o arquivo de extrato.txt com o mesmo formato exibido no console.
        with open('extrato.txt', 'w') as file:
            file.write("\n--- Extrato ---\n")
            for tipo, valor, data in extrato:
                file.write(f"{tipo}: {self.formatar_valor(valor)} - {data}\n")
            file.write(f"\nSaldo atual: {self.formatar_valor(self.saldo)}\n")
        
        # Exibe o extrato no console.
        print("\n--- Extrato ---")
        for tipo, valor, data in extrato:
            print(f"{tipo}: {self.formatar_valor(valor)} - {data}")
        print(f"\nSaldo atual: {self.formatar_valor(self.saldo)}")
        return f"Saldo atual: {self.formatar_valor(self.saldo)}"

    def fechar_conexao(self):
        # Fecha a conexão com o banco de dados.
        self.conn.close()

    def converter_para_float(self, valor):
        # Converte o valor em string para float, considerando diferentes formatos de entrada.
        valor = valor.replace('.', '').replace(',', '.')
        return float(valor)

def exibir_menu():
    # Exibe o menu principal e retorna a opção escolhida pelo usuário.
    print("\n--- Menu ---")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Visualizar Extrato")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_depositar(conta):
    # Permite ao usuário realizar depósitos contínuos até que escolha voltar ao menu.
    while True:
        valor = input("Informe o valor para depósito ou 'm' para voltar ao menu: ")
        if valor.lower() == 'm':
            break
        try:
            valor = conta.converter_para_float(valor)
            print(conta.depositar(valor))
        except ValueError:
            print("Valor inválido. Por favor, insira um número ou 'm' para voltar ao menu.")

def menu_sacar(conta):
    # Permite ao usuário realizar saques contínuos até que escolha voltar ao menu.
    while True:
        valor = input("Informe o valor para saque ou 'm' para voltar ao menu: ")
        if valor.lower() == 'm':
            break
        try:
            valor = conta.converter_para_float(valor)
            print(conta.sacar(valor))
        except ValueError:
            print("Valor inválido. Por favor, insira um número ou 'm' para voltar ao menu.")

conta = ContaBancaria()

while True:
    opcao = exibir_menu()

    if opcao == '1':
        menu_depositar(conta)

    elif opcao == '2':
        menu_sacar(conta)

    elif opcao == '3':
        conta.visualizar_extrato()

    elif opcao == '4':
        print("Saindo do sistema...")
        conta.fechar_conexao()
        break

    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")
