# Projeto ERP Terminal — MVP

## Contexto do Projeto
Este projeto é um ERP interno simples, desenvolvido para a empresa **MVP**, com foco em controle financeiro e operacional de curto prazo.

A motivação principal é registrar e controlar operações recorrentes de compra e venda de arroz entre empresas do mesmo grupo, com prazos curtos (ex: 7 dias), garantindo rastreabilidade, controle de caixa, histórico e auditoria interna.

O sistema será usado por poucos usuários, em ambiente local, e não tem como objetivo ser um sistema visual ou comercial neste momento.

---

## Filosofia do Sistema
- Terminal-first (interface em texto)
- Uso exclusivo de teclado
- Leve, rápido e simples
- Código claro > sofisticação
- Regras de negócio explícitas
- Fácil de auditar e entender

Este sistema deve lembrar ERPs antigos:
menus claros, navegação numérica e fluxos previsíveis.

---

## Escopo Inicial (MVP)
Funcionalidades mínimas esperadas:

1. Cadastro de empresas (ex: Empresa A, Empresa B)
2. Registro de operações:
   - Compra
   - Venda
   - Valor
   - Prazo (ex: 7 dias)
   - Data de vencimento
3. Controle de:
   - Contas a pagar
   - Contas a receber
4. Listagem de operações abertas e liquidadas
5. Histórico completo das operações
6. Exportação de dados para Excel (.xlsx)

---

## Fora do Escopo (por enquanto)
- Interface gráfica
- Web
- Multiusuário simultâneo
- Controle fiscal automatizado
- Integrações externas

---

## Tecnologia Escolhida
- Linguagem: **Python**
- Interface: **Terminal (CLI)**
- Banco de dados: **SQLite**
- Exportação: **Excel (.xlsx)**
- Execução: local (servidor ou máquina interna)

Evitar frameworks pesados ou desnecessários.

---

## Estrutura Esperada do Projeto
```text
mvp_erp/
│
├── main.py               # Entrada do sistema
├── menu.py               # Menus e navegação
├── database.py           # Conexão e setup do banco
├── models.py             # Estruturas de dados
├── services/
│   ├── operacoes.py      # Regras de compra e venda
│   ├── financeiro.py    # Contas a pagar/receber
│
├── export/
│   └── excel.py          # Exportação para Excel
│
├── utils/
│   └── helpers.py        # Funções utilitárias
│
└── data/
    └── mvp.db            # Banco SQLite
