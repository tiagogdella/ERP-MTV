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
from services.pedidos import (
    cadastrar_pedido, adicionar_item_pedido,
    listar_pedidos, buscar_pedido,
    atualizar_data_entrega, baixar_pedido,
    PESO_POR_EMBALAGEM, LABEL_EMBALAGEM
)


def menu_principal():
    """Menu principal do sistema."""
    while True:
        cabecalho("ERP MVP - MENU PRINCIPAL")
        print("  1. Cadastros")
        print("  2. Operações (Compra/Venda)")
        print("  3. Financeiro")
        print("  4. Relatórios")
        print("  5. Pedidos ")
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
        elif opcao == "5":
            menu_pedidos()
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


# ==================== PEDIDOS ====================

def menu_pedidos():
    """Menu de pedidos."""
    while True:
        cabecalho("PEDIDOS")
        print("  1. Cadastrar Pedido")
        print("  2. Consultar Pedidos")
        print("  3. Baixa de Pedido (carregado)")
        print()
        print("  0. Voltar")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            tela_cadastrar_pedido()
        elif opcao == "2":
            tela_consultar_pedidos()
        elif opcao == "3":
            tela_baixar_pedido()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            pausar()


def _selecionar_embalagem() -> tuple:
    """
    Solicita tipo de embalagem e retorna (tipo, quantidade_kg, peso_por_unidade).
    AGRANEL e BAG: faturados em kg — quantidade é diretamente o peso em kg.
    FARDO_30x1 e FARDO_10x1: quantidade é número de fardos, peso calculado.
    """
    tipos = list(PESO_POR_EMBALAGEM.keys())
    print()
    print("  Tipo de embalagem:")
    for i, t in enumerate(tipos, 1):
        print(f"    {i}. {LABEL_EMBALAGEM[t]}")
    print()

    idx = input_inteiro("  Tipo (número): ", minimo=1, maximo=len(tipos))
    tipo = tipos[idx - 1]

    if tipo in ("AGRANEL", "BAG"):
        # Faturado em kg — entrada direta em kg
        qtd_kg = input_valor("  Quantidade (kg): ")
        return tipo, qtd_kg, 1.0

    elif tipo == "FARDO_30x1":
        qtd = input_inteiro("  Número de fardos: ", minimo=1)
        peso_uni = 30.0
        print(f"  Peso por fardo: {peso_uni} kg  |  Total: {qtd * peso_uni:.2f} kg")
        return tipo, float(qtd), peso_uni

    else:  # FARDO_10x1
        qtd = input_inteiro("  Número de fardos: ", minimo=1)
        peso_uni = 10.0
        print(f"  Peso por fardo: {peso_uni} kg  |  Total: {qtd * peso_uni:.2f} kg")
        return tipo, float(qtd), peso_uni


def tela_cadastrar_pedido():
    """Tela de cadastro de pedido com múltiplos itens."""
    cabecalho("CADASTRAR PEDIDO")

    # Selecionar cliente
    empresas = listar_empresas()
    if not empresas:
        print("Cadastre um cliente primeiro!")
        pausar()
        return

    print("Clientes disponíveis:")
    for emp in empresas:
        print(f"  {emp.id}. {emp.nome}")
    print()

    empresa_id = input_inteiro("ID do cliente: ", minimo=1)
    empresa = buscar_empresa(empresa_id)
    if not empresa:
        print("Cliente não encontrado!")
        pausar()
        return

    prazo = input_inteiro("Prazo (dias): ", minimo=1)
    data_entrega = input_data("Data prevista de entrega (DD/MM/AAAA): ", permitir_vazio=False)
    observacao = input("Observação (opcional): ").strip() or None

    # Criar o pedido
    try:
        pedido_id = cadastrar_pedido(empresa_id, prazo, data_entrega, observacao)
    except Exception as e:
        print(f"\nErro ao criar pedido: {e}")
        pausar()
        return

    # Loop para adicionar itens
    itens_adicionados = []
    print()
    print("--- ITENS DO PEDIDO ---")
    print("Adicione os itens. Ao terminar, responda N ao adicionar outro.")

    while True:
        print(f"\n  Item #{len(itens_adicionados) + 1}")

        tipo, qtd, peso_uni = _selecionar_embalagem()

        preco = input_valor("  Preço unitário por kg (R$): ")

        print("  Incidência de ICMS:")
        print("    1. Com ICMS (12%)")
        print("    2. Sem ICMS")
        icms_op = input("  Opção [2]: ").strip() or "2"
        icms = icms_op == "1"

        peso_total = qtd * peso_uni
        valor_base = peso_total * preco
        valor_item = valor_base * 1.12 if icms else valor_base

        lbl = LABEL_EMBALAGEM[tipo]
        qtde_fmt = f"{qtd:.2f} kg" if tipo in ("AGRANEL", "BAG") else f"{qtd:.0f} unid."
        print(f"\n  Resumo do item:")
        print(f"    Embalagem:  {lbl}")
        print(f"    Quantidade: {qtde_fmt}")
        print(f"    Peso total: {peso_total:.2f} kg")
        print(f"    Preço/kg:   {formatar_moeda(preco)}")
        print(f"    ICMS:       {'Sim (12%)' if icms else 'Não'}")
        print(f"    Valor item: {formatar_moeda(valor_item)}")

        if confirmar("  Confirmar item? (S/N): "):
            try:
                adicionar_item_pedido(pedido_id, tipo, qtd, peso_uni, preco, icms)
                itens_adicionados.append(valor_item)
                print(f"  Item adicionado! Total parcial: {formatar_moeda(sum(itens_adicionados))}")
            except Exception as e:
                print(f"  Erro ao adicionar item: {e}")

        continuar = input("\nAdicionar outro item? (S/N) [N]: ").strip().upper()
        if continuar != "S":
            break

    if not itens_adicionados:
        print("\nAVISO: Pedido criado sem itens.")

    print(f"\nPedido #{pedido_id} cadastrado com sucesso!")
    print(f"  Cliente:          {empresa.nome}")
    print(f"  Prazo:            {prazo} dias")
    print(f"  Entrega prevista: {formatar_data(data_entrega)}")
    print(f"  Itens:            {len(itens_adicionados)}")
    if itens_adicionados:
        print(f"  Valor total:      {formatar_moeda(sum(itens_adicionados))}")

    pausar()


