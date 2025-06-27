saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3
menu = "MENU"

while True:
    print (menu.center(30,'='))
    print( """
    (1) - SACAR
    (2) - DEPOSITAR
    (3) - EXTRATO

    (0) - SAIR
          
          """
        )

    opcao = int(input("Escolha uma opção: "))

    
    if opcao == 1:
        if numero_saques == limite_saques:
            print ("\33[31mSeu limite de saque diário foi excedido\033[m")
        else:    
            sacar_valor = float(input("Qual Valor deseja Sacar? R$ "))
            if sacar_valor > saldo:
                print ("\33[31mVocê não tem saldo suficiente\033[m")
            elif sacar_valor > limite:
                print ("\33[31mLimite máximo por saque é R$ 500,00\033[m")
            else:
                saldo -= sacar_valor
                extrato += f"\33[31mSacou = R$ {sacar_valor:.2f}\033[m\n"
                numero_saques += 1
                print ("\033[33mSaque efetuado\033[m")
    
    elif opcao == 2:
        valor_deposito = float(input("Qual Valor deseja depositar? R$ "))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"\033[32mDepositou = R$ {valor_deposito:.2f}\033[m\n"
            print("\033[33mDepósito Efetuado\033[m")
        else:
            print ("\033[31mValor de depósito não permitido\033[m")

    elif opcao == 3:
        print (extrato)
        print(f"\033[34mSaldo = R$ {saldo:.2f}\033[m")
    elif opcao == 0:
        break
    else:
        print ("Opção inválida, digite uma opção válida!")