---
title: Trabalho Prático II
author: 
- Tomás Campinho
- Maria Cunha
- Lingyun Zhu
date: Junho 2025
---

# Relatório de Utilização do Sistema de Processamento de Dados do RepositoriUM

## Funcionalidades

- Recolha de dados do RepositoriUM utilizando o protocolo OAI-PMH
- Processamento e limpeza de metadados de documentos
- Criação de dados de treino para modelos de similaridade
- Afinação de um modelo de transformador de frases para similaridade de documentos
- Sistema de information retrieval baseado em similaridade semântica

## Estrutura de Ficheiros

- `collect_data.py`: Recolhe dados do RepositoriUM usando OAI-PMH
- `process_data.py`: Processa dados XML e cria coleções de treino
- `sentence_similarity.ipynb`: Notebook para treinar e utilizar o modelo de similaridade
- `information_retireval.py`: Módulo que utiliza o modelo treinado para calcular a similaridade

## Utilização

### 1. Recolher Dados

```bash
python collect_data.py
```

Isto irá recolher dados do RepositoriUM para o diretório `data`.

### 2. Processar Dados

```bash
python process_data.py
```

Isto irá:
- Converter dados XML para formato JSON
- Limpar e normalizar metadados
- Criar pares de treino com pontuações de similaridade

### 3. Treinar e Utilizar o Modelo

Abra e execute o `sentence_similarity.ipynb` para:
- Carregar os dados de treino
- Treinar um modelo de transformador de frases
- Utilizar o modelo para information retrieval baseado em similaridade semântica

## Utilização do módulo

Para poder começar a usar o modelo treinado para calcular a similaridade dos abstratos é necessário instalar o módulo primeiro.

1. Instalar com o comando `pip install .` na diretoria módulo, onde se situa o ficheiro `pyproject.toml`

2. Executar com `sim documento1.txt documento2.txt ... documenton.txt`

3. Para listar os top n documentos, passar a flag `-n`, por exemplo, `sim documento1.txt documento2.txt ... documenton.txt`
