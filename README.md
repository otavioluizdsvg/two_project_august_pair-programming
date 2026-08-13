# 🐍 Projetos Educacionais em Python - Finanças e História

Este repositório contém uma coleção de aplicações gráficas desenvolvidas em **Python** utilizando **Tkinter**. Os projetos foram elaborados com foco didático para alunos do programa **Jovem Aprendiz**, integrando conceitos de **programação procedural**, **educação financeira** e **história do Brasil**.

---

## 🎯 Objetivos Didáticos

* **Lógica Procedural:** Estruturação de código sem o uso de Orientação a Objetos (POO), facilitando a assimilação inicial de funções, parâmetros e escopo global (`global`).
* **Interface Gráfica (GUI):** Construção de telas interativas com `tkinter` e componentes modernos (`ttk.Notebook`, `Listbox`, `Frame`, etc.).
* **Tratamento de Exceções:** Uso de blocos `try/except` para validação de entradas numéricas do usuário.
* **Consumo de Requisições HTTP:** Integração com a web (`requests`) e manipulação de imagens (`Pillow`).

---

## 🚀 Projetos Incluídos

### 1. 📜 Linha do Tempo: Eufrásia Teixeira Leite (`historia_financas_with_eufrasia_seunome.py`)
Uma interface interativa sobre **Eufrásia Teixeira Leite** (1850–1930), a primeira investidora global do Brasil.
* **Destaques:** 
  * Download e exibição de imagem via requisição HTTP (`requests` e `Pillow`).
  * Tratamento de falhas de conexão para manter a aplicação funcional mesmo offline.
  * Botões interativos para exibição de fatos históricos.

---

### 2. 💵 Simulador de Aportes (`financas_aportes_bankb3_seunome.py`)
Uma calculadora de fluxo de caixa simplificada para ensinar operações de depósito e saque.
* **Destaques:**
  * Controle de saldo em tempo real.
  * Validação para impedir saques maiores do que o saldo disponível.
  * Atualização dinâmica dos rótulos e campos de texto.

---

### 3. 📊 Dashboard Financeiro - Padrão B3 (`financas_dashboard_bankb3_seunome.py`)
Um painel completo simulando o ambiente da Bolsa de Valores brasileira (B3).
* **Destaques:**
  * Uso de abas interativas (`ttk.Notebook`) para navegar entre **Conta Corrente**, **Criptoativos** e **Extrato**.
  * Simulação de compra de frações de Bitcoin (BTC).
  * Histórico de transações em tempo real utilizando `tk.Listbox`.

---

## 🛠️ Pré-requisitos e Instalação

Para executar os projetos, você precisará do **Python 3.10+** instalado em sua máquina.

### 1. Instalar as dependências do projeto
Abra o terminal ou prompt de comando e execute:

```bash
pip install requests pillow

```
```bash
python -m pip install requests pillow

```


> **Nota:** O `tkinter` já vem instalado por padrão na maioria das instalações do Python para Windows/macOS. Caso esteja utilizando Linux (Ubuntu/Debian), instale-o via terminal:
> `sudo apt-get install python3-tkinter`

---

## 💻 Como Executar as Aplicações

Navegue até a pasta do projeto no seu terminal e rode o arquivo desejado:

```bash
# Executar a Linha do Tempo de Eufrásia
python historia_financas_with_eufrasia_seunome.py

# Executar o Simulador de Aportes
python financas_aportes_bankb3_seunome.py

# Executar o Dashboard B3
python financas_dashboard_bankb3_seunome.py

```

---

## 🗂️ Estrutura do Repositório

```text
.
├── historia_financas_with_eufrasia_seunome.py    # Aplicação sobre Eufrásia Teixeira Leite
├── financas_aportes_bankb3_seunome.py    # Simulador simples de depósitos e saques
├── financas_dashboard_bankb3_seunome.py         # Dashboard financeiro com abas (B3)
└── README.md               # Documentação do projeto

```

---

💙 *Projeto desenvolvido para fins educacionais e de capacitação profissional.*
