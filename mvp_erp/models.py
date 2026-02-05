"""
Estruturas de dados (dataclasses) para o sistema ERP.
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


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
