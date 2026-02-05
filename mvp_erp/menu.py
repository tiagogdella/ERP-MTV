"""
Sistema de menus e navegação do ERP.
Interface terminal-first com navegação numérica.
"""
from datetime import date

from utils.helpers import (
    limpar_tela, cabecalho, pausar, confirmar,
    formatar_moeda, formatar_data,
    input_valor, input_inteiro, input_data
)
from services.operacoes import (
    cadastrar_empresa, listar_empresas, buscar_empresa, desativar_empresa,
    registrar_operacao, listar_operacoes, buscar_operacao,
    liquidar_operacao, cancelar_operacao
)
from services.financeiro import (
    listar_contas_a_pagar, listar_contas_a_receber,
    listar_vencidas, resumo_financeiro
)


def menu_principal():
    """Menu principal do sistema."""
    while True:
        cabecalho("ERP MVP - MENU PRINCIPAL")
        print("  1. Cadastros")
        print("  2. Operações (Compra/Venda)")
        print("  3. Financeiro")
        print("  4. Relatórios")
        print()
        print("  0. Sair")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            menu_cadastros()
        elif opcao == "2":
            menu_operacoes()
        elif opcao == "3":
            menu_financeiro()
        elif opcao == "4":
            menu_relatorios()
        elif opcao == "0":
            if confirmar("Deseja realmente sair? (S/N): "):
                limpar_tela()
                print("Sistema encerrado.")
                break
        else:
            print("Opção inválida!")
            pausar()


# ==================== CADASTROS ====================

def menu_cadastros():
    """Menu de cadastros."""
    while True:
        cabecalho("CADASTROS")
        print("  1. Cadastrar Empresa")
        print("  2. Listar Empresas")
        print("  3. Desativar Empresa")
        print()
        print("  0. Voltar")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            tela_cadastrar_empresa()
        elif opcao == "2":
            tela_listar_empresas()
        elif opcao == "3":
            tela_desativar_empresa()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            pausar()


def tela_cadastrar_empresa():
    """Tela de cadastro de empresa."""
    cabecalho("CADASTRAR EMPRESA")

    nome = input("Nome da empresa: ").strip()
    if not nome:
        print("Nome é obrigatório!")
        pausar()
        return

    cnpj = input("CNPJ (opcional): ").strip() or None

    if confirmar():
        try:
            empresa_id = cadastrar_empresa(nome, cnpj)
            print(f"\nEmpresa cadastrada com sucesso! ID: {empresa_id}")
        except Exception as e:
            print(f"\nErro ao cadastrar: {e}")

    pausar()


def tela_listar_empresas():
    """Tela de listagem de empresas."""
    cabecalho("EMPRESAS CADASTRADAS")

    empresas = listar_empresas(apenas_ativas=True)

    if not empresas:
        print("Nenhuma empresa cadastrada.")
    else:
        print(f"{'ID':<5} {'NOME':<30} {'CNPJ':<18}")
        print("-" * 55)
        for emp in empresas:
            cnpj = emp.cnpj or "-"
            print(f"{emp.id:<5} {emp.nome:<30} {cnpj:<18}")

    pausar()


def tela_desativar_empresa():
    """Tela para desativar empresa."""
    cabecalho("DESATIVAR EMPRESA")

    tela_listar_empresas()

    empresa_id = input_inteiro("ID da empresa a desativar (0 para cancelar): ", minimo=0)
    if empresa_id == 0:
        return

    empresa = buscar_empresa(empresa_id)
    if not empresa:
        print("Empresa não encontrada!")
        pausar()
        return

    print(f"\nEmpresa: {empresa.nome}")
    if confirmar("Confirma desativação? (S/N): "):
        if desativar_empresa(empresa_id):
            print("Empresa desativada com sucesso!")
        else:
            print("Erro ao desativar empresa.")

    pausar()


# ==================== OPERAÇÕES ====================

def menu_operacoes():
    """Menu de operações."""
    while True:
        cabecalho("OPERAÇÕES")
        print("  1. Registrar Compra")
        print("  2. Registrar Venda")
        print("  3. Listar Operações")
        print("  4. Liquidar Operação")
        print("  5. Cancelar Operação")
        print()
        print("  0. Voltar")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            tela_registrar_operacao("COMPRA")
        elif opcao == "2":
            tela_registrar_operacao("VENDA")
        elif opcao == "3":
            tela_listar_operacoes()
        elif opcao == "4":
            tela_liquidar_operacao()
        elif opcao == "5":
            tela_cancelar_operacao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            pausar()


