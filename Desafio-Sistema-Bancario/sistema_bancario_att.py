saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
menu = "MENU"
usuarios = []
contas = []
AGENCIA = "0001"

def sacar(*,saldo, limite, extrato, numero_saques, limite_saques):
    if numero_saques == limite_saques:
            print ("\33[31mSeu limite de saque diário foi excedido\033[m")
    else:    
        valor = float(input("Qual Valor deseja Sacar? R$ "))
        if valor > saldo:
            print ("\33[31mVocê não tem saldo suficiente\033[m")
        elif valor > limite:
            print ("\33[31mLimite máximo por saque é R$ 500,00\033[m")
        else:
            saldo -= valor
            extrato += f"\33[31mSacou = R$ {valor:.2f}\033[m\n"
            numero_saques += 1
            print ("\033[33mSaque efetuado\033[m")
    return saldo, extrato

def depositar(saldo, extrato,/):

    valor = float(input("Qual Valor deseja depositar? R$ "))
    
    if valor > 0:
        saldo += valor
        extrato += f"\033[32mDepositou = R$ {valor:.2f}\033[m\n"
        print("\033[33mDepósito Efetuado\033[m")
    else:
        print ("\033[31mValor de depósito não permitido\033[m")
    
    return saldo, extrato

def ver_extrato(saldo,/,*, extrato):
    print (extrato)

    print(f"\033[34mSaldo = R$ {saldo:.2f}\033[m")    
    return saldo, extrato

def criar_usuario(usuarios):
    
    cpf = input("Digite o CPF (Somente numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print( "\033[31mJá existe usuário com esse CPF!\033[m")
        return
    
    nome= input("Digite o nome:")
    data_de_nascimento = input("Digite data de Nascimento (dd-mm-aaaa): ")
   
    endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_de_nascimento": data_de_nascimento, "cpf": cpf, "endereco": endereco})
    print("\033[32mUsuário cadastrado com sucesso!\033[m")
    
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print( "\033[32mConta criada com sucesso!\033[m")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\033[31mUsuário não encontrado, criação de conta cancelada!\033[m")


while True:
    print (menu.center(30,'='))
    print( """
    (1) - SACAR
    (2) - DEPOSITAR
    (3) - EXTRATO
    (4) - CRIAR USUARIO
    (5) - CRIAR CONTA  

    (0) - SAIR
          
          """
        )

    opcao = int(input("Escolha uma opção: "))

    
    if opcao == 1:
        saldo, extrato = sacar(saldo=saldo,limite=limite,extrato=extrato,numero_saques=numero_saques,limite_saques=LIMITE_SAQUES)
    elif opcao == 2:
        saldo, extrato = depositar(saldo,extrato)

    elif opcao == 3:
        saldo, extrato = ver_extrato(saldo,extrato=extrato)
    
    elif opcao == 4:
        criar_usuario(usuarios)
    
    elif opcao == 5:
        numero_conta = len(contas) +1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)

    elif opcao == 0:
        break
    else:
        print ("Opção inválida, digite uma opção válida!")