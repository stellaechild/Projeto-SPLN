---
UC: SPLN 24-25, mestrado Informática
autores: Maria Cunha pg54042 | Tomás Campinho pg57742 | Lingyun Xhu pg57885
---

# Trabalho Prático 1: SPLN 24-25

## 1. Descarregar o arquivo (usando OAI-PMH)
```
python3 1_descarregar.py
```
Descarrega os registos usando OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting) através do objeto sickle do url
https://www.arquivoalbertosampaio.org/OAI-PMH/ em oai_dc que corresponde a um padrão simples e comum dos metadados.

## 2. Estudar a estrutura do documento
```
python3 2_estrutura.py
```
Para cada registo, guarda os seguintes dados em yaml, agregando o campo de data (início, fim e certeza):
```
{'id': identifier,
    'titulo': get_dc('title')[0] if get_dc('title') else None,
    'datas': {
        'inicio': date_inicio,
        'fim': date_fim,
        'certeza': certeza_data
    },
    'editor': get_dc('publisher')[0] if get_dc('publisher') else None,
    'assunto': get_dc('subject')[0] if get_dc('subject') else None,
    'tipo': get_dc('type')[0] if get_dc('type') else None,
    'formato': get_dc('format')[0] if get_dc('format') else None,
    'lingua': get_dc('language')[0] if get_dc('language') else None,
    'identificadores': get_dc('identifier'),
    'thumbnail': get_dc('relation')[0] if get_dc('relation') else None,
    'colecoes': sets
}
```

## 3. Calcular a árvore arquivistica de fundos
```
python3 3_arvore_arq.py -> archival_tree.txt
```
Busca nos registos_yaml o segundo elemento do campo 'identificadores', por exemplo: PT/MVNF/AMAS/AS-AS/C-A-B/000001, cria um dicionário com os nodos, para este caso, que correspondem às diretorias e documentos existentes nos registos, que for fim imprime a estrutura obtida.

```
F:PT 
SC:PT/MVNF
SSC:PT/MVNF/AMAS
SR:PT/MVNF/AMAS/AS-AS
UI:PT/MVNF/AMAS/AS-AS/C-A-B
D:PT/MVNF/AMAS/AS-AS/C-A-B/000001
```

## 4. Criar uma árvore de diretorias
```
python3 4_arvore_dir.py
```
Gera uma estrutura de diretorias baseada na hierarquia arquivística dos registos. Para cada nó, cria uma pasta com um arquivo `README.md` contendo informações sobre o nó:
- Cria um arquivo de texto com a árvore arquivística (`output/archival_tree.txt`).
- Cria uma versão html da árvore com links para os registos yaml (`output/html_arvore/index.html`).
- Cria uma versão em formato Wiki (`output/wiki_arvore/wiki.txt`).

## 6. Script de procura
Primeiro passo: Criar a base de dados em sqlite e inserir os dados.
Segundo passo:
```
python3 6_procura.py <termo>
```
Procura os artigos que contenham o termo através do seu título e do seu conteúdo, mostrando todos os resultdos obtidos.

## 7. Entidades mencionadas
```
python3 7_entidades.py > entidades.txt
```
Guarda no ficheiro as pessoas, lugares e profissão de cada registo.

## 9. Explorar thesaurus/indices
```
python3 9_thesaurus.py
```
Gera um arquivo html (`thesaurus.html`) que organiza os registos por categorias (baseadas no campo `type`) e exibe os termos associados a cada título. Cada categoria contém uma lista de títulos e os termos relacionados, permitindo explorar os dados de forma categorizada.