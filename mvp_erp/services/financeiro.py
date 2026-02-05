"""
Serviço financeiro: contas a pagar e contas a receber.

Regra de negócio:
- COMPRA gera conta a PAGAR (saída de dinheiro)
- VENDA gera conta a RECEBER (entrada de dinheiro)
"""
from datetime import date
from typing import List, Dict

from database import get_connection
from models import Operacao


def listar_contas_a_pagar(apenas_abertas: bool = True) -> List[Operacao]:
    """
    Lista contas a pagar (operações de COMPRA).
    Compras representam saída de dinheiro.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT o.*, e.nome as empresa_nome
        FROM operacoes o
        JOIN empresas e ON o.empresa_id = e.id
        WHERE o.tipo = 'COMPRA'
    '''

    if apenas_abertas:
        query += " AND o.status = 'ABERTO'"

    query += ' ORDER BY o.data_vencimento'

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [Operacao(
        id=row['id'],
        tipo=row['tipo'],
        empresa_id=row['empresa_id'],
        descricao=row['descricao'],
        valor=row['valor'],
        prazo_dias=row['prazo_dias'],
        data_operacao=row['data_operacao'],
        data_vencimento=row['data_vencimento'],
        data_liquidacao=row['data_liquidacao'],
        status=row['status'],
        observacao=row['observacao'],
        criado_em=row['criado_em'],
        empresa_nome=row['empresa_nome']
    ) for row in rows]


def listar_contas_a_receber(apenas_abertas: bool = True) -> List[Operacao]:
    """
    Lista contas a receber (operações de VENDA).
    Vendas representam entrada de dinheiro.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT o.*, e.nome as empresa_nome
        FROM operacoes o
        JOIN empresas e ON o.empresa_id = e.id
        WHERE o.tipo = 'VENDA'
    '''

    if apenas_abertas:
        query += " AND o.status = 'ABERTO'"

    query += ' ORDER BY o.data_vencimento'

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [Operacao(
        id=row['id'],
        tipo=row['tipo'],
        empresa_id=row['empresa_id'],
        descricao=row['descricao'],
        valor=row['valor'],
        prazo_dias=row['prazo_dias'],
        data_operacao=row['data_operacao'],
        data_vencimento=row['data_vencimento'],
        data_liquidacao=row['data_liquidacao'],
        status=row['status'],
        observacao=row['observacao'],
        criado_em=row['criado_em'],
        empresa_nome=row['empresa_nome']
    ) for row in rows]


def listar_vencidas() -> List[Operacao]:
    """Lista todas as operações vencidas (data de vencimento < hoje)."""
    hoje = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT o.*, e.nome as empresa_nome
        FROM operacoes o
        JOIN empresas e ON o.empresa_id = e.id
        WHERE o.status = 'ABERTO' AND o.data_vencimento < ?
        ORDER BY o.data_vencimento
    ''', (hoje,))

    rows = cursor.fetchall()
    conn.close()

    return [Operacao(
        id=row['id'],
        tipo=row['tipo'],
        empresa_id=row['empresa_id'],
        descricao=row['descricao'],
        valor=row['valor'],
        prazo_dias=row['prazo_dias'],
        data_operacao=row['data_operacao'],
        data_vencimento=row['data_vencimento'],
        data_liquidacao=row['data_liquidacao'],
        status=row['status'],
        observacao=row['observacao'],
        criado_em=row['criado_em'],
        empresa_nome=row['empresa_nome']
    ) for row in rows]


def resumo_financeiro() -> Dict:
    """
    Retorna um resumo financeiro:
    - Total a pagar (compras abertas)
    - Total a receber (vendas abertas)
    - Saldo projetado
    - Operações vencidas
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total a pagar
    cursor.execute('''
        SELECT COALESCE(SUM(valor), 0) as total
        FROM operacoes
        WHERE tipo = 'COMPRA' AND status = 'ABERTO'
    ''')
    total_pagar = cursor.fetchone()['total']

    # Total a receber
    cursor.execute('''
        SELECT COALESCE(SUM(valor), 0) as total
        FROM operacoes
        WHERE tipo = 'VENDA' AND status = 'ABERTO'
    ''')
    total_receber = cursor.fetchone()['total']

    # Vencidas
    hoje = date.today().isoformat()
    cursor.execute('''
        SELECT COUNT(*) as qtd, COALESCE(SUM(valor), 0) as total
        FROM operacoes
        WHERE status = 'ABERTO' AND data_vencimento < ?
    ''', (hoje,))
    vencidas = cursor.fetchone()

    conn.close()

    return {
        'total_a_pagar': total_pagar,
        'total_a_receber': total_receber,
        'saldo_projetado': total_receber - total_pagar,
        'vencidas_qtd': vencidas['qtd'],
        'vencidas_valor': vencidas['total']
    }