def _exibir_pedido_detalhado(pedido):
    """Imprime os detalhes completos de um pedido."""
    print(f"\n{'='*52}")
    print(f"  Pedido #: {pedido.id}    Status: {pedido.status}")
    print(f"  Cliente:  {pedido.empresa_nome}")
    print(f"  Data:     {formatar_data(pedido.data_pedido)}")
    print(f"  Prazo:    {pedido.prazo_dias} dias")
    print(f"  Entrega:  {formatar_data(pedido.data_prevista_entrega)}")
    if pedido.status == "BAIXADO":
        print(f"  Placa:    {pedido.placa or '-'}")
        print(f"  Baixa:    {formatar_data(pedido.data_baixa)}")
    if pedido.observacao:
        print(f"  Obs:      {pedido.observacao}")

    if pedido.itens:
        print(f"\n  {'#':<3} {'EMBALAGEM':<16} {'QUANTIDADE':>12} {'PESO KG':>9} {'R$/KG':>10} {'ICMS':<6} {'TOTAL':>14}")
        print(f"  {'-'*74}")
        for i, item in enumerate(pedido.itens, 1):
            lbl = LABEL_EMBALAGEM.get(item.tipo_embalagem, item.tipo_embalagem)[:15]
            if item.tipo_embalagem in ("AGRANEL", "BAG"):
                qtde_fmt = f"{item.quantidade:.2f} kg"
            else:
                qtde_fmt = f"{item.quantidade:.0f} unid."
            icms_txt = "Sim" if item.icms else "Não"
            print(
                f"  {i:<3} {lbl:<16} {qtde_fmt:>12} {item.peso_kg:>9.2f} "
                f"{formatar_moeda(item.preco_unitario):>10} {icms_txt:<6} "
                f"{formatar_moeda(item.valor_total):>14}"
            )
        print(f"  {'-'*74}")
        print(
            f"  {'TOTAL':<20} {'':>12} {pedido.peso_total_kg:>9.2f} "
            f"{'':>10} {'':>6} {formatar_moeda(pedido.valor_total):>14}"
        )
    else:
        print("\n  (sem itens)")
    print(f"{'='*52}")


def tela_consultar_pedidos():
    """Tela de consulta de pedidos."""
    while True:
        cabecalho("CONSULTAR PEDIDOS")
        print("  1. Todos os pedidos")
        print("  2. Por cliente")
        print("  3. Detalhar pedido por ID")
        print("  4. Alterar data prevista de entrega")
        print()
        print("  0. Voltar")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "1":
            _tela_listar_pedidos()
        elif opcao == "2":
            _tela_listar_pedidos_por_cliente()
        elif opcao == "3":
            _tela_detalhar_pedido()
        elif opcao == "4":
            _tela_alterar_data_entrega()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            pausar()


