"""
Serviço de pedidos do ERP.
Gerencia cadastro, consulta e baixa de pedidos com itens.
"""
from datetime import date, datetime
from typing import Optional, List

from database import get_connection
from models import Pedido, ItemPedido

# Pesos padrão por tipo de embalagem (kg por unidade)
PESO_POR_EMBALAGEM = {
    "AGRANEL":    1.0,    # quantidade já é em kg
    "BAG":        None,   # peso variável, informado pelo usuário
    "FARDO_30x1": 30.0,   # 30 pacotes de 1kg
    "FARDO_10x1": 10.0,   # 10 pacotes de 1kg
}

LABEL_EMBALAGEM = {
    "AGRANEL":    "A Granel (kg)",
    "BAG":        "Big Bag",
    "FARDO_30x1": "Fardo 30x1 (30 kg/fardo)",
    "FARDO_10x1": "Fardo 10x1 (10 kg/fardo)",
}


def calcular_item(tipo_embalagem: str, quantidade: float,
                  peso_por_unidade: float, preco_unitario: float,
                  icms: bool) -> dict:
    """Calcula peso total e valor de um item."""
    peso_kg = quantidade * peso_por_unidade
    valor_base = peso_kg * preco_unitario
    valor_total = valor_base * 1.12 if icms else valor_base
    return {"peso_kg": peso_kg, "valor_total": valor_total}


def cadastrar_pedido(empresa_id: int, prazo_dias: int,
                     data_prevista_entrega: Optional[date],
                     observacao: Optional[str] = None) -> int:
    """Cria um novo pedido e retorna seu ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pedidos
            (empresa_id, data_pedido, prazo_dias, data_prevista_entrega, observacao)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        empresa_id,
        date.today().isoformat(),
        prazo_dias,
        data_prevista_entrega.isoformat() if data_prevista_entrega else None,
        observacao,
    ))
    pedido_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pedido_id


def adicionar_item_pedido(pedido_id: int, tipo_embalagem: str,
                          quantidade: float, peso_por_unidade: float,
                          preco_unitario: float, icms: bool) -> int:
    """Adiciona um item a um pedido existente e retorna o ID do item."""
    calc = calcular_item(tipo_embalagem, quantidade, peso_por_unidade,
                         preco_unitario, icms)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO itens_pedido
            (pedido_id, tipo_embalagem, quantidade, peso_por_unidade,
             peso_kg, preco_unitario, icms, valor_total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pedido_id,
        tipo_embalagem,
        quantidade,
        peso_por_unidade,
        calc["peso_kg"],
        preco_unitario,
        1 if icms else 0,
        calc["valor_total"],
    ))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id


def _montar_pedido(row, itens_rows) -> Pedido:
    """Constrói um objeto Pedido a partir das linhas do banco."""
    itens = []
    peso_total = 0.0
    valor_total = 0.0
    for i in itens_rows:
        item = ItemPedido(
            id=i["id"],
            pedido_id=i["pedido_id"],
            tipo_embalagem=i["tipo_embalagem"],
            quantidade=i["quantidade"],
            peso_por_unidade=i["peso_por_unidade"],
            peso_kg=i["peso_kg"],
            preco_unitario=i["preco_unitario"],
            icms=bool(i["icms"]),
            valor_total=i["valor_total"],
        )
        itens.append(item)
        peso_total += item.peso_kg
        valor_total += item.valor_total

    return Pedido(
        id=row["id"],
        empresa_id=row["empresa_id"],
        empresa_nome=row["empresa_nome"],
        data_pedido=row["data_pedido"],
        prazo_dias=row["prazo_dias"],
        data_prevista_entrega=row["data_prevista_entrega"],
        status=row["status"],
        placa=row["placa"],
        data_baixa=row["data_baixa"],
        observacao=row["observacao"],
        criado_em=row["criado_em"],
        itens=itens,
        peso_total_kg=peso_total,
        valor_total=valor_total,
    )


def listar_pedidos(empresa_id: Optional[int] = None,
                   status: Optional[str] = None) -> List[Pedido]:
    """Lista pedidos com filtros opcionais."""
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT p.*, e.nome AS empresa_nome
        FROM pedidos p
        JOIN empresas e ON e.id = p.empresa_id
        WHERE 1=1
    '''
    params = []
    if empresa_id:
        query += " AND p.empresa_id = ?"
        params.append(empresa_id)
    if status:
        query += " AND p.status = ?"
        params.append(status)
    query += " ORDER BY p.id DESC"

    cursor.execute(query, params)
    pedido_rows = cursor.fetchall()

    pedidos = []
    for row in pedido_rows:
        cursor.execute(
            "SELECT * FROM itens_pedido WHERE pedido_id = ?", (row["id"],)
        )
        itens_rows = cursor.fetchall()
        pedidos.append(_montar_pedido(row, itens_rows))

    conn.close()
    return pedidos


def buscar_pedido(pedido_id: int) -> Optional[Pedido]:
    """Busca um pedido pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.*, e.nome AS empresa_nome
        FROM pedidos p
        JOIN empresas e ON e.id = p.empresa_id
        WHERE p.id = ?
    ''', (pedido_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    cursor.execute(
        "SELECT * FROM itens_pedido WHERE pedido_id = ?", (pedido_id,)
    )
    itens_rows = cursor.fetchall()
    pedido = _montar_pedido(row, itens_rows)
    conn.close()
    return pedido


def atualizar_data_entrega(pedido_id: int, nova_data: date) -> bool:
    """Atualiza a data prevista de entrega de um pedido."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pedidos SET data_prevista_entrega = ? WHERE id = ?",
        (nova_data.isoformat(), pedido_id)
    )
    atualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return atualizado


def baixar_pedido(pedido_id: int, placa: str) -> bool:
    """Registra a baixa (carregamento) de um pedido."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE pedidos
           SET status = 'BAIXADO', placa = ?, data_baixa = ?
           WHERE id = ? AND status = 'ABERTO'
        ''',
        (placa.upper().strip(), date.today().isoformat(), pedido_id)
    )
    atualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return atualizado
