from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta( self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls ( cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar (self, valor):
        saldo = self.saldo

        if valor > saldo:
            print ("\33[31mVocê não tem saldo suficiente\033[m")
        
        elif valor > 0:
            self._saldo -= valor
            print ("\033[33mSaque efetuado\033[m")
            return True
        
        else:
            print ("\33[31mOperação falhou, Valor Inválido!\033[m")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\033[33mDepósito Efetuado\033[m")
            return True
        else:
            print ("\033[31mValor de depósito não permitido\033[m")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self,valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if numero_saque == self.limite_saques:
            print ("\33[31mSeu limite de saque diário foi excedido\033[m")
        
        elif valor > self.limite:
            print ("\33[31mLimite máximo por saque é R$ 500,00\033[m")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar( self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


menus = "MENU"
def menu():
    print (menus.center(30,'='))
    print( """
    (1) - SACAR
    (2) - DEPOSITAR
    (3) - EXTRATO
    (4) - CRIAR USUARIO
    (5) - CRIAR CONTA
    (6) - LISTAR CONTAS

    (0) - SAIR
          
          """
        )


def sacar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print( "\033[31mCliente não encontrado!\033[m")
        return

    valor = float(input("Qual Valor deseja Sacar? R$ "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print( "\033[31mCliente não encontrado!\033[m")
        return

    valor = float(input("Qual Valor deseja depositar? R$ "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def ver_extrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print( "\033[31mCliente não encontrado!\033[m")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n========== EXTRATO ==========")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\033[34mSaldo = R$ {conta.saldo:.2f}\033[m")
    print("=============================")


def criar_usuario(clientes):
    
    cpf = input("Digite o CPF (Somente numeros): ")
    cliente = filtrar_cliente(cpf,clientes)
    if cliente:
        print( "\033[31mJá existe usuário com esse CPF!\033[m")
        return
    
    nome= input("Digite o nome:")
    data_de_nascimento = input("Digite data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(nome = nome, data_nascimento= data_de_nascimento, cpf= cpf, endereco= endereco)
    clientes.append(cliente)
    print("\033[32mUsuário cadastrado com sucesso!\033[m")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print ("\033[31mCliente não tem conta!\033[m")
        return
    return cliente.contas[0]


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
         print("\033[31mUsuário não encontrado, criação de conta cancelada!\033[m")
    
    conta = ContaCorrente.nova_conta(numero= numero_conta, cliente= cliente)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print( "\033[32mConta criada com sucesso!\033[m")
    
    
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))


def main():
    clientes = []
    contas = []

    while True:
        opcao = int(input("Escolha uma opção: "))
        
        if opcao == 1:
            sacar(clientes)
        elif opcao == 2:
            depositar(clientes)

        elif opcao == 3:
            ver_extrato(clientes)
    
        elif opcao == 4:
            criar_usuario(clientes)
    
        elif opcao == 5:
            numero_conta = len(contas) +1
            criar_conta( numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 0:
            break
        else:
            print ("Opção inválida, digite uma opção válida!")


menu()
main()