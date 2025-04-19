import sqlite3
import os
import glob
import xml.etree.ElementTree as ET
import sys

DB_NAME = "arquivo.db"
RECORDS_DIR = "records"

NAMESPACES = {
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "dc": "http://purl.org/dc/elements/1.1/"
}

def parse_dates(dates):
    anos = sorted(set(int(d) for d in dates if d.isdigit()))
    if not anos:
        return None, None
    return anos[0], anos[-1]

def extrair_dados(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    metadata = root.find(".//oai_dc:dc", NAMESPACES)
    if metadata is None:
        return None

    get = lambda tag: [e.text.strip() for e in metadata.findall(f"dc:{tag}", NAMESPACES) if e.text]

    titulo = " | ".join(get("title"))
    assunto = " | ".join(get("subject"))
    datas = get("date")
    data_inicio, data_fim = parse_dates(datas)
    tipo = " | ".join(get("type"))
    formato = " | ".join(get("format"))
    identificadores = get("identifier")
    relacoes = get("relation")

    # Link visível + código interno
    url = identificadores[0] if identificadores else None
    codigo = identificadores[1] if len(identificadores) > 1 else None

    return {
        "titulo": titulo,
        "assunto": assunto,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "tipo": tipo,
        "formato": formato,
        "url": url,
        "codigo": codigo,
        "relacao": relacoes[0] if relacoes else None
    }

def criar_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE VIRTUAL TABLE documentos USING fts5(
            titulo, assunto, tipo, formato,
            codigo UNINDEXED,
            data_inicio UNINDEXED, data_fim UNINDEXED,
            url UNINDEXED, relacao UNINDEXED
        );
    """)
    conn.commit()
    conn.close()

def inserir_dados():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for xml_file in glob.glob(os.path.join(RECORDS_DIR, "*.xml")):
        dados = extrair_dados(xml_file)
        if dados:
            c.execute("""
                INSERT INTO documentos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados["titulo"], dados["assunto"], dados["tipo"], dados["formato"],
                dados["codigo"], dados["data_inicio"], dados["data_fim"],
                dados["url"], dados["relacao"]
            ))

    conn.commit()
    conn.close()
    
def procurar(termo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = """
        SELECT titulo, codigo, url, snippet(documentos, 0, '<b>', '</b>', '...', 40)
        FROM documentos
        WHERE documentos MATCH ?
        LIMIT 10;
    """
    for row in c.execute(query, (termo,)):
        titulo, codigo, url, snippet = row
        print(f"\n {titulo}\n {codigo}\n {url}\n {snippet}\n")

    conn.close()

if __name__ == "__main__":
    # correr uma vez para inserir os dados
    # criar_db()
    # inserir_dados()

    # python3 6_procura.py <termo>")
    
    if len(sys.argv) < 2:
        exit(1)

    termo = " ".join(sys.argv[1:])
    procurar(termo)
