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

## Utilização no Google Colab

Para utilizar o notebook `sentence_similarity.ipynb` no Google Colab, siga estes passos:

1. Carregue o notebook para o Google Colab:
   - Aceda ao [Google Colab](https://colab.research.google.com/)
   - Clique em `Ficheiro` > `Carregar notebook`
   - Escolha o ficheiro `sentence_similarity.ipynb` do seu computador

2. Carregue os ficheiros de dados necessários:
   - Clique no ícone da pasta na barra lateral esquerda
   - Crie um diretório `data`:
     ```python
     !mkdir -p data
     ```
   - Carregue os seus ficheiros de dados para este diretório:
     - `training_data.json` (criado por process_data.py)
     - `col_1822_21316_processed.json` (coleção de documentos processados)
   
   - Em alternativa, pode montar o Google Drive e copiar ficheiros:
     ```python
     from google.colab import drive
     drive.mount('/content/drive')
     !cp -r /content/drive/MyDrive/caminho_para_os_seus_dados/* data/
     ```

3. Configure o ambiente de execução/Change Runtime Type:
   - Vá a `Ambiente de execução` > `Alterar tipo de ambiente de execução`
   - Selecione `GPU`

4. Execute o notebook:
   - Execute as células sequencialmente para evitar problemas de dependência
