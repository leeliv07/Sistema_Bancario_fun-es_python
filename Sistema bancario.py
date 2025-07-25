import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [l]\tLogin (acessar conta)
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def menu_conta():
    menu = """\n
    ========== OPERAÇÕES ==========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair da conta
    => """
    return input(textwrap.dedent(menu))

def depositar(conta, valor):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
        print("✅ Depósito realizado com sucesso!")
    else:
        print("⚠️ Valor inválido.")

def sacar(conta, valor):
    if valor <= 0:
        print("⚠️ Valor inválido.")
    elif valor > conta["saldo"]:
        print("⚠️ Saldo insuficiente.")
    elif valor > conta["limite"]:
        print("⚠️ Excede o limite de saque.")
    elif conta["saques_hoje"] >= conta["limite_saques"]:
        print("⚠️ Limite diário de saques atingido.")
    else:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta["saques_hoje"] += 1
        print("✅ Saque realizado com sucesso!")

def exibir_extrato(conta):
    print("\n========= EXTRATO =========")
    print(conta["extrato"] if conta["extrato"] else "Nenhuma movimentação.")
    print(f"Saldo:\t\tR$ {conta['saldo']:.2f}")
    print("===========================")

def criar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    if not cpf.isdigit() or len(cpf) != 11:
        print("⚠️ CPF inválido.")
        return
    if filtrar_usuario(cpf, usuarios):
        print("⚠️ Usuário já existe.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço: ")
    usuarios.append({"cpf": cpf, "nome": nome, "nascimento": nascimento, "endereco": endereco})
    print("✅ Usuário criado com sucesso.")

def filtrar_usuario(cpf, usuarios):
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def criar_conta(agencia, numero, usuarios, contas):
    cpf = input("CPF do titular: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("⚠️ Usuário não encontrado.")
        return

    conta = {
        "agencia": agencia,
        "numero": numero,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "limite": 500,
        "limite_saques": 3,
        "saques_hoje": 0
    }
    contas.append(conta)
    print("✅ Conta criada com sucesso.")

def listar_contas(contas):
    for conta in contas:
        print("="*40)
        print(f"Agência:\t{conta['agencia']}")
        print(f"Conta:\t\t{conta['numero']}")
        print(f"Titular:\t{conta['usuario']['nome']}")

def acessar_conta(contas):
    cpf = input("Digite seu CPF: ")
    contas_usuario = [c for c in contas if c["usuario"]["cpf"] == cpf]

    if not contas_usuario:
        print("⚠️ Nenhuma conta encontrada para esse CPF.")
        return

    print("Contas disponíveis:")
    for i, conta in enumerate(contas_usuario, 1):
        print(f"[{i}] Conta {conta['numero']} - Agência {conta['agencia']}")

    escolha = int(input("Selecione a conta: ")) - 1
    if 0 <= escolha < len(contas_usuario):
        conta_selecionada = contas_usuario[escolha]
        while True:
            op = menu_conta()
            if op == "d":
                valor = float(input("Valor do depósito: "))
                depositar(conta_selecionada, valor)
            elif op == "s":
                valor = float(input("Valor do saque: "))
                sacar(conta_selecionada, valor)
            elif op == "e":
                exibir_extrato(conta_selecionada)
            elif op == "q":
                break
            else:
                print("⚠️ Opção inválida.")
    else:
        print("⚠️ Seleção inválida.")

def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        op = menu()
        if op == "nu":
            criar_usuario(usuarios)
        elif op == "nc":
            criar_conta(AGENCIA, numero_conta, usuarios, contas)
            numero_conta += 1
        elif op == "lc":
            listar_contas(contas)
        elif op == "l":
            acessar_conta(contas)
        elif op == "q":
            print("👋 Até mais!")
            break
        else:
            print("⚠️ Opção inválida.")

main()