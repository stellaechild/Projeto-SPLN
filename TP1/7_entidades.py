import os
import sqlite3
import spacy
from lxml import etree

def extrair_campos(xml_path,nlp):
    with open(xml_path, 'rb') as f:
        tree = etree.parse(f)
        ns = {
            'oai': 'http://www.openarchives.org/OAI/2.0/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/'
        }

        titulo = tree.findtext('.//dc:title', namespaces=ns) or ""
        assunto = tree.findtext('.//dc:subject', namespaces=ns) or ""
        texto = f"{titulo}. {assunto}"

        # spaCy NER
        doc = nlp(texto)
        pessoas = set()
        lugares = set()
        for ent in doc.ents:
            if ent.label_ == "PER":
                pessoas.add(ent.text)
            elif ent.label_ == "LOC":
                lugares.add(ent.text)

        return {
            'id': os.path.basename(xml_path),
            'titulo': titulo,
            'assunto': assunto,
            'texto': texto,
            'pessoas': ", ".join(pessoas),
            'lugares': ", ".join(lugares)
        }

def indexar_ficheiros(cur, nlp):
    indexed = set(row[0] for row in cur.execute("SELECT id FROM documentos").fetchall())
    for file in os.listdir("records"):
        if file.endswith(".xml") and file not in indexed:
            dados = extrair_campos(os.path.join("records", file), nlp)
            cur.execute("""
                INSERT INTO documentos (id, titulo, assunto, texto, pessoas, lugares)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (dados['id'], dados['titulo'], dados['assunto'], dados['texto'], dados['pessoas'], dados['lugares']))
            
             # Inserir pessoas
            for pessoa in dados['pessoas'].split(", "):
                if pessoa:
                    cur.execute("INSERT INTO entidades (doc_id, nome, tipo) VALUES (?, ?, ?)",
                                (dados['id'], pessoa, "pessoa"))
            # Inserir lugares
            for lugar in dados['lugares'].split(", "):
                if lugar:
                    cur.execute("INSERT INTO entidades (doc_id, nome, tipo) VALUES (?, ?, ?)",
                                (dados['id'], lugar, "lugar"))

def setup():
    nlp = spacy.load("pt_core_news_lg")
    conn = sqlite3.connect("arquivo.db")
    cur = conn.cursor()
    return nlp, conn, cur

def close_db(conn):
    conn.commit()
    conn.close()
    
def indexar(cur, nlp):
    # Criar tabela com FTS5
    cur.execute("DROP TABLE IF EXISTS entidades")
    cur.execute("""
        CREATE TABLE entidades (
            doc_id TEXT,
            nome TEXT,
            tipo TEXT
        )
    """)
    
    indexar_ficheiros(cur,nlp)
    print("Indexação concluída")


def pesquisar(query, cur):
    res = cur.execute(query)
    for doc_id, titulo, pessoas, lugares in res:
        print(f" Documento: {doc_id} - {titulo}")
        if pessoas:
            print(f"Pessoas: {pessoas}")
        if lugares:
            print(f"Lugares: {lugares}")
        print()
    
query = """
        SELECT id, titulo, pessoas, lugares FROM documentos
        WHERE pessoas != '' OR lugares != ''
    """

def main():
    nlp, conn, cur = setup()
    indexar(cur, nlp)
    pesquisar(query, cur)
    close_db(conn)

if __name__ == "__main__":
    main()
    
# pip install sqlite-utils
