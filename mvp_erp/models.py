"""
Estruturas de dados (dataclasses) para o sistema ERP.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List


@dataclass
class Empresa:
    id: Optional[int] = None
    nome: str = ""
    cnpj: Optional[str] = None
    ativo: bool = True
    criado_em: Optional[datetime] = None


@dataclass
class Operacao:
    id: Optional[int] = None
    tipo: str = ""  # COMPRA ou VENDA
    empresa_id: int = 0
    descricao: Optional[str] = None
    valor: float = 0.0
    prazo_dias: int = 7
    data_operacao: Optional[date] = None
    data_vencimento: Optional[date] = None
    data_liquidacao: Optional[date] = None
    status: str = "ABERTO"  # ABERTO, LIQUIDADO, CANCELADO
    observacao: Optional[str] = None
    criado_em: Optional[datetime] = None
    # Campo auxiliar para exibição
    empresa_nome: Optional[str] = None


@dataclass
class ItemPedido:
    id: Optional[int] = None
    pedido_id: int = 0
    tipo_embalagem: str = ""   # AGRANEL, BAG, FARDO_30x1, FARDO_10x1
    quantidade: float = 0.0    # kg para AGRANEL, unidades para os demais
    peso_por_unidade: float = 1.0  # kg por unidade (1 para AGRANEL)
    peso_kg: float = 0.0       # peso total calculado
    preco_unitario: float = 0.0  # preço por kg
    icms: bool = False          # True = com ICMS 12%
    valor_total: float = 0.0   # calculado


@dataclass
class Pedido:
    id: Optional[int] = None
    empresa_id: int = 0
    empresa_nome: Optional[str] = None
    data_pedido: Optional[date] = None
    prazo_dias: int = 7
    data_prevista_entrega: Optional[date] = None
    status: str = "ABERTO"    # ABERTO, BAIXADO, CANCELADO
    placa: Optional[str] = None
    data_baixa: Optional[date] = None
    observacao: Optional[str] = None
    criado_em: Optional[datetime] = None
    itens: List[ItemPedido] = field(default_factory=list)
    # Campos calculados para exibição
    peso_total_kg: float = 0.0
    valor_total: float = 0.0
