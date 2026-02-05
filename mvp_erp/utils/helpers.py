"""
Funções utilitárias para o sistema ERP.
"""
from datetime import datetime, date
import os


def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def formatar_moeda(valor: float) -> str:
    """Formata um valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data(data) -> str:
    """Formata uma data para exibição (DD/MM/AAAA)."""
    if data is None:
        return "-"
    if isinstance(data, str):
        try:
            data = datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            return data
    return data.strftime("%d/%m/%Y")


def parse_data(data_str: str) -> date:
    """
    Converte string de data para objeto date.
    Aceita formatos: DD/MM/AAAA ou AAAA-MM-DD
    """
    data_str = data_str.strip()

    if "/" in data_str:
        return datetime.strptime(data_str, "%d/%m/%Y").date()
    elif "-" in data_str:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    else:
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA")


def input_valor(prompt: str = "Valor: ") -> float:
    """Solicita um valor numérico ao usuário."""
    while True:
        try:
            valor_str = input(prompt).strip()
            # Remove formatação brasileira se houver
            valor_str = valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
            valor = float(valor_str)
            if valor <= 0:
                print("O valor deve ser maior que zero.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Digite apenas números.")


def input_inteiro(prompt: str, minimo: int = None, maximo: int = None) -> int:
    """Solicita um número inteiro ao usuário."""
    while True:
        try:
            valor = int(input(prompt).strip())
            if minimo is not None and valor < minimo:
                print(f"O valor deve ser no mínimo {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"O valor deve ser no máximo {maximo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def input_data(prompt: str = "Data (DD/MM/AAAA): ", permitir_vazio: bool = False) -> date:
    """Solicita uma data ao usuário."""
    while True:
        try:
            data_str = input(prompt).strip()
            if permitir_vazio and not data_str:
                return None
            return parse_data(data_str)
        except ValueError as e:
            print(f"Erro: {e}")


def confirmar(prompt: str = "Confirma? (S/N): ") -> bool:
    """Solicita confirmação do usuário."""
    while True:
        resp = input(prompt).strip().upper()
        if resp in ('S', 'SIM', 'Y', 'YES'):
            return True
        elif resp in ('N', 'NAO', 'NÃO', 'NO'):
            return False
        print("Digite S para Sim ou N para Não.")


def pausar():
    """Pausa a execução até o usuário pressionar Enter."""
    input("\nPressione ENTER para continuar...")


def cabecalho(titulo: str):
    """Exibe um cabeçalho formatado."""
    limpar_tela()
    largura = 50
    print("=" * largura)
    print(f"{titulo.center(largura)}")
    print("=" * largura)
    print()
