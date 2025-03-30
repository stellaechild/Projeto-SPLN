---
title: Trabalho Prático 1
subtitle: SPLN 24-25, mestrado Informática
---

# 1- Descarregar o arquivo (usando OAI-PMH)

- Criar uma script que descarreca o arquivo inteiro (ou parte)

# 2- Estudar a estrutura do documento

- Dependências funcionais, chaves, campos constantes
- Arranjar uma função de prettyprint textual 
  - ? (yaml?) ou (wiki) ou até html
  - ? basead num (yaml/estrutura python) de configuração
  - simplificar 
  - agregar alguns campos numa notação mais legível
   data(inicio, fim, certeza)

# 3- Calcular a árvore arquivistica de fundos

- Usando os atributos `Parent` e eventualmente `RootParent`
- cuidado pode haver né em falta (ex: chamar-lhe 777-fixme)
- F   (fundo)
- SC  (secção)
- SSC (subsecção)
- SR  (Série)
- UI  (unidade de instalação)
- D  DC  (documento, documento composto)

# 4- Criar uma árvore de diretorias

Exemplo:

```
31258-F-Arquivo Casa de Pindela
    31259-SC-Luís de Carvalho e Beatriz de Almeida
        31260-SSC-Luís de Carvalho e Beatriz Almeida
            54460-SR-Documentos
    31262-SC-Simão Pinheiro e Leonor Almeida e Helena Dias
        31263-SSC-Simão Pinheiro e Leonor Almeida
            54461-SR-Documentos
        31265-SSC-Simão Pinheiro e Helena Dias
            54462-SR-Documentos
    31287-SC-João Machado Fagundes da Guerra Pinheiro e Figueira e Mariana Josefa de Castro
        31288-SSC-João Machado Fagundes da Guerra Pinheiro e Figueira e Mariana Josefa de Castro
            54469-SR-Documentos
            98419-SR-Correspondência
                98896-UI-Jerónimo Vaz Vieira
                98903-UI-João Pereira de Sousa
                98922-UI-António Vaz Vieira
                99010-UI-António Francisco Valbom
```

# 4a- Preencher um wiki com esta informação

Ex zim-wiki (wiki desktop)

# 4b- Criar HTML estático

- html hiperligado (árvore de fundos + documentos + ligação ao arquivo original)


# 6- Script de procura

várias hipoteses. Script python usando

- 6a usando rg
- criar indice glimpse
- sqlite + freetext search

# 7- Entidades mencionadas

- Criar um indice de entidades mencionadas
  - pessoas (e sua profissão / título)
  - lugares, casas

# 8- Focar em BiogHist e ScopeContent (outros?)

- tabela de Pessoas e suas biografias

# 9- Explorar thesaurus/indices (ver campo "terms")

- estrutura classificativa

# 10- Arranjar um tipo para cada nó

- formalizar (parcialmente) o tipo dos documentos, séries, DC, etc
- fotografia, carta, livro, seq(carta) 
- set(registo) 