def _tela_listar_pedidos(empresa_id=None, titulo="TODOS OS PEDIDOS"):
    """Lista pedidos em formato tabela."""
    cabecalho(titulo)

    print("  Filtrar por status:")
    print("    1. Abertos")
    print("    2. Baixados")
    print("    3. Todos")
    filtro = input("  Opção [3]: ").strip() or "3"
    status_map = {"1": "ABERTO", "2": "BAIXADO"}
    status = status_map.get(filtro)

    pedidos = listar_pedidos(empresa_id=empresa_id, status=status)

    limpar_tela()
    cabecalho(titulo)

    if not pedidos:
        print("Nenhum pedido encontrado.")
    else:
        print(f"{'ID':<5} {'CLIENTE':<22} {'DATA':^12} {'ENTREGA':^12} {'KG TOTAL':>10} {'VALOR TOTAL':>14} {'STATUS':<8}")
        print("-" * 87)
        for p in pedidos:
            print(
                f"{p.id:<5} {(p.empresa_nome or '')[:22]:<22} "
                f"{formatar_data(p.data_pedido):^12} "
                f"{formatar_data(p.data_prevista_entrega):^12} "
                f"{p.peso_total_kg:>10.2f} "
                f"{formatar_moeda(p.valor_total):>14} "
                f"{p.status:<8}"
            )

    pausar()


def _tela_listar_pedidos_por_cliente():
    """Lista pedidos filtrando por cliente."""
    cabecalho("PEDIDOS POR CLIENTE")

    empresas = listar_empresas()
    if not empresas:
        print("Nenhum cliente cadastrado.")
        pausar()
        return

    print("Clientes:")
    for emp in empresas:
        print(f"  {emp.id}. {emp.nome}")
    print()

    empresa_id = input_inteiro("ID do cliente (0 para cancelar): ", minimo=0)
    if empresa_id == 0:
        return

    empresa = buscar_empresa(empresa_id)
    if not empresa:
        print("Cliente não encontrado!")
        pausar()
        return

    _tela_listar_pedidos(empresa_id=empresa_id,
                         titulo=f"PEDIDOS - {empresa.nome.upper()}")


def _tela_detalhar_pedido():
    """Exibe detalhes completos de um pedido."""
    cabecalho("DETALHAR PEDIDO")

    pedido_id = input_inteiro("ID do pedido (0 para cancelar): ", minimo=0)
    if pedido_id == 0:
        return

    pedido = buscar_pedido(pedido_id)
    if not pedido:
        print("Pedido não encontrado!")
        pausar()
        return

    _exibir_pedido_detalhado(pedido)
    pausar()


def _tela_alterar_data_entrega():
    """Altera a data prevista de entrega de um pedido."""
    cabecalho("ALTERAR DATA DE ENTREGA")

    pedido_id = input_inteiro("ID do pedido (0 para cancelar): ", minimo=0)
    if pedido_id == 0:
        return

    pedido = buscar_pedido(pedido_id)
    if not pedido:
        print("Pedido não encontrado!")
        pausar()
        return

    print(f"\nPedido #: {pedido.id} — {pedido.empresa_nome}")
    print(f"Data prevista atual: {formatar_data(pedido.data_prevista_entrega)}")
    print()

    nova_data = input_data("Nova data prevista de entrega (DD/MM/AAAA): ")

    if confirmar(f"Alterar para {formatar_data(nova_data)}? (S/N): "):
        if atualizar_data_entrega(pedido_id, nova_data):
            print("Data atualizada com sucesso!")
        else:
            print("Erro ao atualizar a data.")

    pausar()


def tela_baixar_pedido():
    """Tela de baixa de pedido (carregamento realizado)."""
    cabecalho("BAIXA DE PEDIDO")

    pedidos = listar_pedidos(status="ABERTO")
    if not pedidos:
        print("Nenhum pedido em aberto para baixar.")
        pausar()
        return

    print(f"{'ID':<5} {'CLIENTE':<25} {'ENTREGA':^12} {'KG TOTAL':>10} {'VALOR TOTAL':>14}")
    print("-" * 70)
    for p in pedidos:
        print(
            f"{p.id:<5} {(p.empresa_nome or '')[:25]:<25} "
            f"{formatar_data(p.data_prevista_entrega):^12} "
            f"{p.peso_total_kg:>10.2f} "
            f"{formatar_moeda(p.valor_total):>14}"
        )

    print()
    pedido_id = input_inteiro("ID do pedido a baixar (0 para cancelar): ", minimo=0)
    if pedido_id == 0:
        return

    pedido = buscar_pedido(pedido_id)
    if not pedido or pedido.status != "ABERTO":
        print("Pedido não encontrado ou já baixado!")
        pausar()
        return

    _exibir_pedido_detalhado(pedido)

    print()
    placa = input("Placa do veículo: ").strip().upper()
    if not placa:
        print("Placa é obrigatória!")
        pausar()
        return

    from datetime import date as _date
    print(f"\n  Data da baixa: {formatar_data(_date.today())}")
    print(f"  Placa:         {placa}")

    if confirmar("\nConfirmar baixa do pedido? (S/N): "):
        if baixar_pedido(pedido_id, placa):
            print(f"\nPedido #{pedido_id} baixado com sucesso!")
        else:
            print("Erro ao realizar baixa do pedido.")

    pausar()