def tela_registrar_operacao(tipo: str):
    """Tela de registro de operação (compra ou venda)."""
    cabecalho(f"REGISTRAR {tipo}")

    # Selecionar empresa
    empresas = listar_empresas()
    if not empresas:
        print("Cadastre uma empresa primeiro!")
        pausar()
        return

    print("Empresas disponíveis:")
    for emp in empresas:
        print(f"  {emp.id}. {emp.nome}")
    print()

    empresa_id = input_inteiro("ID da empresa: ", minimo=1)
    empresa = buscar_empresa(empresa_id)
    if not empresa:
        print("Empresa não encontrada!")
        pausar()
        return

    descricao = input("Descrição (opcional): ").strip() or None
    valor = input_valor("Valor (R$): ")
    prazo = input_inteiro("Prazo em dias [7]: ", minimo=1) if input("Usar prazo diferente de 7 dias? (S/N): ").strip().upper() == 'S' else 7

    print(f"\n--- RESUMO DA OPERAÇÃO ---")
    print(f"Tipo: {tipo}")
    print(f"Empresa: {empresa.nome}")
    print(f"Valor: {formatar_moeda(valor)}")
    print(f"Prazo: {prazo} dias")
    if descricao:
        print(f"Descrição: {descricao}")

    if confirmar("\nConfirma o registro? (S/N): "):
        try:
            op_id = registrar_operacao(
                tipo=tipo,
                empresa_id=empresa_id,
                valor=valor,
                prazo_dias=prazo,
                descricao=descricao
            )
            print(f"\nOperação registrada com sucesso! ID: {op_id}")
        except Exception as e:
            print(f"\nErro ao registrar: {e}")

    pausar()


def tela_listar_operacoes():
    """Tela de listagem de operações."""
    cabecalho("LISTAR OPERAÇÕES")

    print("Filtrar por status:")
    print("  1. Abertas")
    print("  2. Liquidadas")
    print("  3. Todas")
    print()

    filtro = input("Opção [1]: ").strip() or "1"

    status = None
    if filtro == "1":
        status = "ABERTO"
    elif filtro == "2":
        status = "LIQUIDADO"

    operacoes = listar_operacoes(status=status)

    limpar_tela()
    cabecalho("OPERAÇÕES")

    if not operacoes:
        print("Nenhuma operação encontrada.")
    else:
        print(f"{'ID':<5} {'TIPO':<7} {'EMPRESA':<20} {'VALOR':>15} {'VENCIMENTO':<12} {'STATUS':<10}")
        print("-" * 75)
        for op in operacoes:
            print(f"{op.id:<5} {op.tipo:<7} {op.empresa_nome[:20]:<20} {formatar_moeda(op.valor):>15} {formatar_data(op.data_vencimento):<12} {op.status:<10}")

    pausar()


def tela_liquidar_operacao():
    """Tela para liquidar uma operação."""
    cabecalho("LIQUIDAR OPERAÇÃO")

    # Mostrar operações abertas
    operacoes = listar_operacoes(status="ABERTO")

    if not operacoes:
        print("Nenhuma operação em aberto.")
        pausar()
        return

    print(f"{'ID':<5} {'TIPO':<7} {'EMPRESA':<20} {'VALOR':>15} {'VENCIMENTO':<12}")
    print("-" * 65)
    for op in operacoes:
        print(f"{op.id:<5} {op.tipo:<7} {op.empresa_nome[:20]:<20} {formatar_moeda(op.valor):>15} {formatar_data(op.data_vencimento):<12}")

    print()
    op_id = input_inteiro("ID da operação a liquidar (0 para cancelar): ", minimo=0)
    if op_id == 0:
        return

    operacao = buscar_operacao(op_id)
    if not operacao or operacao.status != "ABERTO":
        print("Operação não encontrada ou já liquidada!")
        pausar()
        return

    print(f"\nOperação: {operacao.tipo} - {operacao.empresa_nome} - {formatar_moeda(operacao.valor)}")

    if confirmar("Confirma liquidação? (S/N): "):
        if liquidar_operacao(op_id):
            print("Operação liquidada com sucesso!")
        else:
            print("Erro ao liquidar operação.")

    pausar()


def tela_cancelar_operacao():
    """Tela para cancelar uma operação."""
    cabecalho("CANCELAR OPERAÇÃO")

    operacoes = listar_operacoes(status="ABERTO")

    if not operacoes:
        print("Nenhuma operação em aberto.")
        pausar()
        return

    print(f"{'ID':<5} {'TIPO':<7} {'EMPRESA':<20} {'VALOR':>15}")
    print("-" * 50)
    for op in operacoes:
        print(f"{op.id:<5} {op.tipo:<7} {op.empresa_nome[:20]:<20} {formatar_moeda(op.valor):>15}")

    print()
    op_id = input_inteiro("ID da operação a cancelar (0 para voltar): ", minimo=0)
    if op_id == 0:
        return

    operacao = buscar_operacao(op_id)
    if not operacao or operacao.status != "ABERTO":
        print("Operação não encontrada ou não pode ser cancelada!")
        pausar()
        return

    print(f"\nOperação: {operacao.tipo} - {operacao.empresa_nome} - {formatar_moeda(operacao.valor)}")

    if confirmar("ATENÇÃO: Esta ação não pode ser desfeita. Confirma? (S/N): "):
        if cancelar_operacao(op_id):
            print("Operação cancelada com sucesso!")
        else:
            print("Erro ao cancelar operação.")

    pausar()


