"""
Serviço de operações: cadastro de empresas e registro de compra/venda.
"""
from datetime import date, timedelta
from typing import List, Optional

from database import get_connection
from models import Empresa, Operacao


# ==================== EMPRESAS ====================

def cadastrar_empresa(nome: str, cnpj: Optional[str] = None) -> int:
    """Cadastra uma nova empresa e retorna o ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO empresas (nome, cnpj) VALUES (?, ?)',
        (nome.upper(), cnpj)
    )
    conn.commit()
    empresa_id = cursor.lastrowid
    conn.close()
    return empresa_id


def listar_empresas(apenas_ativas: bool = True) -> List[Empresa]:
    """Lista todas as empresas cadastradas."""
    conn = get_connection()
    cursor = conn.cursor()

    if apenas_ativas:
        cursor.execute('SELECT * FROM empresas WHERE ativo = 1 ORDER BY nome')
    else:
        cursor.execute('SELECT * FROM empresas ORDER BY nome')

    rows = cursor.fetchall()
    conn.close()

    return [Empresa(
        id=row['id'],
        nome=row['nome'],
        cnpj=row['cnpj'],
        ativo=bool(row['ativo']),
        criado_em=row['criado_em']
    ) for row in rows]


def buscar_empresa(empresa_id: int) -> Optional[Empresa]:
    """Busca uma empresa pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM empresas WHERE id = ?', (empresa_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Empresa(
            id=row['id'],
            nome=row['nome'],
            cnpj=row['cnpj'],
            ativo=bool(row['ativo']),
            criado_em=row['criado_em']
        )
    return None


def desativar_empresa(empresa_id: int) -> bool:
    """Desativa uma empresa (não exclui do banco)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE empresas SET ativo = 0 WHERE id = ?', (empresa_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


# ==================== OPERAÇÕES ====================

def registrar_operacao(
    tipo: str,
    empresa_id: int,
    valor: float,
    prazo_dias: int = 7,
    descricao: Optional[str] = None,
    data_operacao: Optional[date] = None,
    observacao: Optional[str] = None
) -> int:
    """
    Registra uma nova operação de compra ou venda.
    Retorna o ID da operação criada.
    """
    if tipo not in ('COMPRA', 'VENDA'):
        raise ValueError("Tipo deve ser COMPRA ou VENDA")

    if data_operacao is None:
        data_operacao = date.today()

    data_vencimento = data_operacao + timedelta(days=prazo_dias)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO operacoes
        (tipo, empresa_id, descricao, valor, prazo_dias, data_operacao, data_vencimento, observacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tipo, empresa_id, descricao, valor, prazo_dias,
          data_operacao.isoformat(), data_vencimento.isoformat(), observacao))

    conn.commit()
    operacao_id = cursor.lastrowid
    conn.close()
    return operacao_id


def listar_operacoes(
    status: Optional[str] = None,
    tipo: Optional[str] = None,
    empresa_id: Optional[int] = None
) -> List[Operacao]:
    """Lista operações com filtros opcionais."""
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT o.*, e.nome as empresa_nome
        FROM operacoes o
        JOIN empresas e ON o.empresa_id = e.id
        WHERE 1=1
    '''
    params = []

    if status:
        query += ' AND o.status = ?'
        params.append(status)

    if tipo:
        query += ' AND o.tipo = ?'
        params.append(tipo)

    if empresa_id:
        query += ' AND o.empresa_id = ?'
        params.append(empresa_id)

    query += ' ORDER BY o.data_vencimento'

    cursor.execute(query, params)
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


def buscar_operacao(operacao_id: int) -> Optional[Operacao]:
    """Busca uma operação pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.*, e.nome as empresa_nome
        FROM operacoes o
        JOIN empresas e ON o.empresa_id = e.id
        WHERE o.id = ?
    ''', (operacao_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Operacao(
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
        )
    return None


def liquidar_operacao(operacao_id: int, data_liquidacao: Optional[date] = None) -> bool:
    """Marca uma operação como liquidada."""
    if data_liquidacao is None:
        data_liquidacao = date.today()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE operacoes
        SET status = 'LIQUIDADO', data_liquidacao = ?
        WHERE id = ? AND status = 'ABERTO'
    ''', (data_liquidacao.isoformat(), operacao_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def cancelar_operacao(operacao_id: int) -> bool:
    """Cancela uma operação aberta."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE operacoes
        SET status = 'CANCELADO'
        WHERE id = ? AND status = 'ABERTO'
    ''', (operacao_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
