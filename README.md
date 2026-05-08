# ANBIMA Financial Data ETL Pipeline

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Selenium](https://img.shields.io/badge/library-selenium-green.svg)
![Pandas](https://img.shields.io/badge/library-pandas-orange.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

## Descrição do Projeto

Este repositório contém uma solução automatizada de **Business Intelligence** para a extração, processamento e consolidação de indicadores financeiros da ANBIMA. O pipeline foca especificamente nos índices **IMA** (Índice de Mercado ANBIMA) e **IDkA** (Índices de Duração Constante ANBIMA).

A aplicação automatiza a navegação web, supera desafios de interfaces baseadas em frames, trata inconsistências de tipos de dados financeiros e gera relatórios prontos para análise técnica ou alimentação de bancos de dados.

## Arquitetura do Sistema

O projeto adota os princípios de **Clean Code** e **Separação de Preocupações (SoC)**, dividindo a lógica em camadas distintas:

```text
├── data/               # Persistent Storage (Relatório gerado)
├── src/                # Core Application Logic
│   ├── scraper.py      # Data Extraction Layer (Selenium/Web Automation)
│   ├── processor.py    # Transformation Layer (Data Wrangling com Pandas)
│   └── utils.py        # Shared Utilities (Formatação e Sanetização)
├── main.py             # Application Entry Point (Workflow Orchestration)
├── requirements.txt    # Dependency Management
└── README.md           # Technical Documentation
```

## Configuração e Instalação

### Pré-requisitos
- ython 3.8 ou superior.

- Google Chrome instalado (o driver é gerenciado automaticamente).

### 1. Instalação
```
git clone [git clone https://github.com/Almeida-Adriel/Extracao-diaria-fundos-ima.git](git clone https://github.com/Almeida-Adriel/Extracao-diaria-fundos-ima.git)
```

### 2. Crie e ative um ambiente virtual:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

### 3. Instale as dependências:
```
Instale as dependências:
```

### 4. Excução
```
python main.py # Conferir se está na pasta Extracao-diaria-fundos-ima
```

Desenvolvido por: Adriel Almeida Pereira Leite
Finalidade: Automação de Processos Financeiros
