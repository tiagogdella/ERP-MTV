# 🇧🇷 ERP-MTV — Minha Terceira Versão

## 📌 Sobre o Projeto

O **ERP-MTV** é um sistema de gestão empresarial simplificado, desenvolvido em Python para rodar diretamente no terminal. O projeto nasceu de uma necessidade real: a empresa em que eu trabalhava em 2026 possuía hardware limitado para rodar sistemas robustos e precisava implantar uma nova operação de compra e venda de grãos.

A solução foi criar um software extremamente leve, focado em economia de processamento de dados e eficiência operacional, permitindo que processos complexos de ERP fossem executados em máquinas mais antigas sem perda de performance.

---

## 🚀 Funcionalidades

### Cadastros
- Cadastro, listagem e desativação de empresas/clientes

### Operações (Compra e Venda)
- Registro de compras e vendas com valor e prazo de vencimento
- Liquidação e cancelamento de operações

### Financeiro
- Resumo financeiro com saldo projetado
- Contas a pagar e contas a receber
- Alertas de operações vencidas

### Pedidos
- Cadastro de pedidos com múltiplos itens
- Tipos de embalagem: Granel, BAG, Fardo 30x1 e Fardo 10x1
- Cálculo automático de peso total (kg)
- Incidência de ICMS (12%) por item
- Baixa de pedido com registro de placa do veículo
- Consulta por cliente e alteração de data prevista de entrega

### Relatórios
- Histórico completo de operações

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Banco de dados:** SQLite (via `sqlite3` da biblioteca padrão)
- **Dependências externas:** nenhuma
- **Paradigma:** Programação estruturada/funcional voltada para performance

---

## ▶️ Como Executar

**Pré-requisito:** Python 3.10 ou superior instalado.

```bash
# Clone o repositório
git clone <url-do-repositorio>

# Acesse a pasta do projeto
cd ERP-MTV

# Execute o sistema
python3 mvp_erp/main.py
```

O banco de dados SQLite (`mvp.db`) é criado automaticamente na primeira execução.

---

## 📁 Estrutura do Projeto

```
mvp_erp/
├── main.py              # Ponto de entrada
├── database.py          # Conexão e inicialização do SQLite
├── models.py            # Estruturas de dados (dataclasses)
├── menu.py              # Menus e navegação por terminal
├── services/
│   ├── operacoes.py     # Lógica de compras e vendas
│   ├── financeiro.py    # Módulo financeiro
│   └── pedidos.py       # Módulo de pedidos
├── utils/
│   └── helpers.py       # Utilitários de entrada e formatação
└── data/
    └── mvp.db           # Banco de dados SQLite (gerado automaticamente)
```

---

## 📈 Impacto Gerado

A implementação permitiu que a terceira operação da empresa fosse iniciada sem a necessidade imediata de investimento em novos servidores ou estações de trabalho, garantindo a continuidade do negócio com custo zero de infraestrutura de hardware.

---
---

# 🇺🇸 ERP-MTV — My Third Version

## 📌 About the Project

**ERP-MTV** is a simplified Enterprise Resource Planning system developed in Python to run directly in the terminal. The project was born from a real-world business need: the company I worked for in 2026 had limited hardware to run standard robust systems and needed to implement a new grain trading operation.

The solution was to create extremely lightweight software, focused on data processing savings and operational efficiency, allowing complex ERP processes to run on older machines without performance loss.

---

## 🚀 Features

### Registrations
- Register, list, and deactivate companies/clients

### Operations (Purchase & Sales)
- Record purchases and sales with value and due date
- Settle and cancel operations

### Financial
- Financial summary with projected balance
- Accounts payable and accounts receivable
- Overdue operation alerts

### Orders
- Order registration with multiple items
- Package types: Bulk (Granel), BAG, 30x1 Bale, and 10x1 Bale
- Automatic total weight calculation (kg)
- Per-item ICMS tax (12%) calculation
- Order fulfillment with vehicle plate registration
- Query by client and delivery date management

### Reports
- Full operation history

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Database:** SQLite (via standard library `sqlite3`)
- **External dependencies:** none
- **Paradigm:** Performance-oriented structured/functional programming

---

## ▶️ How to Run

**Prerequisite:** Python 3.10 or higher installed.

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project folder
cd ERP-MTV

# Run the system
python3 mvp_erp/main.py
```

The SQLite database (`mvp.db`) is created automatically on first run.

---

## 📁 Project Structure

```
mvp_erp/
├── main.py              # Entry point
├── database.py          # SQLite connection and initialization
├── models.py            # Data structures (dataclasses)
├── menu.py              # Terminal menus and navigation
├── services/
│   ├── operacoes.py     # Purchase and sales logic
│   ├── financeiro.py    # Financial module
│   └── pedidos.py       # Orders module
├── utils/
│   └── helpers.py       # Input and formatting utilities
└── data/
    └── mvp.db           # SQLite database (auto-generated)
```

---

## 📈 Business Impact

The implementation allowed the company's third operation to begin without the immediate need for investment in new servers or workstations, ensuring business continuity with zero hardware infrastructure costs.