# ==================== FINANCEIRO ====================

def menu_financeiro():
    """Menu financeiro."""
    while True:
        cabecalho("FINANCEIRO")
        print("  1. Resumo Financeiro")
        print("  2. Contas a Pagar")
        print("  3. Contas a Receber")
        print("  4. Contas Vencidas")
        print()
        print("  0. Voltar")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            tela_resumo_financeiro()
        elif opcao == "2":
            tela_contas_a_pagar()
        elif opcao == "3":
            tela_contas_a_receber()
        elif opcao == "4":
            tela_contas_vencidas()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            pausar()


def tela_resumo_financeiro():
    """Tela de resumo financeiro."""
    cabecalho("RESUMO FINANCEIRO")

    resumo = resumo_financeiro()

    print(f"  Total a Pagar:    {formatar_moeda(resumo['total_a_pagar']):>20}")
    print(f"  Total a Receber:  {formatar_moeda(resumo['total_a_receber']):>20}")
    print("-" * 45)
    print(f"  Saldo Projetado:  {formatar_moeda(resumo['saldo_projetado']):>20}")
    print()

    if resumo['vencidas_qtd'] > 0:
        print(f"  ATENÇÃO: {resumo['vencidas_qtd']} operação(ões) vencida(s)")
        print(f"           Valor: {formatar_moeda(resumo['vencidas_valor'])}")

    pausar()


def tela_contas_a_pagar():
    """Tela de contas a pagar."""
    cabecalho("CONTAS A PAGAR")

    contas = listar_contas_a_pagar()

    if not contas:
        print("Nenhuma conta a pagar em aberto.")
    else:
        total = 0
        print(f"{'ID':<5} {'EMPRESA':<25} {'VALOR':>15} {'VENCIMENTO':<12}")
        print("-" * 60)
        for conta in contas:
            print(f"{conta.id:<5} {conta.empresa_nome[:25]:<25} {formatar_moeda(conta.valor):>15} {formatar_data(conta.data_vencimento):<12}")
            total += conta.valor
        print("-" * 60)
        print(f"{'TOTAL:':<31} {formatar_moeda(total):>15}")

    pausar()


def tela_contas_a_receber():
    """Tela de contas a receber."""
    cabecalho("CONTAS A RECEBER")

    contas = listar_contas_a_receber()

    if not contas:
        print("Nenhuma conta a receber em aberto.")
    else:
        total = 0
        print(f"{'ID':<5} {'EMPRESA':<25} {'VALOR':>15} {'VENCIMENTO':<12}")
        print("-" * 60)
        for conta in contas:
            print(f"{conta.id:<5} {conta.empresa_nome[:25]:<25} {formatar_moeda(conta.valor):>15} {formatar_data(conta.data_vencimento):<12}")
            total += conta.valor
        print("-" * 60)
        print(f"{'TOTAL:':<31} {formatar_moeda(total):>15}")

    pausar()


def tela_contas_vencidas():
    """Tela de contas vencidas."""
    cabecalho("CONTAS VENCIDAS")

    contas = listar_vencidas()

    if not contas:
        print("Nenhuma conta vencida. Parabéns!")
    else:
        total = 0
        print(f"{'ID':<5} {'TIPO':<7} {'EMPRESA':<20} {'VALOR':>15} {'VENCIMENTO':<12}")
        print("-" * 65)
        for conta in contas:
            print(f"{conta.id:<5} {conta.tipo:<7} {conta.empresa_nome[:20]:<20} {formatar_moeda(conta.valor):>15} {formatar_data(conta.data_vencimento):<12}")
            total += conta.valor
        print("-" * 65)
        print(f"{'TOTAL:':<33} {formatar_moeda(total):>15}")

    pausar()


# ==================== RELATÓRIOS ====================

def menu_relatorios():
    """Menu de relatórios."""
    while True:
        cabecalho("RELATÓRIOS")
        print("  1. Histórico de Operações")
        print("  2. Exportar para Excel (em breve)")
        print()
        print("  0. Voltar")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            tela_historico()
        elif opcao == "2":
            print("\nFuncionalidade em desenvolvimento...")
            pausar()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            pausar()


def tela_historico():
    """Tela de histórico completo de operações."""
    cabecalho("HISTÓRICO DE OPERAÇÕES")

    operacoes = listar_operacoes()

    if not operacoes:
        print("Nenhuma operação registrada.")
    else:
        print(f"{'ID':<5} {'DATA':<12} {'TIPO':<7} {'EMPRESA':<18} {'VALOR':>14} {'STATUS':<10}")
        print("-" * 70)
        for op in operacoes:
            print(f"{op.id:<5} {formatar_data(op.data_operacao):<12} {op.tipo:<7} {op.empresa_nome[:18]:<18} {formatar_moeda(op.valor):>14} {op.status:<10}")

    pausar()
