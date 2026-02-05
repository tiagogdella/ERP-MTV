#!/usr/bin/env python3
"""
ERP MVP - Sistema de controle financeiro e operacional.

Empresa: MVP
Versão: 1.0
"""
import sys
import os

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db
from menu import menu_principal
from utils.helpers import limpar_tela


def main():
    """Ponto de entrada do sistema."""
    try:
        # Inicializa o banco de dados
        init_db()

        # Inicia o menu principal
        menu_principal()

    except KeyboardInterrupt:
        limpar_tela()
        print("\nSistema encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
