class ContaBancaria:
    def __init__(self):
        self.saldo = 0.0
        self.extrato = []
        self.saques_diarios = 0
        self.limite_saques_diarios = 3
        self.limite_valor_saque = 500.00

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: R$ {valor:.2f}")
            return f"Depósito de R$ {valor:.2f} realizado com sucesso."
        else:
            return "Valor de depósito inválido. Apenas valores positivos são aceitos."

    def sacar(self, valor):
        if self.saques_diarios >= self.limite_saques_diarios:
            return "Limite de saques diários atingido."

        if valor > self.limite_valor_saque:
            return f"O limite por saque é de R$ {self.limite_valor_saque:.2f}. Não é possível sacar valores maiores."

        if valor > self.saldo:
            return "Saldo insuficiente para realizar o saque."

        if valor <= 0:
            return "Valor de saque inválido. Apenas valores positivos são aceitos."

        self.saldo -= valor
        self.extrato.append(f"Saque: R$ {valor:.2f}")
        self.saques_diarios += 1
        return f"Saque de R$ {valor:.2f} realizado com sucesso."

    def visualizar_extrato(self):
        if not self.extrato:
            return "Nenhuma transação realizada."
        
        print("\n--- Extrato ---")
        for operacao in self.extrato:
            print(operacao)
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        return f"Saldo atual: R$ {self.saldo:.2f}"

def exibir_menu():
    print("\n--- Menu ---")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Visualizar Extrato")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

# Exemplo de uso com menu
conta = ContaBancaria()

while True:
    opcao = exibir_menu()

    if opcao == '1':
        valor = float(input("Informe o valor para depósito: "))
        print(conta.depositar(valor))

    elif opcao == '2':
        valor = float(input("Informe o valor para saque: "))
        print(conta.sacar(valor))

    elif opcao == '3':
        conta.visualizar_extrato()

    elif opcao == '4':
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")
